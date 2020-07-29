from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import datetime


from Student.models import Student, Teacher, Lesson, Grades, News, Exam

# 主页
def index(request):
    student_school_id = request.POST.get('student_school_id')
    student_passwd = request.POST.get('student_passwd')
    if student_school_id is None or student_passwd is None:
        return render(request, 'index.html', {})
    try:
        search_student = Student.objects.get(student_study_id=student_school_id)
    except Exception:
        error = '不存在该学号!'
        return render(request, 'index.html', {'error1': error})
    if search_student.student_passwd != student_passwd:
        error = '密码错误！'
        return render(request, 'index.html', {'error2': error})
    else:
        response = redirect('/log_in')
        response.set_cookie('user_id', student_school_id, max_age=60 * 60 * 24)
        return response


# 找回密码
def get_passwd(request):
    student_name = request.POST.get('student_name')
    student_study_id = request.POST.get('student_study_id')
    student_id_card = request.POST.get('student_id_card')
    if student_name is None or student_id_card is None or student_study_id is None:
        return render(request, 'get_passwd.html', {})
    student = Student.objects.get(student_name=student_name)
    student_passwd = student.student_passwd
    if student.student_study_id == int(student_study_id) and student.student_id_card == int(student_id_card):
        response = redirect('/passwd')
        response.set_cookie('student_study_id', student_study_id, max_age=5)
        return render(request, 'passwd.html', {'student_passwd': student_passwd})
    err = '存在错误项，请检查！'
    return render(request, 'get_passwd.html', {'err': err})


def passwd(request):
    return render(request, 'passwd.html', {})


