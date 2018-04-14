from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['Debug'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
        blog_posts = Blog.query.all()

    #if request.method == 'POST':

        return render_template('build-a-blog.html',title="Building a Blog", blog_posts=blog_posts)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_posts = Blog.query.all()

    return render_template('build-a-blog.html',title="Building a Blog", blog_posts=blog_posts)

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
            return redirect("/")

        return render_template('add-entry.html', title="Create New Post",
                           error_title=error_title, error_body=error_body,
                           blog_title=blog_title, blog_body=blog_body)





if __name__ == "__main__":
    app.run()

