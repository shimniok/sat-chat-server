import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import create_config
from api.models import db
from app import create_app

app = create_app()

app.config.from_object(create_config(env = os.environ['APP_SETTINGS']))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

#@manager.commands
#def seed():
#    "Add seed data to the database"
#    u = User(user='admin', email='', password='sha256$Gvk5fRPF$74462c8a5da334bf551b2943eda4604ba4ae4ba3ec7f0d86154238ef7aaa8e3d')
#    db.session.add(u)
#    db.session.commit()

if __name__ == '__main__':
    manager.run()
