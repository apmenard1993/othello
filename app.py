from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import config
from database import db
from game import Display
# create app
from server.gameController import game_controller

app = Flask(__name__, template_folder="server/templates")
Bootstrap(app)

# configure
app.config.from_object(config.get_config_environment())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# register blueprints
app.register_blueprint(game_controller)

# noinspection PyUnresolvedReferences
from server import models

# default routes
@app.route('/')
def index():
    return render_template('index.html', title="Web Othello", welcomeText=Display.get_intro())


if __name__ == '__main__':
    app.run(port=8080)
