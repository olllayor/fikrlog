import hashlib
import os
from flask import Flask, render_template, session, request, make_response, flash
# from flask_ckeditor import CKEditor

from articles import Article 

app = Flask(__name__)
# ckeditor = CKEditor(app)

app.secret_key = "thisissecretkey"

ARTICLES_DIR = "articles"
# Authentication


# Cookie, Session
# Hashing, Sha256


# users = {
#     "admin": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
# }


articles = Article.all()

@app.route('/')
def blog():
    return render_template('index.html', articles=articles)




# @app.get('/admin')
# def admin_page():

#     if "user" in session:
#         return "You are already in"

#     return render_template('login.html')

# @app.post('/admin')
# def admin_login():
#     username = request.form["username"]
#     password = request.form["password"]

#     if username not in users:
#         return render_template('login.html', error="Invalid Username")

#     hashed = hashlib.sha256(password.encode()).hexdigest()
    
#     if users[username] != hashed:
#         return render_template('login.html', error="Invalid Password")
#     session["user"] = username
#     return "You are now authenticated"

@app.route('/blog/<slug>')
def article(slug: str):
    article = articles[slug]    
    return render_template('article.html', article=article)
@app.route('/publish', methods=['GET', 'POST'])
def publish():
    # if "user" not in session:
    #     return render_template('login.html', error="Please log in to publish an article")

    if request.method == 'GET':
        return render_template('publish.html')

    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]

        # Create a new article instance with title and content
        new_article = Article(title, content)
        
        # Save the article content into a file within the 'articles' folder
        article_filename = f"{new_article.title}"
        article_path = os.path.join(ARTICLES_DIR, article_filename)
        with open(article_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {new_article.title}\n\n{new_article.content}")

        # Redirect to the updated blog page after publishing the article
        # return redirect('/')
        # Add the new article to the articles dictionary
        slug = new_article.slug
        articles[slug] = new_article  # Update the dictionary with the new article
        return render_template('blog.html', articles=articles)  # Pass the updated articles dictionary
    title = request.form.get('title')
    content = request.form.get('content')

    insert_article(title, content)
    flash("Article published successfully!")

    return render_template('blog.html', articles=articles)
# @app.route("/set-session")
# def set_session():
#     session["user_id"] = 1
#     return "session set"

# @app.route("/get-session")
# def get_session():
#     return f"user_id = {session['user_id']}"

# @app.route("/first-time")
# def first_time():
#     if 'seen' not in request.cookies:
#         response = make_response("You are new here")
#         response.set_cookie('seen', "1")
#         return response
    
#     seen = int(request.cookies['seen'])

#     response = make_response(f"I have seen you before {seen} times!")
#     response.set_cookie('seen', str(seen + 1))
#     return response

# Create Custom Error Pages

#Invalid URL
@app.errorhandler(404)# type: ignore
def page_not_found(e): # type: ignore
    return render_template('404.html'), 404

@app.errorhandler(500) # type: ignore
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(port=4200, debug=True)

