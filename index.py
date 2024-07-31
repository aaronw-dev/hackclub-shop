from flask import Flask, render_template

app = Flask(__name__,
            static_url_path='/resources',
            static_folder='static',
            template_folder='templates')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return 'About'
