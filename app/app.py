# Team E and F (Karl Hernandez, Eric Lo, Amelia Chin, Ari Schechter)
# SoftDev
# P0: Da Art of Storytellin' / blog project
# 2020-12-12
# from db_manager import checkLogin, createTables, getUserId, registerUser
# import db_manager
from flask import Flask, render_template, request, session, redirect
import os
from db_manager import *
app = Flask(__name__)
app.secret_key = os.urandom(32)  # random 32 bit key


createTables()

# check if alr logged in


@app.route("/")
def home():
    if 'username' in session:  # <username> dpdt on form submission args
        return redirect("/home")  # dpdt on home.html

    return render_template("login.html")  # dpdt on login.html

# login func
# the register button should be in the login template but not in the fxn to redirect to register


@app.route("/loginRead", methods=['POST'])  # takes info from the login form
def login():
    # <username> & <password> dpdt on form args
    tempUser = request.form['username']
    tempPass = request.form['password']
    loginS, issue, user_id = checkLogin(tempUser, tempPass)
    if loginS:  # dpdt on DB methods to match user and pass
        session['username'] = tempUser
        session['password'] = tempPass
        session['user_id'] = user_id
        return redirect("/home")  # dpdt on home.html

    # we will pass issue as an argument
    # vague error
    return render_template("error.html", error=issue)  # dpdt on error.html

# register func


@app.route("/register")  # this route should be callable on login.html
def register():
    return render_template("register.html")  # dpdt on register.html

# take you to home page after creating account


@app.route("/registerRead", methods=['POST'])
def registerRedirect():
    # <username> & <password> dpdt on form args
    tempUser = request.form['username']
    tempPass = request.form['password']
    registerUser(tempUser, tempPass)
    return render_template("registersuccess.html")  # dpdt on home.html


# logout func
@app.route("/logout")
def logout():
    session.pop('username')  # <username> & <password> dpdt on form args
    session.pop('password')
    return redirect("/")  # dpdt on login.html


@app.route("/home")
def homePage():
    ids = getAllUsers()
    names = []
    for _id in ids:
        names.append(getUsername(_id))

    # createBlog(1, 'ddd', "test", "1/6/2021", "this is a test")

    blog_info = []
    for _id in ids:
        for blog_id in getUserBlogs(_id):
            blog_info.append(list(getBlogBasic(blog_id)))

    return render_template("home.html", names=names, blog_info=blog_info)

    # return render_template("home.html", names=names)


# create blog func
@app.route("/createBlog")
def createBlogPage():
    return render_template("createBlogForm.html")  # createBlogForm.html


@app.route("/createBlogRead", methods=['POST'])
def createBlogForm():
    bT = request.form['blogTitle']
    dC = request.form['dateCreated']
    bB = request.form['blogBio']
    createBlog(session['user_id'], session['username'], bT, dC, bB)
    return redirect("/home")


"""
#edit and add blog func
#<TBD>

# #delete blog entry func
# @app.route("/delete") #might need a delete form on yourBlog.html that records if user clicks a delete button
# def deleteEntry():
#     #<SOME CODE> dpdt on DB method to pop the entry fron the blog
#     return render_template() #dpdt on yourBlog.html

# add blog entry func
@app.route("/addEntry")
def addBlogEntry():
    pass

#view profile
@app.route("/profile")
def profile():
    #Eventually add in the ability to reference any user id
    
    blogs = getUserBlogs(session['user_id'])
    for blog in blogs:
        blog_title, blog_bio, date_created = getBlogBasic(blog)
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


if __name__ == "__main__":
    app.debug = True
    app.run()


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
