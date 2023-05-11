from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    db = "books_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.num_of_pages = data["num_of_pages"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.authors = []

    @classmethod
    def save_book(cls,data):
        query = """
            INSERT INTO books
            (title, num_of_pages) VALUES(%(title)s, %(num_of_pages)s)
            """
        return connectToMySQL(cls.db).query_db(query,data)
        
    @classmethod
    def get_all_books(cls):
        query = """
            SELECT * FROM books;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_books = []
        for one_book in results:
            all_books.append(cls(one_book))

        return all_books
    
    @classmethod
    def get_book_with_author(cls,data):
        query = """
            SELECT * FROM books
            LEFT JOIN favourites ON favourites.book_id = books.id
            LEFT JOIN authors ON favourites.author_id = authors.id
            WHERE books.id = %(id)s;
        """

        results = connectToMySQL(cls.db).query_db(query,data)
        book = cls(results[0])

        for book_row in results:
            author_data = {
                "id": book_row["authors.id"],
                "name": book_row["name"],
                "created_at": book_row["authors.created_at"],
                "updated_at": book_row["authors.created_at"]
            }
            book.authors.append(author.Author(author_data))

        return book
    
    @classmethod
    def add_fav_author(cls,data):
        query = """
            INSERT INTO favourites 
            (book_id, author_id) VALUES (%(book_id)s, %(author_id)s);
        """
        return connectToMySQL(cls.db).query_db(query,data)