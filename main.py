from flask import Flask
from config import DevConfig
from crawler import crawler
app = Flask(__name__)
app.config.from_object(DevConfig)

@app.route('/')
def index():
    return 'Hello World!'


url = 'https://od.moi.gov.tw/MOI/v1/pbs'




if __name__ == '__main__':
    app.run()
