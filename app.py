"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
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
        tags = Tag.query.all()
        return render_template("new_post.html", user=user, tags=tags)

    else:
        user = User.query.get_or_404(user_id)

        post_title = request.form['post_title']
        post_content = request.form['post_content']

        # tag_name = request.form['Happy']
        print("YELLOOOOOOOOW")
       

        new_post = Post(post_title=post_title, post_content=post_content, posters_id=user.id)


 
        db.session.add(new_post)
        db.session.commit()  
        db.session.refresh(new_post)  

        for key, elm in request.form.items():

            if key.startswith('tag.'):
                new_post_tag = PostTag(post_id=new_post.id, tag_id=elm)
                db.session.add(new_post_tag)


        db.session.commit()
        

        return redirect(f"/users/{user.id}")

@app.route('/posts/<int:post_id>')
def load_post(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    post_tags = PostTag.query.all()

    return render_template('post.html', post=post, tags=tags, post_tags=post_tags)



@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete's User Post"""

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
        db.sessions.refresh(post)

        for key, elm in request.form.items():

            if key.startswith('tag.'):
                new_post_tag = PostTag(post_id=post.id, tag_id=elm)
                db.session.add(new_post_tag)


        db.session.commit()

        db.session.commit()

    return redirect('/users')


@app.route('/tags')
def get_tags():
    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)


@app.route('/tags/new', methods=["GET", "POST"])
def new_tag():
        if request.method == 'GET':
            return render_template('new_tag.html')
        else:
            tag_name = request.form['tag_name']

            new_tag = Tag(name=tag_name)
            db.session.add(new_tag)
            db.session.commit()

            return redirect('/users')
        
@app.route('/tags/<int:tag_id>')
def tagged_posts(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    tags = Tag.query.all()
    post_tags = PostTag.query.all()
    

    # tag_posts =


    return render_template('tag.html', tag=tag, tags=tags, posts=posts, post_tags=post_tags)

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
 
    db.session.delete(tag)
    db.session.commit()
