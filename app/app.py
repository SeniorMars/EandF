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
    users = []
    for _id in getAllUsers():
        users.append(getUsername(_id))
    if tempUser in users:
        return render_template("error.html", error="Username already exists")
    tempPass = request.form['password']
    registerUser(tempUser, tempPass)
    return redirect("/")  # dpdt on home.html


# logout func
@app.route("/logout")
def logout():
    session.pop('username')  # <username> & <password> dpdt on form args
    session.pop('password')
    session.pop('blog_id')
    return redirect("/")  # dpdt on login.html


@app.route("/home")
def homePage():
    ids = getAllUsers()
    names = []
    for _id in ids:
        names.append(getUsername(_id))

    # createBlog(1, 'ddd', "test4", "1/6/2021", "this is a test")

    blog_info = []
    for _id in ids:
        for blog_id in getUserBlogs(_id):
            blog_info.append(list(getBlogBasic(blog_id)))

    mid = len(blog_info) // 2
    return render_template("home.html", names=names,
                           blog_info_part1=blog_info[:mid],
                           blog_info_part2=blog_info[mid:])

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
    if bT == "" or dC == "" or bB == "":
        # fix later by changing button to return to home
        return render_template("blogError.html", error="You need to fill all three fields")

    createBlog(session['user_id'], session['username'], bT, dC, bB)
    return redirect("/home")

    # return render_template("successBlog.html") #dpdt on blog.html and the info asked from form


# add blog entry func
@app.route("/addEntry")
def addBlogEntry():
    return render_template("addEntryForm.html")


@app.route("/addEntryRead", methods=['POST'])
def addEntryRead():
    entry_title = request.form['entryTitle']
    date_created = request.form['dateCreated']
    entry_content = request.form['entryContent']
    if entry_content == "" or date_created == "" or entry_content == "":
        return render_template('entryError.html', error="You need to fill all three fields")
    blog_id = session['blog_id']

    createEntry(blog_id, session['username'],
                entry_title, entry_content, date_created)

    return redirect("/home")


# view profile
@app.route("/profile")
def profile():
    user = request.args.get('user')
    blogs = getUserBlogs(user)
    blog_info = []

    for blog_id in blogs:
        blog_info.append(list(getBlogBasic(blog_id)))

    return render_template("profile.html", username=user, length=len(blog_info), blog_info=blog_info)


# view your blog, has editing perms


@app.route("/yourBlog")
def viewYourBlog():
    blog_id = request.args.get('blog_num')
    session['blog_id'] = blog_id
    title, bio, date, _id = getBlogBasic(blog_id)

    entry_info = []
    for entry_id in getBlogEntries(blog_id):
        entry_info.append(list(getEntryInfo(entry_id)))

    return render_template("yourBlog.html", username=session['username'], entry_info=entry_info, blog_title=title, blog_bio=bio)
# view other blogs, no editing perms


"""
@app.route("/blog")
def viewBlog():
    # <SOME CODE> dpdt on DB method to fetch blog data
    return render_template()  # dpdt on blog.html
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
