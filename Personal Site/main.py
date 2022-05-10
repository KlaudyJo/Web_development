from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CREATE TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# db.create_all()


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('The email does not exist')
            return redirect (url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Incorrect password')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('aboutme'))
    return render_template('Login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('You have already signed up! Please log in!')
            return redirect(url_for('login'))
        hash_salted_password = generate_password_hash(request.form.get('password'),method='pbkdf2:sha256',salt_length=8 )
        new_user = User(
            email = request.form.get('email'),
            name = request.form.get('name'),
            password = hash_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('login'))
    
    return render_template("Signin.html")


@app.route('/loader')
def loader():
    return render_template("loader.html")



@app.route('/aboutme')
@login_required
def aboutme():
    return render_template("aboutme.html", name= current_user.name)


@app.route('/contact')
@login_required
def contact_me():
    print(current_user.name)
    return render_template("Contact.html", name=current_user.name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/blog')
@login_required
def blog():
    return render_template("blog.html", name= current_user.name)


if __name__ == '__main__':
    app.run(debug=True)


