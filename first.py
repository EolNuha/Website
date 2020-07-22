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
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='eol.nuha22@gmail.com',
    MAIL_PASSWORD='haxherja'
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
    def __init__(self, id, category, product, quantity, price):
        self.id = id
        self.category = category
        self.product = product
        self.quantity = quantity
        self.price = price


orders = []
prices = [0]
if len(orders) == 0:
    prices.clear()

@app.route("/order", methods=["POST", "GET"])
def order():
    if not "user" in session:
        flash(f"Please log in!")
        return redirect(url_for('login'))

    else:
        if request.method == "POST":
            for item in orders:
                if "remove" + str(item.id) in request.form:
                    remove = orders.index(item)
                    orders.pop(remove)
                    prices.pop(remove)


            if 'submit1' in request.form:
                if not len(orders) == 0:
                    orders.clear()
                    prices.clear()
                    return redirect(url_for("order"))



            elif 'submit' in request.form:
                category = request.form["category"]
                product = request.form["product"]
                quantity = request.form["quantity"]
                if product == "Qipsa":
                    price = int(quantity) * 1
                elif product == "Smoka":
                    price = int(quantity) * 0.5
                elif product == "Torte":
                    price = int(quantity) * 1.1
                elif product == "Perime":
                    price = int(quantity) * 0.7
                elif product == "Coca-Cola":
                    price = int(quantity) * 1.4
                elif product == "Fanta":
                    price = int(quantity) * 1.4
                elif product == "Pepsi":
                    price = int(quantity) * 1.4
                elif product == "Sprite":
                    price = int(quantity) * 1.4
                elif product == "Ice-Tea":
                    price = int(quantity) * 1
                elif product == "Paloma-Banjo":
                    price = int(quantity) * 1.2
                elif product == "Domestos":
                    price = int(quantity) * 2
                elif product == "Sapun i Lengshem":
                    price = int(quantity) * 1.8
                else:
                    price = int(quantity) * 2.2
                orders.append(
                    Order(id=len(orders) + 1, category=category, product=product, quantity=int(quantity),
                          price=("%.2f" % round(price, 2))))
                prices.append(price)

            elif 'order' in request.form:
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
                    msg.html = render_template('client.html', client=client, orders=orders,
                                               total=("%.2f" % round(sum(prices), 2)))
                    mail.send(msg)
                    orders.clear()
                    prices.clear()
        return render_template("order.html", orders=orders, prices=prices, total=("%.2f" % round(sum(prices), 2)))


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
        msg.body = "Greetings " + user + "!""\nYour sign up has been successful!\nWelcome to PYGAMES WITH EOL."
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
    prices.clear()
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
