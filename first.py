from flask import Flask, render_template, request, session, redirect, url_for, g, flash
from datetime import timedelta


class user:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(user(id=1, username='eoli', password='kosova22'))
users.append(user(id=2, username='ledri', password='ledri123'))

app = Flask(__name__)
app.secret_key = 'eolnuha'
app.permanent_session_lifetime = timedelta(days=7)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user1 = [x for x in users if x.username == username]
        if not user1:
            flash(f"Wrong username!")
            return render_template('login.html')

        user = [x for x in users if x.username == username][0]

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        flash(f"Wrong password!")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['usr']
        password = request.form['psw']
        users.append(user(id=len(users) + 1, username=username, password=password))
        flash(f"Please enter the username and password again!")
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route("/logout")
def logout():
    if g.user:
        flash(f"Logged out successful!")
    session.pop('user_id', None)

    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/spaceinvaders")
def space():
    if not g.user:
        flash(f"Please login!")
        return redirect(url_for('login'))
    return render_template('Spaceinvaders.html')


@app.route("/dinogame")
def dino():
    if not g.user:
        flash(f"Please login!")
        return redirect(url_for('login'))
    return render_template('dino.html')


@app.route("/towerwar")
def tower():
    if not g.user:
        flash(f"Please login!")
        return redirect(url_for('login'))
    return render_template('tower.html')


@app.route("/supermario")
def mario():
    if not g.user:
        flash(f"Please login!")
        return redirect(url_for('login'))
    return render_template('mario.html')


@app.route("/snakegame")
def snake():
    if not g.user:
        flash(f"Please login!")
        return redirect(url_for('login'))
    return render_template('snake.html')


@app.route("/sourcecode")
def source():
    if not g.user:
        flash(f"Please login!")
        return redirect(url_for('login'))
    return render_template('source.html')


if __name__ == "__main__":
    app.run(debug=True)