# 修改密码页面
def register(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        user = Student.objects.get(student_study_id=user_id)
        student_passwd = request.POST.get('student_passwd')
        if user.student_passwd != student_passwd and request.method == 'POST':
            err = '原密码错误!'
            return render(request, 'register.html', {'err': err})
        student_passwd1 = request.POST.get('student_passwd1')
        student_passwd2 = request.POST.get('student_passwd2')
        if student_passwd1 != student_passwd2 and request.method == 'POST':
            err1 = '密码输入不一致!'
            return render(request, 'register.html', {'err1': err1})
        if student_passwd1 is None:
            user.student_passwd = user.student_passwd
        else:
            user.student_passwd = student_passwd1
        user.save()
        if request.method == 'POST':
            return redirect('/index')
        return render(request, 'register.html', {})
    else:
        return redirect('/index')


# 学生中心首页
def log_in(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        print(user_id)
        student1 = Student.objects.filter(student_study_id=user_id)

        return render(request, 'person_index.html', {'student': student1})
    else:
        return redirect('/index')


# 课程表
def my_lesson(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        lesson = Lesson.objects.filter(student__student_study_id=user_id)
        student1 = Student.objects.filter(student_study_id=user_id)
        list = []
        for i in lesson:
            teacher = Teacher.objects.filter(lesson__lesson_name=i.lesson_name)
            for i in teacher:
                print(i.teacher_name)
                list.append(i.teacher_name)
        print(list)
        return render(request, 'my_lesson.html', {'student': student1, 'lesson': lesson, 'list': list})
    else:
        return redirect('/index')


# 我的成绩
def my_grades(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        lesson = Lesson.objects.filter(student__student_study_id=user_id)
        print(type(lesson))
        for i in lesson:
            print(i)
        student1 = Student.objects.filter(student_study_id=user_id)
        grade = Grades.objects.filter(student_name__student_study_id=user_id)
        sum = 0
        sum1 = 0
        k = 0
        m = 0
        for i in grade:
            sum += i.lesson_name.lesson_score
            if i.grade < 60:
                k += 1
            if i.grade >= 60:
                sum1 += i.lesson_name.lesson_score
                m += 1
        return render(request, 'my_grades.html', {'student': student1, 'grade': grade, 'sum': sum, 'k': k,
                                                  'sum1': sum1, 'm': m})
    else:
        return redirect('/index')


# 基本信息
def my_info(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student_tel = request.POST.get('student_tel')
        student_email = request.POST.get('student_email')
        student_addr = request.POST.get('student_addr')
        student_short = request.POST.get('student_short')
        print(student_tel, student_email, student_addr, student_short)
        student1 = Student.objects.filter(student_study_id=user_id)
        user = Student.objects.get(student_study_id=user_id)
        print(user.student_addr, user.student_email)
        if student_tel is None:
            user.student_tel = user.student_tel
        else:
            user.student_tel = student_tel
        if student_email is None:
            user.student_email = user.student_email
        else:
            user.student_email = student_email
        if student_addr is None:
            user.student_addr = user.student_addr
        else:
            user.student_addr = student_addr
        if student_short is None:
            user.student_short = user.student_short
        else:
            user.student_short = student_short
        user.save()
        flag = str(user.student_study_id)[0]
        name = user.student_name
        return render(request, 'my_info.html', {'student': student1, 'flag': flag, 'name': name, 'user': user})
    else:
        return redirect('/index')


# 退出登陆
def user_logout(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        if request.method == 'POST':
            response = redirect('/index')
            response.delete_cookie('user_id')
            return response
        else:
            return render(request, 'logout.html', {})
    else:
        return redirect('/index')


# 查看考试
def search_test(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        lesson = Lesson.objects.filter(student__student_study_id=user_id)
        student1 = Student.objects.filter(student_study_id=user_id)
        return render(request, 'search_test.html', {'lesson': lesson, 'student': student1})
    else:
        return redirect('/index')


def grade1718(request):
    return render(request, 'grade-1718.html', {})


def grade1819(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        grade = Grades.objects.filter(student_name__student_study_id=user_id)
        sum = 0
        sum1 = 0
        k = 0
        m = 0
        for i in grade:
            if i.lesson_name.lesson_data == '18-19':
                sum += i.lesson_name.lesson_score
                if i.grade < 60:
                    k += 1
                if i.grade >= 60:
                    sum1 += i.lesson_name.lesson_score
                    m += 1
        return render(request, 'grade-18-19.html',
                      {'student': student1, 'grade': grade, 'sum': sum, 'sum1': sum1, 'm': m, 'k': k})
    else:
        return redirect('/index')


def grade1920(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        grade = Grades.objects.filter(student_name__student_study_id=user_id)
        sum = 0
        sum1 = 0
        k = 0
        m = 0
        for i in grade:
            if i.lesson_name.lesson_data == '19-20':
                sum += i.lesson_name.lesson_score
                if i.grade < 60:
                    k += 1
                if i.grade >= 60:
                    sum1 += i.lesson_name.lesson_score
                    m += 1
        return render(request, 'grade-19-20.html',
                      {'student': student1, 'grade': grade, 'sum': sum, 'sum1': sum1, 'm': m, 'k': k})
    else:
        return redirect('/index')


# 学校新闻页面
def school_news(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        today = datetime.date.today()
        print(today)
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        data = week_day_dict[datetime.datetime.now().weekday()]
        page = request.GET.get('page')
        if page:
            page = int(page)
        else:
            page = 1
        news = News.objects.all()
        paginator = Paginator(news, 5)
        page_num = paginator.num_pages
        page_news_list = paginator.page(page)
        if page_news_list.has_next():
            next_page = page + 1
        else:
            next_page = page
        if page_news_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        return render(request, 'school_news.html', {'student': student1, 'today': today, 'data': data, 'news': news,
                                                    'cuur_page': page, 'next_page': next_page,
                                                    'previous_page': previous_page,
                                                    # 'page_news_list': page_news_list,
                                                    'page_num': range(1, page_num + 1)})
    else:
        return redirect('/index')


# 新闻详情页面
def news_detail(request, new_ids):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        news = News.objects.all()
        student1 = Student.objects.filter(student_study_id=user_id)
        for index, new in enumerate(news):
            if new.news_id == new_ids:
                title = new.news_title
                acontents = new.news_body.split('\n')
                break
        return render(request, 'news_detail.html', {'student': student1, 'acontents': acontents, 'title': title,
                                                    })
    else:
        return redirect('/index')


# 选修课程选择
def get_test(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        student2 = Student.objects.get(student_study_id=user_id)
        lesson = Lesson.objects.all()
        list = []
        for i in lesson:
            if not i.is_default:
                list.append(i)
        if request.method == 'POST':
            try:
                a = request.POST.get('zzz')
                print(a)
                lesson = Lesson.objects.filter(student__student_study_id=user_id)
                flag = 0
                for i in lesson:
                    if not i.is_default:
                        flag += 1
                if flag >= 4:
                    err = '每个学生一学期之多选择四门选修课！'
                    return render(request, 'get_test.html', {'err': err, 'list': list})
                for i in lesson:
                    if i.lesson_name == a:
                        if flag >= 4:
                            err = '每个学生一学期之多选择四门选修课！'
                        else:
                            err = '该门课程已经选过了！请重新选择！'

                        return render(request, 'get_test.html', {'err': err, 'list': list})
                get_num = Lesson.objects.get(lesson_name=a)
                if get_num.lesson_num <= 0:
                    err = '课程人数已满！'
                    return render(request, 'get_test.html', {'err': err, 'list': list})
                get_num.lesson_num -= 1
                get_num.save()
                Lesson.objects.get(lesson_name=a).student.add(student2)
                mes = '选课成功！'
                # print(get_lesson)
                return render(request, 'get_test.html', {'mes': mes, 'list': list})
            except:
                return redirect('/get_test')
        return render(request, 'get_test.html', {'student': student1, 'list': list})
    else:
        return redirect('/index')


# 全国考试选择
def get_exam(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        student2 = Student.objects.get(student_study_id=user_id)
        exam = Exam.objects.all()
        exam_get = Exam.objects.filter(student__student_study_id=user_id)
        if request.method == 'POST':
            try:
                a = request.POST.get('zzz')
                print(a)
                Exam.objects.get(exam_name=a).student.add(student2)
                exam_get = Exam.objects.filter(student__student_study_id=user_id)
                print(exam_get)
                return render(request, 'get_exam.html', {'student': student1, 'exam': exam, 'exam_get': exam_get})
            except:
                return render(request, 'get_exam.html', {'student': student1, 'exam': exam, 'exam_get': exam_get})
        return render(request, 'get_exam.html', {'student': student1, 'exam': exam,'exam_get':exam_get})
    else:
        return redirect('/index')

def exam_check(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        student2 = Student.objects.get(student_study_id=user_id)
        exam = Exam.objects.all()
        exam_get = Exam.objects.filter(student__student_study_id=user_id)
        if request.method == 'POST':
            try:
                a = request.POST.get('zzz')
                print(a)
                Exam.objects.get(exam_name=a).student.remove(student2)
                exam_get = Exam.objects.filter(student__student_study_id=user_id)
                print(exam_get)
                return render(request, 'get_exam.html', {'student': student1, 'exam': exam, 'exam_get': exam_get})
            except:
                return render(request, 'get_exam.html', {'student': student1, 'exam': exam, 'exam_get': exam_get})
        return render(request, 'get_exam.html', {'student': student1, 'exam': exam, 'exam_get': exam_get})
    else:
        return redirect('/index')