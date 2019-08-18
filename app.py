from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from gameController import game_controller
from game import Display

app = Flask(__name__, template_folder="server/templates")
Bootstrap(app)
app.register_blueprint(game_controller)


@app.route('/')
def index():
    return render_template('index.html', title="Web Othello", welcomeText=Display.get_intro())


if __name__ == '__main__':
    app.run(port=8080, debug=True)
