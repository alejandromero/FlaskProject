from app import app, db
import os

if __name__=="__main__":
    db.create_all()

    current_path = os.getcwd()

    for path in ["\\Files", "\\Files\\PublicFiles", "\\Files\\Users"]:
        if os.path.isdir(current_path + path):
            pass
        else:
            os.makedirs(current_path+path)

    app.config["PUBLIC_FILES"] = current_path + "\\Files\\PublicFiles"
    app.config["USERS_FOLDER"] = current_path + "\\Files\\Users"
    app.config["ALLOWED_EXTENSIONS"] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'm4a'])

    del current_path
    app.run()