from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Christoffer:hvsxYJ3GOVtjeMK3@cluster0.cjztj.mongodb.net/test'
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
