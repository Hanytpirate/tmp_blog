import os
import secrets
from PIL import Image

from flask import render_template,url_for,flash,redirect,request, abort,jsonify
from flask_blog.forms import RegistrationForm,LoginForm,UpdateAccountForm, PostForm
from flask_blog import app,db,bcrypt
from flask_blog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from markdown import markdown
from markupsafe import Markup
@app.route("/")
def home():
    posts = Post.query.all()
    for post in posts:
        post.content = md_to_html(post.content)
    return render_template('home.html',posts=posts)
def md_to_html(md):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']
    html = markdown(md,extensions=exts)
    content = Markup(html)
    return content
@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"账号:{form.username.data}创建成功!您现在可以登录了","success")
        return redirect(url_for('login'))
    return render_template('register.html',title='注册',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("登录失败!请检查邮箱和密码.")
    return render_template('login.html',title='登录',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static',"img","avatar", picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    if i.size[0] > i.size[1]:
        i = i.crop([(i.size[0]-i.size[1])//2,0,(i.size[0]-i.size[1])//2+i.size[1],i.size[1]])
    if i.size[0] < i.size[1]:
        i = i.crop([(i.size[1]-i.size[0])//2,0,(i.size[1]-i.size[0])//2+i.size[0],i.size[0]])
    i.thumbnail(output_size)
    print(i.size)
    i.save(picture_path)

    return picture_fn
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static",filename="profile_pics/%s" % current_user.image_file)
    return render_template('account.html',title='账户空间',image_file=image_file,form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    title = request.form.get('article_title')
    content = request.form.get('article-content')
    if title != None and content != None:
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html')
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post.content = md_to_html(post.content)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    if request.args.get('have')=="true":
        return jsonify({'title':post.title,'content':post.content})
    title = request.form.get('article_title')
    content = request.form.get('article-content')
    if title != None and content != None:
        post.title = title
        post.content = content
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('create_post.html', title='更新文章')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))