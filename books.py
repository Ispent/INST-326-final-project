import sqlite3
import csv

#conn = sqlite3.connect("books.db")
#cursor = conn.cursor()
#print(conn.total_changes)
class Books:
    """ A class to manage book records in a SQL database.
    
    Attributes:
        conn (sqlite3.connection): Connection to the books.db database.
        cursor (sqlite3.cursor): Cursor used to execute SQL queries.
    """
    
    def __init__(self):
        """Initializes connection to the books.db and creates a cursor for executing SQL queries.
        
        Args:
            conn (sqlite3.connection): see Class documentation.
            cursor (sqlite3.cursor): see Class documentation.
        Side effects: 
            Opens SQLite database called "books.db"
        """
        
        #connecting to database and creates a cursor
        self.conn = sqlite3.connect("books.db")
        self.cursor = self.conn.cursor()
    
    def input_data(self, path):
        """ Opens csv file and initializes SQL database.
       
        Args:
            path (str): The file path to the CSV file.
            
        Side Effects: 
            Drops books table if it exists.
            Creates new books table.
            Inserts data from the csv file into the database.
            Prints each book in the table.
        """
        
        self.path = path
        
        #opening csv file
        with open(path) as file:
            contents = csv.reader(file)
            
            #formatting data by removing first column
            data = [] #initializing empty list
            for row in contents:
                data.append(row[1:]) #appending each row except the first column
            
            #dropping existing table    
            self.cursor.execute("DROP TABLE IF EXISTS books")
            
            #creating book table in database
            create_table = '''CREATE TABLE books (
                    title TEXT, author TEXT, publication_date INTEGER
                    )'''
            self.cursor.execute(create_table)

            #inserting data into books table
            insert_records = '''INSERT INTO books (title, author, publication_date) VALUES (?,?,?)'''
            self.cursor.executemany(insert_records, data)
            self.conn.commit()

            #selecting all records from the books table
            select_all = '''SELECT * FROM books'''
            books = self.cursor.execute(select_all).fetchall()
    
            #printing each book in the table
            for book in books:
                print(book)

        
    
    def info(self):
        """ Returns number of books in the database.
        
        Args: 
            None
            
        Returns:
            str: Number of books in database.
        
        Side Effects:
            Closes the database connection.
        """
        
        #counting amount of books in the db
        count = self.cursor.execute('''SELECT COUNT (*) FROM books''').fetchone()[0]
        self.conn.close() #closing db connection
        return f"There are {count} books in this database."
        


if __name__=="__main__":
    #creating instance of Books class
    book_db = Books()
    book_db.input_data('books.csv')
    print(book_db.info()) #printing count of books in db
    