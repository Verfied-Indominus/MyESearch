from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import publication, topic
index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    topics = topic.get_all_topics()
    publications = publication.get_recent()
    return render_template('index.html',topics=topics,publications=publications)

@index_views.route('/publication/<id>',methods=["GET"])
def publication_page(id):
    
    pub = publication.get_pub_byid(id)
    if not pub:
        return("404")
    return render_template("publication.html",pub=pub.toDict())
    

# @index_views.route('/', methods=['GET'])
# def health_check():
#     return jsonify({'status':'healthy'})