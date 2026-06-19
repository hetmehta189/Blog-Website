from datetime import datetime
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import json
import math

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_password']
)

mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):

    __tablename__ = 'contacts'

    srno = db.Column(db.Integer, primary_key=True)
    name_of_person = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)

    Date_of_contact = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Posts(db.Model):

    __tablename__ = 'posts'

    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    img_file = db.Column(db.String(255), nullable=True)

    date_of_post = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = len(posts) // params['no_of_posts']

     
    page = math.floor(request.args.get('page', 1, type=int))
    if(not str(page).isnumeric()):
        page=0
    posts = posts[(page-1)*params['no_of_posts']:(page-1)*params['no_of_posts']+params['no_of_posts']]
    
    if page==1:
        prev="#"
        next="/?page="+str(int(page)+1)
    elif page==last:
        prev="/?page="+str(int(page)-1)
        next="#"
    else:
        prev="/?page="+str(int(page)-1)
        next="/?page="+str(int(page)+1)


    return render_template(
        "index.html",
        params=params,
        posts=posts,
        prev=prev,
        next=next
    )


@app.route("/about")
def about():

    return render_template(
        "about.html",
        params=params
    )


@app.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form.get('name_of_person')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')

        entry = Contacts(
            name_of_person=name,
            email=email,
            phone_number=phone_number,
            message=message
        )

        db.session.add(entry)
        db.session.commit()

        mail.send_message(
            'New message from ' + name,
            sender=email,
            recipients=[params['gmail_user']],
            body=message + "\n" + "Contact No. " + phone_number
        )

    return render_template(
        "contact.html",
        params=params
    )


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):

    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template(
        "post.html",
        params=params,
        post=post
    )


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    if 'uname' in session and session['uname'] == params['admin_user']:

        posts = Posts.query.all()

        return render_template(
            "dashboard.html",
            params=params,
            posts=posts
        )

    if request.method == 'POST':

        username = request.form.get('username')
        userpass = request.form.get('password')

        if username == params['admin_user'] and userpass == params['admin_password']:

            session['uname'] = username

            posts = Posts.query.all()

            return render_template(
                "dashboard.html",
                params=params,
                posts=posts
            )

    return render_template(
        "login.html",
        params=params
    )


@app.route("/edit/<string:srno>", methods=['GET', 'POST'])
def edit(srno):

    if 'uname' in session and session['uname'] == params['admin_user']:

        if srno == '0':
            post = None
        else:
            post = Posts.query.filter_by(srno=srno).first()

        if request.method == 'POST':

            title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')

            date_of_post = datetime.now()

            # ADD NEW POST
            if srno == '0':

                post = Posts(
                    title=title,
                    tagline=tagline,
                    slug=slug,
                    content=content,
                    img_file=img_file,
                    date_of_post=date_of_post
                )

                db.session.add(post)
                db.session.commit()

                return redirect('/dashboard')

            # UPDATE EXISTING POST
            else:

                post.title = title
                post.tagline = tagline
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date_of_post = date_of_post

                db.session.commit()

                return redirect('/edit/' + srno)

        return render_template(
            "edit.html",
            params=params,
            post=post,
            srno=srno
        )
    
@app.route("/logout")
def logout():
    session.pop('uname')
    return redirect('/dashboard')

@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if 'uname' in session and session['uname'] == params['admin_user']:
        if request.method == 'POST':
            f = request.files['file']
            f.save(os.path.join(params['upload_location'], secure_filename(f.filename)))
            return "File uploaded successfully"

@app.route("/delete/<string:srno>", methods=['GET'])
def delete(srno):
    if 'uname' in session and session['uname'] == params['admin_user']:
        post = Posts.query.filter_by(srno=srno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')





if __name__ == "__main__":
    app.run(debug=True)