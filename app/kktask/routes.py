import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from kktask import app, db, bcrypt
from kktask.forms import RegistrationForm, LoginForm , UpdateAccountForm
from kktask.models import User
from flask_login import login_user, current_user, logout_user, login_required




@app.route("/")
@app.route("/home")
def home():
    myUser = User.query.all()
    return render_template('home.html' , myUser=myUser)


@app.route("/register" , methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_home('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hashing for security reasons
        user = User(username=form.username.data,registration_number=form.registartion_number.data,email=form.email.data,age=form.age.data,gender=form.gender.data, address=form.address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can login to update/delete account', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account" ,  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
         if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
         current_user.email = form.email.data
         current_user.age = form.age.data
         current_user.address = form.address.data
         db.session.commit()
         flash('Your account has been updated!', 'success')
         return redirect(url_for('account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.address.data = current_user.address
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file , form=form)

@app.route("/Delete Acoount")
def delete():

    delete = User.query.filter_by(username=current_user.username).first()
    db.session.delete(delete)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))
