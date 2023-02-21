import pyrebase
import os

config = {
  "apiKey": "AIzaSyAkDqi_KOPXF_jmaed8MxL7kerY9jY0ZgM",
  "authDomain": "my-e-search.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "my-e-search.appspot.com"
}


# const firebaseConfig = {
#   apiKey: "AIzaSyAkDqi_KOPXF_jmaed8MxL7kerY9jY0ZgM",
#   authDomain: "my-e-search.firebaseapp.com",
#   projectId: "my-e-search",
#   storageBucket: "my-e-search.appspot.com",
#   messagingSenderId: "401005454141",
#   appId: "1:401005454141:web:0b738fcc77657467d05b54",
#   measurementId: "G-HFMRPL61EW"
# };
#initilize firebase connection
firebase = pyrebase.initialize_app(config)


#STORAGE

storage = firebase.storage()

#as admin
def uploadFile(file_name):
    return storage.child(f"/workspaces/MyESearch/App/uploads/{file_name}").put(f"{file_name}")
# storage.child("images/example.jpg").put("example.jpg")

#as user
# storage.child("images/example.jpg").put("example2.jpg", user['idToken'])

# #download
# storage.child("images/example.jpg").download("downloaded.jpg")

# #get url of file
# storage.child("images/example.jpg").get_url()
# https://firebasestorage.googleapis.com/v0/b/storage-url.appspot.com/o/images%2Fexample.jpg?alt=media
