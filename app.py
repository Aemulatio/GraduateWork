from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    # return "Hello world"
    # data = csv_reader('results.csv')
    return render_template('index.html')

# def sum(a, b):
#     return a + b


if __name__ == '__main__':
    app.run()
