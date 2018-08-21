from app import app, db
from app.tables import Users, PublicImages, PrivateImages
from flask import render_template, request, url_for, redirect, flash, session, abort, g
from werkzeug.utils import secure_filename
from os import makedirs
from hashlib import sha256


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.before_request
def before_request():
    try:
        session["user"]
        user = Users.query.filter_by(username = session["user"]).first()
        g.user = user
    except:
        session["user"]=None

@app.errorhandler(404)
def page_not_found(err):
    if session["user"]==None:
        return render_template("page_not_found.html", home_redirect="home"), 404
    else:
        return render_template("page_not_found.html", home_redirect="myfiles"), 404

@app.errorhandler(403)
def forbidden(err):
    if session["user"]==None:
        return render_template("forbidden.html", home_redirect="home"), 403
    else:
        return render_template("forbidden.html", home_redirect="myfiles"), 403

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/publicbrowser')
def publicbrowser():
    return render_template("publicsearch.html")

@app.route('/results')
def results():
    if session["user"]==None:
        filename = request.args.get("filename")
        public_results = PublicImages.query.filter_by(name=str(filename).strip().split(".")[0]).all()
        return render_template("results.html", template_extend="base-index.html", public_results=public_results, public=True ,private=False)
    else:
        public, private = False, False
        public_results, private_results = None, None

        filename = request.args.get("filename")
        if request.args.get("publicSearch")!=None:
            public = True
            public_results = PublicImages.query.filter_by(name=str(filename).strip().split(".")[0]).all()

        if request.args.get("privateSearch") != None:
            private_results = PrivateImages.query.filter_by(name=str(filename).strip().split(".")[0]).all()
            private = True

        return render_template("results.html", template_extend="base-user.html", public_results=public_results, private_results=private_results, public=public, private=private)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            hasehd_password = sha256(request.form["password"].encode('utf-8')).hexdigest()
            new_user = Users(username = username, email=email, password = hasehd_password)
            db.session.add(new_user)
            db.session.commit()
            print("Successful commit")
            makedirs(app.config["USERS_FOLDER"]+"\\"+username)
            print("Successful create the folder")
            flash("Successful registered, login now!", "success")
            return redirect(url_for("login"))
        except:
            flash("Something went wrong, try again", "error")
    return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user:
            pass
        else:
            user = Users.query.filter_by(email=request.form["username"]).first()

        if user and user.password == sha256(request.form["password"].encode('utf-8')).hexdigest():
            session["user"] = user.username
            return redirect(url_for("myfiles"))
        else:
            flash("Check you're password and try again", "error")
    return render_template("login.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/myfiles')
def myfiles():
    if session["user"]:
        user_public_images = PublicImages.query.filter_by(owner_id=g.user.id).all()
        user_private_images = PrivateImages.query.filter_by(owner_id=g.user.id).all()
        return render_template("user-files.html", public_files = user_public_images, private_files = user_private_images)
    else:
        abort(403)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if session["user"]:
        if request.method=="POST":
            if not "file" in request.files:
                flash("No file part in the form.","error")
                return redirect(url_for("upload"))
            f = request.files["file"]
            if f.filename == "":
                flash("No file selected.", "error")
                return redirect(url_for("upload"))
            if f and allowed_file(f.filename):
                f = request.files["file"]
                filename = secure_filename(f.filename)
                name, extension = str(filename).strip().split(".")
                if request.form.get('publicUpload')!=None:
                    f.save(app.config["PUBLIC_FILES"]+'\\'+filename)
                    new_public_file = PublicImages(name = name, extension = extension, owner_id = g.user.id)
                    db.session.add(new_public_file)
                    db.session.commit()
                if request.form.get('privateUpload')!=None:
                    f.save(app.config["USERS_FOLDER"]+"\\"+session["user"]+'\\'+ filename)
                    new_private_file = PrivateImages(name = name, extension = extension, owner_id = g.user.id)
                    db.session.add(new_private_file)
                    db.session.commit()
                flash("The file was uploaded successfully","success")
                return redirect(url_for("myfiles"))
        return render_template("user-upload.html")
    else:
        abort(403)

@app.route('/search')
def search():
    if session["user"]:
        return render_template("user-search.html")
    else:
        abort(403)

@app.route('/settings', methods=['GET','POST'])
def settings():
    if session["user"]:
        return render_template("user-settings.html")
    else:
        abort(403)

@app.route('/logout')
def logout():
    if session["user"]:
        session["user"]=None
        return redirect(url_for("login"))
    else:
        abort(403)

#request.args.get("something") use for GET ?
#request.form["something"] use for POST?