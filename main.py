from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['Debug'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

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


if __name__ == "__main__":
    app.run()

