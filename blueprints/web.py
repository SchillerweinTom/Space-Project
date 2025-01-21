from flask import Flask, Blueprint, render_template

app = Blueprint("web", __name__)

@app.route('/')
def load_home_page():
    return render_template('mainPage.html')
