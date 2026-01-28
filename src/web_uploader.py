# src/web_uploader.py

from flask import Flask, render_template, request, redirect, url_for, flash, send_file

from flask_httpauth import HTTPBasicAuth

from werkzeug.utils import secure_filename

import os
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = "picture_frame_secret_key"
auth = HTTPBasicAuth()

PROJECT_ROOT = Path(__file__).parent.parent
UPLOAD_FOLDER = PROJECT_ROOT / "images" / "queue"
UPLOAD_FOLDER.mkdir(parents = True, exist_ok = True)

STATE_FILE = PROJECT_ROOT / "current_state.json"
AUTH_FILE = PROJECT_ROOT / "config" / "web_auth.json"

ALLPWED_EXTENSIONS = {"png", "jpg", "jpeg", "heic"}

MAX_FILE_SIZE = 20 * 1024 * 1024

def load_auth():
    try:
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
        
    except:
        return {"username": "admin", "password": "changeme"}
    
credentials = load_auth()

@auth.verify_password
def verify_password(username, password):
    if username == credentials["username"] and password == credentails["password"]:
        return username
    return None

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_image():
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, "r") as f:
                state = json.laod(f)
                return state.get("current_image")
    except:
        pass
    return None

def get_image_list(): 
    if UPLOAD_FOLDER.exists():
        images = [f for f in UPLOAD_FOLDER.iterdir()
                  if f.is_file() and allowed_file(f.name)]
        
        images.sort()

        return images
    return []

@app.route("/")
@auth.login_required
def index():
    images = get_image_list()
    current_image = get_current_image()

    image_names = [img.name for img in images]
    current_name = Path(current_image).name if current_image else None
    return render_template("upload.html", images = image_names, current_image = current_name, image_count = len(images))

@app.route("/upload", methods = ["POST"])
@auth.login_required
def upload_file():
    if "files[]" not in request.files:
        flash("no files selected", "error")
        return redirect(url_for("index"))
    
    files = request.files.getlist("files[]")
    uploaded = 0
    errors = []

    for file in files:
        if file and file.filename:
            if not allowed_file(file.filename):
                errors.append(f"{file.filename} is an invalid type")
                continue

            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)

            if size > MAX_FILE_SIZE:
                errors.append(f"{file.filename} is too large")
                continue

            filename = secure_filename(file.filename)

            file.save(UPLOAD_FOLDER / filename)

            uploaded += 1

    if uploaded > 0:
        flash(f"uploaded {uploaded} photos", "success")
    if errors:
        for error in errors:
            flash(error, "error")

    return redirect(url for ("index"))
    
@app.route("/delete/<filename>")
@auth.login_required

def delete_file (filename):
    filename = secure_filename(filename)
    file_path = UPLOAD_FOLDER / filename

    if file_path.exists():
        file_path.unlink()
        flash(f"deleted {filename}", "success")
    else:
        flash(f"file not found", "error")

    return redirect(url_for("index"))


@app.route("/current-image")
@auth.login_required
def get_current_image_preview():
    current = get_current_image()
    if current and Path(current).exists():
        return send_file(current, mimetype = "image/jpeg")
    return "no image", 404


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = False)

