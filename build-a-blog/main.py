from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password2@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))


    def __init__(self, title, body):
        self.title = title
        self.body = body




@app.route('/blog')
def main_blog():
    posts = Blog.query.all() 
    val = request.args.get('id')
    try:
        if val.isdigit() == True:
            entry = Blog.query.filter_by(id=val).first()
            return render_template('single_post.html', entry=entry)
    except:

        return render_template('blog.html', entries=posts)



#@app.route('/blog?id={{entry.id}}')
#def bpost_page():
    #info = Blog.query.filter_by(id='{{entry.id}}').first()
    #t = info.title
    #b = info.body
    
    #return render_template('register.html', entry=entry)   


def blank_title(title):
    if title == "":
        return False
    else:
        return True

def blank_body(body):
    if body == "":
        return False
    else:
        return True




@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        entry = Blog(title, body)

        title_error = ''
        body_error = ''

        if not blank_title(title):
            title_error = "Need a title!"

        if not blank_body(body):
            body_error = "Need blog body!"

        if not title_error and not body_error:
            db.session.add(entry)
            db.session.commit()
            

            x = str(entry.id)
        
            return redirect('/blog?id=' + x)


        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error)


    else:
        return render_template('newpost.html')




if __name__ == '__main__':
    app.run()