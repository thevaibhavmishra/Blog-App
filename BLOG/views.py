from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, login_user, current_user, logout_user
from .models import User, Blog
from . import db

views = Blueprint('views', __name__)


@views.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':       # checking if the method type is post
        name = request.form.get('name')     #accessing the name from the from data
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        if password != confirmpassword: # comparing the password and confirm password
            flash('password and confirm password does not match', category='error')
        else:
            new_user = User(full_name=name, email=email, password=password)
            db.session.add(new_user)  # adding the new user to database
            db.session.commit()
            login_user(new_user)  # logging the user
            flash('Account created', category='success')
            return redirect(url_for('views.home'))  # redirecting the user to home view

    return render_template('signup.html')   # redering the signup page



@views.route('/login', methods = ['GET', 'POST'])   
def login():
    if request.method == 'POST':  #checking if the method is POST
        email = request.form.get('email')  # getting the email and 
        password = request.form.get('password') # password from form data
        user = User.query.filter_by(email=email).first() # finding the user with 
        if user and user.password == password:  # given email and matching password
                flash('Logged In Successfully', category="success")
                login_user(user)    #logging in the user 
        else:
            flash('Incorrect Credentials', category="error")

    return render_template('login.html')#if the method is 'GET' return the login page


@views.route('/logout')
@login_required
def logout():
    logout_user()   # function to log out the current_user
    return redirect(url_for('views.login')) #redirect to login view


@views.route('/')
@login_required     #this decorator will make the URL private 
def home():
    blogs = Blog.query.all() #querying all the blogs in database
    for blog in blogs:  # iterating through all the blogs
        user = User.query.filter_by(id=blog.user_id).first()
        if user:
            blog.author = user.email # assigning the user email as
        else:                   # the blog's author
            blog.author = "Someone"

    return render_template('home.html', blogs = blogs) # passing all 
                # the blogs as data to the home template 


@views.route('/createblog', methods = ['POST', 'GET'] )
@login_required     # decorator to allow only logged in user to acces the route
def createblog():
    if request.method == 'POST': # checking, if the method is POST
        title = request.form.get('title')  # Getting the title from user form
        content = request.form.get('content') # Getting the content from user form
        if len(title) <= 0:     
            flash('Blog must have a Title', category='error')
        elif len(content) <= 5:
            flash('Blog must have a adequate content', category='error')
        else:
            new_blog = Blog(title = title, data = content, user_id = current_user.id )
            db.session.add(new_blog)    # adding the new blog to our database
            db.session.commit()
            flash('Blog Created', category='success')   # Flashing the success message
            return redirect(url_for('views.createblog'))# redirecting to the create view URL

    return render_template('createblog.html')#rendering the createblog template for GET request