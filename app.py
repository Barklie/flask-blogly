"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
from sqlalchemy import text
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect('/users')

@app.route("/users")
def list_users():
    """List users and show add form."""

    users = User.query.all()

    return render_template("list.html", users=users)


@app.route("/users/new", methods=['GET', 'POST'])
def new_user():
    """Creates new User through a form."""

    print('above if statement')

    if request.method == 'GET':
        return render_template("new_user.html")
    
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_picture = request.form['profile_picture']

        new_user = User(first_name=first_name, last_name=last_name, profile_picture=profile_picture)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')
    

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.all()

    print(user)
    

    return render_template("user.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edits User Data"""

    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return render_template("edit_user.html", user=user)

    else:
        user = User.query.get_or_404(user_id)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_picture = request.form['profile_picture']

        user.update_user(first_name, last_name, profile_picture)
        db.session.add(user)
        db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes User"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/')

def redirect_posts():
    return redirect('/users/<int:user_id>')
    

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def route_posts(user_id):
    """New User Post"""

    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return render_template("new_post.html", user=user)

    else:
        user = User.query.get_or_404(user_id)
        

        post_title = request.form['post_title']
        post_content = request.form['post_content']

        new_post = Post(post_title=post_title, post_content=post_content, posters_id=user.id)

        db.session.add(new_post)
        db.session.commit()  

        return redirect(f"/users/{user.id}")

@app.route('/posts/<int:post_id>')
def load_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)



@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Edits User Data"""

    del_post = Post.query.get_or_404(post_id)
    db.session.delete(del_post)
    db.session.commit()

    return redirect('/users')

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Edits User Data"""

    if request.method == 'GET':
        post = Post.query.get_or_404(post_id)
        return render_template("edit_post.html", post=post)

    else:
        post = Post.query.get_or_404(post_id)

        post_title = request.form['post_title']
        post_content = request.form['post_content']


        post.update_post(post_title, post_content)
        db.session.add(post)
        db.session.commit()

    return redirect('/users')