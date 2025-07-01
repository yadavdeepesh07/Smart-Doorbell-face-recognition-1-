from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from app.config import get_config, update_config
from app.aws_rekognition import index_face, list_faces, delete_face
import os
import json
import csv
import cv2
from io import StringIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['UPLOAD_FOLDER'] = "static/uploads"
os.makedirs(app.config['UPLOAD_FOLDER'] , exist_ok=True)

@app.route("/")
def index():
    log = []
    if os.path.exists("logs/visitor_log.json"):
        with open("logs/visitor_log.json") as f:
            logs = json.load(f)
    return render_template("index.html",logs=logs)

@app.route("/privacy", methods=["GET", "POST"])
def privacy():
    if request.method == "POST":
        enable_feed = request.form.get("live_feed") == "on"
        enable_recognition = request.form.get("recognition") == "on"
        update_config("ENABLE_LIVE_FEED", enable_feed)
        update_config("ENABLE_RECOGNITION", enable_recognition)
        return redirect(url_for("privacy"))

    return render_template("privacy.html",
        live_feed=get_config("ENABLE_LIVE_FEED", True),
        recognition=get_config("ENABLE_RECOGNITION", True))

@app.route("/visitors", methods=["GET", "POST"])
def visitors():
    log_path = "logs/visitor_log.json"
    logs = []

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
                print("🔎 Logs loaded:", logs)
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
                logs = []

    if request.method == "POST":
        search_name = request.form.get("search_name", "").strip().lower()
        search_date = request.form.get("search_date", "").strip()
        filtered_logs = []
        for entry in logs:
            name_match = search_name in entry["name"].lower() if search_name else True
            date_match = search_date in entry["timestamp"] if search_date else True
            if name_match and date_match:
                filtered_logs.append(entry)
        print("Filtered logs:", filtered_logs)
        return render_template("visitors.html", logs=filtered_logs)

    print("All logs passed to template:", logs)
    return render_template("visitors.html", logs=logs)

@app.route("/export_visitors")
def export_visitors():
    log_path = "logs/visitor_log.json"
    if not os.path.exists(log_path):
        return "Log file not found", 404

    with open(log_path, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return "Log file is corrupted", 500

    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Name", "Confidence", "Timestamp", "Snapshot Path"])

    for entry in logs:
        writer.writerow([
            entry.get("name", ""),
            entry.get("confidence", ""),
            entry.get("timestamp", ""),
            entry.get("image_path", "")
        ])

    csv_buffer.seek(0)
    return send_file(
        csv_buffer,
        mimetype='text/csv',
        download_name="visitor_log.csv",
        as_attachment=True
    )

@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        image = request.files.get("image")

        if not name or not image:
            flash("Name and image are required.", "danger")
            return redirect(url_for("manage_users"))

        filename = secure_filename(f"{name}.jpg")
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)

        try:
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) == 0:
                os.remove(path)
                flash("No face detected in the image. Please upload a clear front-facing photo.", "danger")
                return redirect(url_for("manage_users"))
        except Exception as e:
            flash(f"⚠️ Face detection failed: {e}", "warning")

        with open(path, "rb") as f:
            success = index_face(f.read(), name)

        if success:
            flash(f"{name} added to face collection.", "success")
        else:
            os.remove(path)
            flash("AWS Rekognition could not index the face. Try another image.", "danger")

        return redirect(url_for("manage_users"))

    faces = list_faces()
    return render_template("manage_users.html", faces=faces)

@app.route("/delete_user/<face_id>")
def delete_user(face_id):
    if delete_face(face_id):
        flash("Face deleted successfully.", "success")
    else:
        flash("Failed to delete face.", "danger")
    return redirect(url_for("manage_users"))

@app.route("/export_users")
def export_users():
    faces = list_faces()
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Face ID", "ExternalImageId", "Confidence", "Timestamp"])

    for face in faces:
        writer.writerow([
            face.get("FaceId", ""),
            face.get("ExternalImageId", ""),
            face.get("Confidence", "N/A"),
            face.get("CreationTimestamp", "")
        ])

    csv_buffer.seek(0)
    return send_file(
        csv_buffer,
        mimetype='text/csv',
        download_name="registered_users.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
