from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password2@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password






class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))


    def __init__(self, title, body):
        self.title = title
        self.body = body


#@app.before_request
#def require_login():
    #allowed_routes = ['login', 'register']
    #if request.endpoint not in allowed_routes and 'email' not in session:
        #return redirect('/login')

@app.route('/blog')
def main_blog():
    posts = Blog.query.all() 
    return render_template('blog.html', entries=posts)


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

    #    if request.method == 'POST':
#        task_name = request.form['task']
#        new_task = Task(task_name, owner)
#        db.session.add(new_task)
#        db.session.commit()

#    tasks = Task.query.filter_by(completed=False,owner=owner).all()
#    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
#    return render_template('todos.html',title="Get It Done!", 
#        tasks=tasks, completed_tasks=completed_tasks)


@app.route('/blog?id={{id}}')
def bpost_page():
    t = request.args.get('title')
    b = request.args.get('body')




@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        entries = Blog(title, body)

        title_error = ''
        body_error = ''

        if not blank_title(title):
            title_error = "Need a title!"

        if not blank_body(body):
            body_error = "Need blog body!"

        if not title_error and not body_error:
            db.session.add(entries)
            db.session.commit()
                
            entries = Blog.query.all()    

            return render_template('blog.html', entries=entries)   

        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error)



    else:
        #entries = Blog.query.all()
        return render_template('newpost.html')








       #?????????????? user = User.query.filter_by(email=email).first()
        #if user and user.password == password:
        #    session['email'] = email
        #    flash("Logged in")
        #    return redirect('/')
        #else:
         #   flash('User password incorrect, or user does not exist', 'error')

    





#@app.route('/login', methods=['POST', 'GET'])
#def login():
    #if request.method == 'POST':
    #    email = request.form['email']
    #    password = request.form['password']
    #    user = User.query.filter_by(email=email).first()
    #    if user and user.password == password:
    #        session['email'] = email
    #        flash("Logged in")
    #        return redirect('/')
    #    else:
    #        flash('User password incorrect, or user does not exist', 'error')

    #return render_template('login.html')


#@app.route('/register', methods=['POST', 'GET'])
#def register():
#    if request.method == 'POST':
#        email = request.form['email']
#        password = request.form['password']
#        verify = request.form['verify']

        # TODO - validate user's data

#        existing_user = User.query.filter_by(email=email).first()
#        if not existing_user:
#            new_user = User(email, password)
#            db.session.add(new_user)
#            db.session.commit()
#            session['email'] = email
#            return redirect('/')
#        else:
            # TODO - user better response messaging
#            return "<h1>Duplicate user</h1>"

#    return render_template('register.html')

#@app.route('/logout')
#def logout():
#    del session['email']
#    return redirect('/')


#@app.route('/', methods=['POST', 'GET'])
#def index():

#    owner = User.query.filter_by(email=session['email']).first()

#    if request.method == 'POST':
#        task_name = request.form['task']
#        new_task = Task(task_name, owner)
#        db.session.add(new_task)
#        db.session.commit()

#    tasks = Task.query.filter_by(completed=False,owner=owner).all()
#    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
#    return render_template('todos.html',title="Get It Done!", 
#        tasks=tasks, completed_tasks=completed_tasks)


#@app.route('/delete-task', methods=['POST'])
#def delete_task():

#    task_id = int(request.form['task-id'])
#    task = Task.query.get(task_id)
#    task.completed = True
#    db.session.add(task)
#    db.session.commit()

#    return redirect('/')


if __name__ == '__main__':
    app.run()