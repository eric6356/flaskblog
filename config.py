import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    BLOG_MAIL_SUBJECT_PREFIX = '[Blog]'
    BLOG_MAIL_SENDER = MAIL_USERNAME + '@qq.com'
    BLOG_ADMIN = os.environ.get('BLOG_ADMIN')
    UPLOAD_FOLDER = '/home/flask/imgs'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'blog-dev',
        'host': '127.0.0.1',
        'port': 27017
    }


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'blog-test',
        'host': '127.0.0.1',
        'port': 27017
    }


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'blog',
        'host': '127.0.0.1',
        'port': 27017
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
