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
    if 'blog_id' in session:
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
                           blog_info_part2=blog_info[:mid],
                           blog_info_part1=blog_info[mid:],
                           real_user=session['username'])

    # return render_template("home.html", names=names)


# create blog func
@app.route("/createBlog")
def createBlogPage():
    return render_template("createBlogForm.html", real_user=session['username'])  # createBlogForm.html


@app.route("/createBlogRead", methods=['POST'])
def createBlogForm():
    bT = request.form['blogTitle']
    dC = request.form['dateCreated']

    bB = request.form['blogBio']
    if bT == "" or dC == "" or bB == "":
        # fix later by changing button to return to home
        return render_template("blogError.html", real_user=session['username'], error="You need to fill all three fields")

    createBlog(session['user_id'], session['username'], bT, dC, bB)
    return redirect("/home")

    # return render_template("successBlog.html") #dpdt on blog.html and the info asked from form


# add blog entry func
@app.route("/addEntry")
def addBlogEntry():
    return render_template("addEntryForm.html", real_user=session['username'])


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
    blogs = getUserBlogs(getUserId(user))
    blog_info = []

    for blog_id in blogs:
        blog_info.append(list(getBlogBasic(blog_id)))

    return render_template("profile.html", username=user,
                           length=len(blog_info), blog_info=blog_info,
                           real_user=session['username'])


# view your blog, has editing perms
@app.route("/yourBlog")
def viewYourBlog():
    blog_id = 0
    username = ""
    if ',,,' in request.args.get('blog_num'):

        blog_id = request.args.get('blog_num').split(',,,')[0]
        username = request.args.get('blog_num').split(',,,')[1]
    else:
        blog_id = request.args.get('blog_num')
        username = request.args.get('user')

    if username != session['username']:
        return redirect("/blog?blog_num={}&user={}".format(blog_id, username))

    session['blog_id'] = blog_id
    title, bio, date, _id, username = getBlogBasic(blog_id)

    entry_info = []
    for entry_id in getBlogEntries(blog_id):
        entry_info.append(list(getEntryInfo(entry_id)))

    return render_template("yourBlog.html", real_user=session['username'], username=session['username'], entry_info=entry_info, blog_title=title, blog_bio=bio)


# view other blogs, no editing perms
@app.route("/blog")
def viewBlog():
    blog_id = request.args.get('blog_num')
    username = request.args.get('user')

    session['blog_id'] = blog_id
    title, bio, date, _id, username = getBlogBasic(blog_id)

    entry_info = []
    for entry_id in getBlogEntries(blog_id):
        entry_info.append(list(getEntryInfo(entry_id)))

    return render_template("blog.html", username=username,
                           entry_info=entry_info, blog_title=title,
                           blog_bio=bio, real_user=session['username'])


@app.route("/editEntry", methods=['GET'])
def entryEdit():
    entry_id = request.args.get('entry_id')

    entry_title = getEntryInfo(entry_id)[2]
    entry_content = getEntryInfo(entry_id)[3]

    return render_template("editEntryForm.html", entry_title=entry_title,
                           entry_content=entry_content, entry_id=entry_id,
                           real_user=session['username'])


@app.route("/editEntryRead", methods=['POST'])
def editEntryRead():

    new_entry_title = request.form['entryTitle']
    new_entry_content = request.form['entryContent']
    entry_id = request.form['entry_id']

    if new_entry_content == "" or new_entry_title == "":
        return render_template("entryEditError.html",
                               real_user=session['username'], error="Please fill in both fields")

    editEntry(entry_id, new_entry_title, new_entry_content)
    return redirect("/home")


if __name__ == "__main__":
    app.debug = True
    app.run()
