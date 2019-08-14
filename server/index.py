from flask import Flask

from game import Display

app = Flask(__name__)


@app.route('/')
def index():
    return Display.get_intro()


if __name__ == '__main__':
    app.run(port=8080, debug=True)
