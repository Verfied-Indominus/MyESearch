from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models.forms import *
import json

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

@index_views.route('/interests/<selected>', methods=['GET'])
def parse_interests(selected):
    selected = json.loads(selected)
    print(selected)
    print(selected['selected'][0]) #AMAZING
    return jsonify(selected)