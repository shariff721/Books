from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import author, book


@app.route('/books')
def all_books():
    books = book.Book.get_all_books()
    return render_template("books_dashboard.html", all_books = books)

@app.route('/new/book', methods = ["POST"])
def add_new_book():
    book.Book.save_book(request.form)
    return redirect('/books')

@app.route('/book/<int:id>')
def book_with_author(id):
    data = {
        'id':id
    }
    return render_template("book_show.html", one_book = book.Book.get_book_with_author(data), all_authors = author.Author.get_all_authors())

@app.route('/favauthor/book', methods = ["POST"])
def add_fav_author():
    data = {
        'book_id':request.form['book_id'],
        'author_id':request.form['author_id']
    }
    book.Book.add_fav_author(data)
    return redirect(f"/book/{request.form['book_id']}")


