from django.contrib import admin
from django.urls import path
from Student.views import index, register, log_in, my_lesson, my_grades, my_info, user_logout, search_test, grade1718, \
    grade1819, grade1920, school_news, news_detail, get_test, get_exam, get_passwd,passwd,exam_check

app_name = '[Student]'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index/', index),
    path('register/', register),
    path('log_in/', log_in, name='log_in'),
    path('my_lesson', my_lesson),
    path('my_grades', my_grades),
    path('my_info', my_info),
    path('logout', user_logout),
    path('search_test', search_test),
    path('grade1718', grade1718),
    path('grade1819', grade1819),
    path('grade1920', grade1920),
    path('school_news', school_news),
    path('news_detail/<int:new_ids>', news_detail),
    path('get_test', get_test),
    path('get_exam', get_exam),
    path('get_passwd', get_passwd),
    path('passwd', passwd),
    path('exam_check',exam_check),
]
