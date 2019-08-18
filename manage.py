from flask_migrate import Migrate, MigrateCommand, Manager

import config
from app import app
from database import db

app.config.from_object(config.get_config_environment())

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
