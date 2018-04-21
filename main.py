from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['Debug'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'anotherkey'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self. password = password

@app.route('/', methods=['POST', 'GET'])
def index():
    blog_posts = Blog.query.all()

    return render_template('build-a-blog.html',title="Building a Blog", blog_posts=blog_posts)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    blog_post = Blog.query.get(blog_id)

    return render_template('blog-entry.html',title="Blog Post", blog_post=blog_post)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    error_title = ""
    error_body = ""
    if request.method == 'GET':
        return render_template('add-entry.html', title="Create New Post")
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if blog_title == "":
            error_title = "Please fill in the title"
        if blog_body == "":
            error_body = "Please fill in the body"
        if error_title == error_body == "":
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id
            return redirect("/blog?id={}".format(blog_id))

        return render_template('add-entry.html', title="Create New Post",
                           error_title=error_title, error_body=error_body,
                           blog_title=blog_title, blog_body=blog_body)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error_user = ''
    error_pass = ''
    error_verify = ''
    error_existing = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_pass = request.form['verify_pass']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is not None:
            error_existing = 'User account already exists'
        for i in username:
            if i == '':
                error_user = "That's not a valid username"
            elif i == ' ':
                error_user = "That's not a valid username"

        if len(username) < 3:
            error_user = "That's not a valid username"

        for i in password:
            if i == '':
                error_pass = "That's not a valid password"
            elif i == ' ':
                error_pass = "That's not a valid password"

        if len(password) < 3:
            error_pass = "That's not a valid password"

        if verify_pass != password or len(verify_pass) < 3:
            error_verify = "Passwords don't match"

        if error_user == error_verify == error_pass == error_existing == '':
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username

            return render_template('add-entry.html', username=username)
        return render_template('signup.html', error_user=error_user, error_pass=error_pass,
                               error_verify=error_verify, error_existing=error_existing, username=username)
    return render_template('signup.html')




if __name__ == "__main__":
    app.run()

