# Blog by EandF
a blog hosting site with register, login, logout functionality. users can view, create, and edit blogs and their posts. 

## Installation on Linux
```sh
 $ git clone https://github.com/KarlWithK/EandF.git
 $ cd EandF/
 $ pip install -r requirements.txt
 $ flask run
 $ xdg-open http://localhost:500/
```

## Roles:
- Carlos "Karl" Hernandez: PM, database manager, CSS for templates
- Eric Lo: Flask app
- Amelia Chin: HTML for Jinja templates
- Ari Schechter: database manager
(We eventually overlapped roles and worked with each other a lot on different areas)

## Known Issues
- Redirecting to home all the time for various things is annoying, but it avoids errors regarding lost query strings
  - We put the create new blog on the home page, but it should have gone on the profile page (we would have to make a separate yourProfile route with editing perms)
- DO NOT USE THE " CHARACTER WHEN ADDING ENTRIES (actually just avoid it when typing any info into a form)
- It doesn't make sense to be able to choose the date created for blog creation
- We didn't get to implement deleting entries
- There is no clear way to check who you are signed in as
