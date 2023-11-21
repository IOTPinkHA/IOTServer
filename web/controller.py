from flask import render_template, Response, request, session, Blueprint
from face_detector import face_detector
from recognition import recognize_faces
Control = Blueprint("Control", __name__)


@Control.route("/")
def index():
    return render_template('index.html')


@Control.route("/home")
def home():
    return render_template('home.html')


@Control.route("/recognize")
def recognize():
    return Response(recognize_faces(), mimetype='multipart/x-mixed-replace; boundary=frame')


@Control.route("/add", methods=["GET", "POST"])
def add():
    input_name = True
    if request.method == "POST":
        input_name = False
        session["userId"] = request.form["userId"]
        return render_template('add.html', input_name=input_name)
    else:
        return render_template('add.html', input_name=input_name)


@Control.route("/add_new_person")
def add_new_person():
    return Response(face_detector(session["userId"]), mimetype='multipart/x-mixed-replace; boundary=frame')
