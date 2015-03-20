#!/usr/bin/env python
import os
from app import create_app, db, mongo, models
from app.mongo_models import User, Post
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, mongo=mongo, m=models)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    from flask.ext.migrate import upgrade

    upgrade()
    User.init_user()

if __name__ == '__main__':
    manager.run()
