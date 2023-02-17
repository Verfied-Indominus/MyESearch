from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models.forms import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/signup', methods=['GET'])
def signup_page():
    form = ResearcherSignUpForm()
    return render_template('signup.html', form=form)