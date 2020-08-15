from wechat import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    manager.run()   
