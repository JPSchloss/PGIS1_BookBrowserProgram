# Jonathan Schlosser
# Assignment 7 Book Browser
# INLS 560 Fall 2019
# July 1, 2020

# The purpose of this code is to create a simple browser GUI for the books database. The GUI will
# sort results in alphabetical order by title, author, or category.
# It will also have a search functionality that will work to search all columns. After each search,
# the results will be cleared.

# Notes: For this program, the books.db file must be in the same directory as the Python file. If not,
#        there may be an error.

# Importing needed packages.
import tkinter
import sqlite3
import os

db = None
# This is a global variable, that initially has no value,
# but will be defined as the object representing the database.

# Setting the background colors and fonts.
bg_color = 'red'
button_color = 'white'
button_font = 'Helvetica 18 bold'
title_font = 'Helvetica 36 bold'
text_font = 'Helvetica 14 bold'


# BookBrowser class that defines the GUI for the application
class BookBrowser:
    def __init__(self, rows):
        # Main window for the application
        self.main_window = tkinter.Tk()
        self.main_window.geometry('1100x1000')
        self.main_window.configure(background=bg_color)

        # Sets the title for the program.
        tkinter.Label(self.main_window, text='A Very Simple Book Browser',
                      font=title_font, bg=bg_color
                      ).grid(row=0, column=1, pady=10)

        # Sets the search button and the text entry box.
        self.search_value = tkinter.StringVar()
        tkinter.Button(self.main_window, text="Search", font=button_font, bg=button_color,
                       command=self.search_db).grid(row=1, column=0, pady=20)
        self.search_value_entry = tkinter.Entry(self.main_window, width=15, font=button_font,
                                                textvariable=self.search_value).grid(row=1, column=1, pady=20)

        # Creating the column headers for the list of books: Title, Author, and Category.
        # Each header is a Button. When clicked, the sort_db function is called to sort
        # the data on the corresponding column.
        try:
            tkinter.Button(self.main_window, text='Title', font=button_font, bg=button_color,
                           command=lambda: self.sort_db('Title')).grid(row=2, column=0, padx=10, pady=10)
            tkinter.Button(self.main_window, text='Author', font=button_font, bg=button_color,
                           command=lambda: self.sort_db('Author')).grid(row=2, column=1, padx=10, pady=10)
            tkinter.Button(self.main_window, text='Category', font=button_font, bg=button_color,
                           command=lambda: self.sort_db('Category')).grid(row=2, column=2, padx=10, pady=10)

            # Display the results (in rows variable) of the query executed in the main function.
            self.display_rows(rows)

            tkinter.mainloop()
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred:', err)

        # Including a footer to ensure continuity.


    # Displays the results of the last query. The results (list of tuples) are contained in the rows variable.
    # If this function is called after a search, it is possible there are no results.
    # In this case, a "No results found" message is displayed.
    def display_rows(self, rows):
        # Clearing previous results.
        for label in self.main_window.grid_slaves():
            if int(label.grid_info()['row']) > 2:
                label.grid_forget()

        # Book titles are displayed as Radiobuttons
        # Each Radiobutton has a variable with a unique value defined by the book ISBN (self.book_isbn)
        # When a Radiobutton is clicked, the get_book_details function is called to display the details
        # for the book with the associated ISBN
        self.book_isbn = tkinter.StringVar()    # variable, with a unique value, that is associated with each book
        self.book_isbn.set("not selected yet")  # forces the radio buttons to initially display as not selected

        r = 3
        for row in rows:
            tkinter.Radiobutton(self.main_window, text=row[1], bg=bg_color, font=text_font,
                                variable=self.book_isbn, value=row[0], command=self.get_book_details,
                                indicatoron=0, borderwidth=0).grid(row=r, column=0, padx=10)
            tkinter.Label(self.main_window, text=row[2], bg=bg_color, font=text_font).grid(row=r, column=1, padx=10)
            tkinter.Label(self.main_window, text=row[5], bg=bg_color, font=text_font).grid(row=r, column=2, padx=10)
            r = r + 1

        # Displaying No Results message if no results are found.
        if r == 3:
            tkinter.Label(self.main_window, text="No Results Found. \n Would you like to search again?",
                          font=button_font, bg=bg_color).grid(row=r, column=1, pady=20)


    # Searching the database using a wildcard search across the Title, Author, and Category columns
    def search_db(self):
        # Get the search value entered by the user
        search_term = self.search_value.get()

        # Connecting to the database and conducting the search if the search is not blank.
        global db
        try:
            dbname = 'books.db'
            if os.path.exists(dbname):
                db = sqlite3.connect(dbname)
                cursor = db.cursor()
                if search_term != '':
                    sql = "SELECT * FROM Book WHERE Title LIKE '%" + search_term + "%'  OR  " \
                                                    "Author LIKE '%" + search_term + "%' OR " \
                                                    "Category LIKE '%" + search_term + "%' ORDER BY Title"
                # If the search is blank, then the SQL returns all results ordered by the title.
                else:
                    sql = 'SELECT * FROM Book ORDER BY Title'
                cursor.execute(sql)
                rows = cursor.fetchall()
                db.close()
                # Calling display_rows to display the results.
                self.display_rows(rows)
            else:
                print('Error:', dbname, 'does not exist')
        # Exception handling for SQLite
        except sqlite3.IntegrityError as err:
            print('Integrity Error on connect:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error on connect:', err)
        except sqlite3.Error as err:
            print('Error on connect:', err)

    # Sorting the database on the selected column name (Title, Author, or Category)
    def sort_db(self, column_name):
        # Clearing any previous value in the search entry field
        self.search_value.set('')

        # Connecting to the database and conducting the sort based on the radiobutton selected.
        global db
        try:
            dbname = 'books.db'
            if os.path.exists(dbname):
                db = sqlite3.connect(dbname)
                cursor = db.cursor()
                # Chose to create separate SQL statements to be more explicit in the code.
                if column_name == 'Title':
                    sql = "SELECT * FROM Book ORDER BY Title"
                elif column_name == 'Author':
                    sql = "SELECT * FROM Book ORDER BY Author"
                elif column_name == 'Category':
                    sql = "SELECT * FROM Book ORDER BY Category"
                else:
                    sql = "SELECT * FROM Book ORDER BY Title"
                cursor.execute(sql)
                rows = cursor.fetchall()
                db.close()
                # Calling display_rows to display the results.
                self.display_rows(rows)
            else:
                print('Error:', dbname, 'does not exist')
        # Exception handling for SQLite
        except sqlite3.IntegrityError as err:
            print('Integrity Error on connect:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error on connect:', err)
        except sqlite3.Error as err:
            print('Error on connect:', err)

    # When the user clicks a Title RadioButton, the ISBN value for the associated book is saved in
    # the self.book_isbn variable. This value is used to query the database for that specific book.
    def get_book_details(self):
        # Getting the isbn...
        isbn = self.book_isbn.get()

        # Connecting to the database and conducting the search based on the ISBN.
        global db
        try:
            dbname = 'books.db'
            if os.path.exists(dbname):
                db = sqlite3.connect(dbname)
                cursor = db.cursor()
                sql = "SELECT * FROM Book WHERE ISBN = '" + isbn + "'"
                cursor.execute(sql)
                rows = cursor.fetchall()
                db.close()
                # Calling display_book_details to present the results.
                self.display_book_details(rows)
            else:
                print('Error:', dbname, 'does not exist')
        # Exception handling for SQLite
        except sqlite3.IntegrityError as err:
            print('Integrity Error on connect:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error on connect:', err)
        except sqlite3.Error as err:
            print('Error on connect:', err)

    # Displaying the details for a specific book.
    # The variable rows is a list with one tuple that contains the detailed information for a specific book
    def display_book_details(self, rows):
        # Creating a new window to display the details for the selected book and establishing the settings.
        self.details_window = tkinter.Toplevel(self.main_window)
        self.details_window.geometry('400x200')
        self.details_window.configure(background=bg_color)

        # Each book detail (ISBN, Title, Author, Publisher, Format, Category) is displayed as a Label.
        # Each Label is laid out in a single column grid in the window.
        for row in rows:
            tkinter.Label(self.details_window, bg=bg_color, font=text_font,
                          text='ISBN:\t\t'+row[0]).grid(row=6, column=1, sticky=tkinter.constants.W)
            tkinter.Label(self.details_window, bg=bg_color, font=button_font,
                          text='Title:\t'+row[1]).grid(row=1, column=1, sticky=tkinter.constants.W)
            tkinter.Label(self.details_window, bg=bg_color, font=text_font,
                          text='Author:\t\t'+row[2]).grid(row=2, column=1, sticky=tkinter.constants.W)
            tkinter.Label(self.details_window, bg=bg_color, font=text_font,
                          text='Publisher:\t'+row[3]).grid(row=3, column=1, sticky=tkinter.constants.W)
            tkinter.Label(self.details_window, bg=bg_color, font=text_font,
                          text='Format:\t\t'+row[4]).grid(row=5, column=1, sticky=tkinter.constants.W)
            tkinter.Label(self.details_window, bg=bg_color, font=text_font,
                          text='Category:\t'+row[5]).grid(row=4, column=1, sticky=tkinter.constants.W)


# The main function connects to the database and executes a query to retrieve a list of all books
# in the database. A BookBrowser object is created to define the GUI for the application, and the
# results of the query (rows variable) is passed to the GUI which will display the results.
def main():
    global db
    try:
        dbname = 'books.db'
        if os.path.exists(dbname):
            db = sqlite3.connect(dbname)
            cursor = db.cursor()
            sql = 'SELECT * FROM Book ORDER BY Title'
            cursor.execute(sql)
            rows = cursor.fetchall()
            BookBrowser(rows)
            db.close()
        else:
            print('Error:', dbname, 'does not exist')
    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on connect:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)


main()
