from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "eol"
app.permanent_session_lifetime = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lists.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class lists(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password


@app.route("/view")
def view():
    return render_template("view.html", values=lists.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        found_user = lists.query.filter_by(name=user).first()
        if found_user:
            password = request.form["password"]
            if found_user.password == password:
                session["user"] = user
                return redirect(url_for("home"))
            else:
                flash(f"Wrong password!")
                return redirect(url_for("login"))

        else:
            flash(f"Wrong username!")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        user = request.form["name"]
        password = request.form["password"]
        session.permanent = True
        found_user = lists.query.filter_by(name=user).first()
        if found_user:
            flash(f"Username unavailable!")
            return redirect(url_for("signup"))
        usr = lists(user, password)
        db.session.add(usr)
        db.session.commit()
        flash("Signed up successful. Please enter the username and password again!")
        return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("signup.html")


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Logged out successful!")
    session.pop("user", None)
    session.pop("password", None)

    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/spaceinvaders")
def space():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    return render_template('Spaceinvaders.html')


@app.route("/dinogame")
def dino():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    return render_template('dino.html')


@app.route("/towerwar")
def tower():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    return render_template('tower.html')


@app.route("/supermario")
def mario():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    return render_template('mario.html')


@app.route("/snakegame")
def snake():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    return render_template('snake.html')


@app.route("/sourcecode")
def source():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    return render_template('source.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
