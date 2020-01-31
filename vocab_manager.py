import os
from app import create_app, db
from app.models import User

config = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('testing')
    unittest.TextTestRunner(verbosity=2).run(tests)
