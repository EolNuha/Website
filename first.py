from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.secret_key = "eol"
app.permanent_session_lifetime = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lists.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'eol.nuha22@gmail.com',
	MAIL_PASSWORD = 'haxherja'
	)
mail = Mail(app)
db = SQLAlchemy(app)


class lists(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password


class Order:
    def __init__(self, id, country, city, quantity):
        self.id = id
        self.country = country
        self.city = city
        self.quantity=quantity

orders =[]


@app.route("/order", methods=["POST", "GET"])
def order():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))
    if request.method == "POST":
        country = request.form["country"]
        city = request.form["city"]
        quantity = request.form["quantity"]
        orders.append(Order(id=len(orders) + 1, country=country, city=city, quantity=quantity))
    if request.method == "GET":
        client = session["user"]
        found_user = lists.query.filter_by(name=client).first()
        email = found_user.email
        if len(orders) == 0:
            flash("sban")
        else:
            msg = Message("Pygames with Eol!",
                          sender=email,
                          recipients=["eol.nuha22@gmail.com"])
            msg.body = "Greetings"
            msg.html = render_template('client.html', client=client, orders=orders)
            mail.send(msg)
            orders.clear()
            return render_template("order.html")
    return render_template("order.html", orders=orders )

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
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        session.permanent = True
        found_user = lists.query.filter_by(name=user).first()
        found_user1 = lists.query.filter_by(email=email).first()
        if found_user:
            flash(f"Username unavailable!")
            return redirect(url_for("signup"))
        if found_user1:
            flash(f"Another account has already signed up with this email!")
            return redirect(url_for("signup"))
        usr = lists(user, email, phone, password)
        db.session.add(usr)
        db.session.commit()
        session["user"] = user
        msg = Message("Pygames with Eol!",
                      sender="eol.nuha22@gmail.com",
                      recipients=[email])
        msg.body = "Greetings "+user+"!""\nYour sign up has been successful!\nWelcome to PYGAMES WITH EOL."
        mail.send(msg)
        return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("signup.html")


@app.route("/forgotpassword", methods=["POST", "GET"])
def password():
    if "user" in session:
        return redirect(url_for('home'))
    if request.method == "POST":
        user = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        session.permanent = True
        found_user = lists.query.filter_by(name=user).first()
        if found_user:
            if found_user.email == email:
                if found_user.phone == phone:
                    msg = Message("Pygames with Eol!",
                                  sender="eol.nuha22@gmail.com",
                                  recipients=[email])
                    msg.body = "Greetings " + user + "!"
                    msg.html = render_template('forgot_password.html', user=user, password=found_user.password)
                    mail.send(msg)
                    return render_template("found.html")
                else:
                    flash(f"Wrong phone number!")
            else:
                flash(f"Wrong email!")
        else:
            flash(f"Wrong username!")
    return render_template("password.html")


@app.route("/changepassword", methods=["POST", "GET"])
def change():
    if request.method == "POST":
        user = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        found_user = lists.query.filter_by(name=user).first()
        if found_user:
            if found_user.email == email:
                if found_user.password == password:
                    if not password == password1:
                        if password1 == password2:
                            found_user.password = password2
                            db.session.commit()
                            session["user"] = user
                            return redirect(url_for('home'))
                        else:
                            flash(f"New passwords don't match!")
                    else:
                        flash(f"New password can not be the same as the old one!")
                else:
                    flash(f"Old password is not correct!")
        else:
            flash(f"Account does not exist!")
    return render_template("change.html")


@app.route("/logout")
def logout():
    if "user" in session:
        flash(f"Logged out successful!")
    session.pop("user", None)
    session.pop("password", None)

    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    orders.clear()
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
