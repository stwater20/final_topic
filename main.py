from flask_bootstrap import Bootstrap
from config import DevConfig
from flask import Flask,render_template





app = Flask(__name__)
app.config.from_object(DevConfig)
bootstrap = Bootstrap(app)

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run()
