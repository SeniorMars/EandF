# Team E and F (Karl Hernandez, Eric Lo, Amelia Chin, Ari Schechter)
# SoftDev
# P0: Da Art of Storytellin' / blog project
# 2020-12-12
from flask import Flask, render_template, request, session
import os
app = Flask(__name__)
app.secret_key = os.urandom(32)  # random 32 bit key

#check if alr logged in
@app.route("/")
def home():
    if 'username' in session: #<username> dpdt on form submission args
        return render_template() #dpdt on home.html
    return render_template() #dpdt on login.html

#login func
#the register button should be in the login template but not in the fxn to redirect to register
@app.route("/loginForm", methods=['POST']) #takes info from the login form
def login():
    tempUser = request.form['username'] #<username> & <password> dpdt on form args
    tempPass = request.form['password']
    if True: #dpdt on DB methods to match user and pass
        session['username'] = tempUser
        session['password'] = tempUser
        return render_template() #dpdt on home.html

    # vague error
    return render_template() #dpdt on error.html

#register func
@app.route("/register") #this route should be callable on login.html
def register():
    return render_template() #dpdt on register.html

#take you to home page after creating account
@app.route("/registerForm", methods=['POST'])
def registerRedirect():
    tempUser = request.form['username'] #<username> & <password> dpdt on form args
    tempPass = request.form['password']
    #<SOME CODE> dpdt on DB methods to add user and pass into DB
    return render_template() #dpdt on home.html

#logout func
@app.route("/logout")
def logout():
    session.pop('username') #<username> & <password> dpdt on form args
    session.pop('password')
    return render_template() #dpdt on login.html

#create blog func 
@app.route("/createBlogForm", methods=['POST'])
def createBlog():
    #<SOME CODE> dpdt on blog creation form and types of info users put in
    return render_template() #dpdt on blog.html and the info asked from form

#edit and add blog func
#<TBD>

#delete blog entry func
@app.route("/delete") #might need a delete form on yourBlog.html that records if user clicks a delete button
def deleteEntry():
    #<SOME CODE> dpdt on DB method to pop the entry fron the blog
    return render_template() #dpdt on yourBlog.html

#view profiles
@app.route("/profiles")
def profiles():
    #<SOME CODE> dpdt on DB method to fetch user data
    return render_template() #dpdt on profile.html

#view your blog, has editing perms
@app.route("/yourBlog")
def viewYourBlog():
    #<SOME CODE> dpdt on DB method to fetch blog data
    return render_template() #dpdt on yourBlog.html

#view other blogs, no editing perms
@app.route("/blog")
def viewBlog():
    #<SOME CODE> dpdt on DB method to fetch blog data
    return render_template() #dpdt on blog.html

"""
import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
"""