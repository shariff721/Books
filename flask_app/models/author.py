from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    db = "books_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.books = []


    @classmethod
    def save_author(cls,data):
        query = """
            INSERT INTO authors 
            (name) VALUES (%(name)s);
        """

        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_authors(cls):
        query = """
            SELECT * FROM authors;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_authors = []
        for one_author in results:
            all_authors.append(cls(one_author))

        return all_authors
    
    @classmethod
    def get_author_with_books(cls,data):
        query = """
            SELECT * FROM authors 
            LEFT JOIN favourites on favourites.author_id = authors.id
            LEFT JOIN books on favourites.book_id = books.id
            WHERE authors.id = %(id)s;
        """

        results = connectToMySQL(cls.db).query_db(query,data)
        author = cls(results[0])

        for author_row in results:
            books_data = {
                "id": author_row["books.id"],
                "title": author_row["title"],
                "num_of_pages": author_row["num_of_pages"],
                "created_at": author_row["books.created_at"],
                "updated_at": author_row["books.updated_at"]
            }
            author.books.append(book.Book(books_data))

        return author
    
    @classmethod
    def add_fav_book(cls,data):
        query = """
            INSERT INTO favourites
            (book_id, author_id) VALUES (%(book_id)s, %(author_id)s);
        """
        return connectToMySQL(cls.db).query_db(query,data)
