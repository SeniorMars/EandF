# Blog by EandF
A blog hosting site with register, login, logout functionality. Users can view, create, and edit blogs and their entries. 

## Launch Codes
```sh
 $ git clone https://github.com/KarlWithK/EandF.git
 $ cd EandF/
 $ pip install -r requirements.txt
 $ flask run
 $ xdg-open http://localhost:5000/
```

## Roles:
- Carlos "Karl" Hernandez: PM, database manager, CSS for templates
- Eric Lo: Flask app, king of catching mistakes
- Amelia Chin: HTML for Jinja templates
- Ariel Schechter: database manager
(We eventually overlapped roles and worked with each other a lot on different areas.)

## Known Issues
- Redirecting to home all the time for various things is annoying, but it avoids errors regarding lost query strings
  - We put the create new blog on the home page, but it should have gone on the profile page (we would have to make a separate yourProfile route with editing perms)
- Please do not use the " character (double quotations) when adding blog entries (actually just avoid it when typing any info into a form)
- It doesn't make sense to be able to choose the date created for blog creation, but we didn't have a way to record the current date
- We didn't get to implement deleting entries
- The home page does not list the author of each blog. (it's a surprise!)
- Do not enter new lines in the blog bio
