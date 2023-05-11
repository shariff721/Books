from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import author, book


@app.route('/authors')
def author_dashboard():
    authors = author.Author.get_all_authors()
    return render_template("authors_dashboard.html", all_authors = authors)

@app.route('/new/author', methods = ["POST"])
def add_new_author():
    data = {
        'name':request.form['name']
    }
    author.Author.save_author(data)
    return redirect('/authors')

@app.route('/author/<int:id>')
def author_with_book(id):
    data = {
        'id':id
    }
    return render_template("author_show.html", one_author = author.Author.get_author_with_books(data), all_books = book.Book.get_all_books())

@app.route('/favbook/author', methods = ["POST"])
def add_fav_book():
    data = {
        'book_id':request.form['book_id'],
        'author_id':request.form['author_id']
    }
    author.Author.add_fav_book(data)
    return redirect(f"/author/{request.form['author_id']}")