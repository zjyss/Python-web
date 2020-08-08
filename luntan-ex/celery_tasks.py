import config
from celery import Celery
from exts import mail
from flask_mail import Message
from flask import Flask

jingyu = Flask(__name__)

jingyu.config.from_object(config)
mail.init_app(jingyu)


def make_celery(app):
    celery = Celery(
        # app.import_name,
        'default',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(jingyu)


@celery.task
def sendmail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message=message)
