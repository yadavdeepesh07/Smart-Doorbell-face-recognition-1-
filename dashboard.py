from flask import Flask, render_template, request, redirect
from app.aws_rekognition import list_faces, delete_face, index_face
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    logs = []
    if os.path.exists("logs/visitor_log.json"):
        with open("logs/visitor_log.json") as f:
            logs = json.load(f)
    return render_template("index.html", logs=logs)

@app.route('/manage_users')
def manage_users():
    return render_template("manage_users.html", faces=list_faces())

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    with open(filepath, 'rb') as f:
        index_face(f.read(), name)
    os.remove(filepath)
    return redirect('/manage_users')

@app.route('/delete_user', methods=['POST'])
def delete_user():
    face_id = request.form['face_id']
    delete_face(face_id)
    return redirect('/manage_users')

if __name__ == '__main__':
    app.run(debug=True)
