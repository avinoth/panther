from flask import render_template, flash, redirect, session, url_for, request, g, Flask, abort
from flask.ext.sqlalchemy import SQLAlchemy
from models import User, Post, db, Comment
import os
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from config import basedir
import datetime

#app configuration settings
app = Flask(__name__)
app.config.from_object('config')


#Flask-Login configuration settings
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/register', methods = ['GET', 'POST'])

def register():
    if request.method == 'GET':
        return render_template('register.html',
                                user = "Vinoth")
    user = User(name=request.form['name'] , email=request.form['email'], password=request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email,password=password).first()
    if registered_user is None:
        flash('Email or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('manage'))

@app.route('/manage')
@login_required
def manage():
    return render_template("manage.html",
    posts = Post.query.filter_by(user_id = g.user.id).order_by(Post.timestamp.desc()).all())

@app.route('/feed/<name>')
def feed(name):
    user = User.query.filter_by(name = name).first()
    return render_template("feed.html",
    posts = Post.query.filter_by(user_id = user.id).order_by(Post.timestamp.desc()).all())

@app.route('/feed/<int:pid>', methods=['GET', 'POST'])
@login_required
def blogpost(pid):
    post = Post.query.filter_by(id = pid).first()
    if request.method == 'POST':
        comment = Comment(content=request.form['comment'], parentpost=post, commenter = g.user)
        db.session.add(comment)
        db.session.commit()
    return render_template("blogpost.html",
                           post = post,
                           comments = Comment.query.filter_by(post_id = post.id).all())

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.filter_by(id = id).first()
    if post.author.id == g.user.id:
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted")
        return redirect(url_for('manage'))
    flash("You are not authorised to delete this post")
    return redirect(url_for('manage'))


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Enter a title', 'error')
        elif not request.form['body']:
            flash('Content cannot be empty', 'error')
        else:
            post = Post(title=request.form['title'], body=request.form['body'], timestamp=datetime.datetime.now().date(),
                        author = g.user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('manage'))
    return render_template('newpost.html',
                           form = form)


@app.route('/edit/<int:pid>', methods = ['GET', 'POST'])
@login_required
def edit(pid):
    post = Post.query.filter_by(id = pid).first()
    if request.method == 'POST':
        if post.author.id == g.user.id:
            post.title = request.form['title']
            post.body = request.form['body']
            post.timestamp = datetime.datetime.now().date()
            db.session.add(post)
            db.session.commit()
            flash("Post has been successfully updated")
            return redirect(url_for('manage'))
        else:
            flash("You are not authorized to edit this post")
            return redirect(url_for('manage'))
        
    return render_template("edit.html",
                           post = post)
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

