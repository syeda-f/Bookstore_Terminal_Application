import mysql.connector
from datetime import datetime
import uuid

# connecting to mySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="books_db"
)

# creating cursor object
my_cursor = db.cursor()

userid = None


def set_userid(user_id):
    global userid
    userid = user_id


def access_userid():
    global userid
    return userid


def main_menu():
    print(" ")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("* * *                                                 * * *")
    print("* * *         Welcome to the Online Book Store        * * *")
    print("* * *                                                 * * *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print()
    print("                   1. Member Login                         ")
    print("                   2. New Member Registration              ")
    print("                   q. Quit                                 ")
    print()

    option = input("Type in your option: ")
    if option == "1":
        member_login()
    if option == "2":
        member_registration()
    if option == "q":
        quit()
    else:
        print("Invalid input!")


def member_registration():
    print()
    print("Welcome to the Online Book Store")
    print("     New Member Registration    ")
    print()

    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    address = input("Enter street address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zip = input("Enter zip: ")
    phone = input("Enter phone: ")
    email = input("Enter email address: ")
    userid = input("Enter userId: ")
    password = input("Enter password: ")

# inserting new members in the member table
    query_1 = "INSERT INTO members (fname, lname, address, city, state, zip, phone, email, userid, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    query_1_values = (fname, lname, address, city, state, zip, phone, email, userid, password)
    my_cursor.execute(query_1, query_1_values)

# making changes to database
    db.commit()

    print()
    print("You have registered successfully!")

    my_cursor.close()
    db.close()

    main_menu()


def member_login():
    print("Welcome to the Online Book Store")
    print("     Member Login     ")
    print(" ")

    userid = input("Enter userID: ")
    password = input("Enter password: ")

    query_2 = "SELECT * FROM members WHERE userid = %s AND password = %s"
    query_2_values = (userid, password)
    my_cursor.execute(query_2, query_2_values)
    outcome = my_cursor.fetchone()

    if outcome:
        set_userid(userid)
        print("You have logged in successfully!")
        while True:
            print()
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
            print("* * *                                                 * * *")
            print("* * *         Welcome to the Online Book Store        * * *")
            print("* * *                 Member Menu                     * * *")
            print("* * *                                                 * * *")
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
            print("                   1  Browse by Subject                    ")
            print("                   2  Search by Author/Title               ")
            print("                   3  Checkout                             ")
            print("                   4  Logout                               ")
            print()

            option = input("Type in your option")
            if option == "1":
                browse_by_subject()
            elif option == "2":
                search_by_author_or_title()
            elif option == "3":
                checkout()
            elif option == "4":
                print("You have logged out successfully!")
            db.close()
            break
    else:
        print("Invalid username/login credentials!")


def member_menu():
    while True:
        print()
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("* * *                                                 * * *")
        print("* * *         Welcome to the Online Book Store        * * *")
        print("* * *                 Member Menu                     * * *")
        print("* * *                                                 * * *")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("                   1  Browse by Subject                    ")
        print("                   2  Search by Author/Title               ")
        print("                   3  Checkout                             ")
        print("                   4  Logout                               ")
        print()

        option = input("Type in your option: ")
        if option == "1":
            browse_by_subject()
        elif option == "2":
            search_by_author_or_title()
        elif option == "3":
            checkout()
        elif option == "4":
            print("You have logged out successfully!")
            break
        else:
            print("Invalid input!")


def browse_by_subject():
    print()
    print("   Browse by Subject   ")
    print()

    my_cursor = db.cursor()
    my_cursor.execute("SELECT DISTINCT subject FROM books ORDER BY subject")
    all_subjects = my_cursor.fetchall()

# lists the subjects
    print("List of Subjects: ")
    for i, sub_name in enumerate(all_subjects):
        print(str(i + 1) + ". " + sub_name[0])

    choice = input("Enter your choice: ")
    if choice.isdigit() and int(choice) <= len(all_subjects):
        subject = all_subjects[int(choice)-1][0]

# listing the books for the subject selected
    query_3 = ("SELECT * FROM books WHERE subject = %s")
    query_3_values = (subject,)
    my_cursor.execute(query_3, query_3_values)
    all_books = my_cursor.fetchall()

    if not all_books:
        print("0 books found")
        return

    print(len(all_books), "available on this subject")

# displays details of 2 books at a time
    i = 0
    while i < len(all_books):
        print("Author: ", all_books[i][0])
        print("Title: ", all_books[i][1])
        print("ISBN: ", all_books[i][2])
        print("Price: ", all_books[i][3])
        print("Subject: ", all_books[i][4])

        if (i + 1) < len(all_books):
            print("Author: ", all_books[i + 1][0])
            print("Title: ", all_books[i + 1][1])
            print("ISBN: ", all_books[i + 1][2])
            print("Price: ", all_books[i + 1][3])
            print("Subject: ", all_books[i + 1][4])

        option = input("Enter ISBN to add to Cart or ENTER 'n' to browse"
                       " or press ENTER to go back to menu: ")
        if option == "":
            member_menu()
        elif option == "n":
            i = i + 2
        else:
            add_to_cart()


def search_by_author_or_title():
    print()
    print("   Search by Author/Title   ")
    print(" 1. Author Search ")
    print(" 2. Title Search ")
    print(" 3. Go Back to Member Menu ")
    print()

    option = input("Type in your option: ")
    if option == "1":
        search_by_author()
    elif option == "2":
        search_by_title()
    elif option == "3":
        member_menu()
    else:
        print("Invalid input!")


def search_by_author():
    print()
    author_sub_option = input("Enter Author Name: ")
    print()
    my_cursor = db.cursor()
    query_4 = "SELECT * FROM books WHERE author LIKE %s"
    query_4_values = ("%" + author_sub_option + "%",)
    my_cursor.execute(query_4, query_4_values)
    all_books_1 = my_cursor.fetchall()

    if not all_books_1:
        print("0 books found")
        return

    print(len(all_books_1), "books found")

# displays details of 3 books at a time
    i = 0
    while i < len(all_books_1):
        print("Author: ", all_books_1[i][1])
        print("Title: ", all_books_1[i][2])
        print("ISBN: ", all_books_1[i][0])
        print("Price: ", all_books_1[i][3])
        print("Subject: ", all_books_1[i][4])

        if (i + 1) < len(all_books_1):
            print("Author: ", all_books_1[i + 1][1])
            print("Title: ", all_books_1[i + 1][2])
            print("ISBN: ", all_books_1[i + 1][0])
            print("Price: ", all_books_1[i + 1][3])
            print("Subject: ", all_books_1[i + 1][4])

        if (i + 2) < len(all_books_1):
            print("Author: ", all_books_1[i + 2][1])
            print("Title: ", all_books_1[i + 2][2])
            print("ISBN: ", all_books_1[i + 2][0])
            print("Price: ", all_books_1[i + 2][3])
            print("Subject: ", all_books_1[i + 2][4])

        opt = input("Enter ISBN to add to Cart or Enter 'n' to browse"
                    " or press ENTER to go back to menu: ")
        if opt == "":
            search_by_author_or_title()
        elif opt == "n":
            i = i + 3
        else:
            add_to_cart()


def search_by_title():
    print()
    title_sub_option = input("Enter Title or part of Title: ")
    print()
    my_cursor = db.cursor()
    query_5 = "SELECT * FROM books WHERE title LIKE %s"
    query_5_values = ("%" + title_sub_option + "%",)
    my_cursor.execute(query_5, query_5_values)
    all_books_2 = my_cursor.fetchall()

    if not all_books_2:
        print("0 books found")
        return

    print(len(all_books_2), "books found")

# displays details of 3 books at a time
    j = 0
    while j < len(all_books_2):
        print("Author: ", all_books_2[j][1])
        print("Title: ", all_books_2[j][2])
        print("ISBN: ", all_books_2[j][0])
        print("Price: ", all_books_2[j][3])
        print("Subject: ", all_books_2[j][4])

        if (j + 1) < len(all_books_2):
            print("Author: ", all_books_2[j + 1][1])
            print("Title: ", all_books_2[j + 1][2])
            print("ISBN: ", all_books_2[j + 1][0])
            print("Price: ", all_books_2[j + 1][3])
            print("Subject: ", all_books_2[j + 1][4])

        if (j + 2) < len(all_books_2):
            print("Author: ", all_books_2[j + 2][1])
            print("Title: ", all_books_2[j + 2][2])
            print("ISBN: ", all_books_2[j + 2][0])
            print("Price: ", all_books_2[j + 2][3])
            print("Subject: ", all_books_2[j + 2][4])

        opt_ = input("Enter ISBN to add to Cart or ENTER 'n' to browse"
                     " or press ENTER to go back to menu: ")
        if opt_ == "":
            search_by_author_or_title()
        elif opt_ == "n":
            j = j + 3
        else:
            add_to_cart()


def add_to_cart(userid):
    book_id = input("Enter isbn: ")

    if not book_id.isdigit():
        print("Invalid book_id!")
        return

# details of book/books for the entered isbn
    query_6 = ("SELECT * FROM books WHERE isbn = %s")
    query_6_values = (book_id,)
    my_cursor.execute(query_6, query_6_values)
    all_books_3 = my_cursor.fetchone()

    if all_books_3:
        quantity = input("Enter quantity: ")
        userid = access_userid()
        query_7 = ("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)")
        query_7_values = (userid, book_id, quantity)
        my_cursor.execute(query_7, query_7_values)
        db.commit()
        print("The book/books is/are added to cart successfully!")

    else:
        print("The book does not exist!")


def checkout(userid):
    print()
    print("   Checkout   ")

    my_cursor = db.cursor()
    query_8 = ("SELECT address, city, state, zip FROM users WHERE user_id = %s")
    query_8_values = (userid,)
    my_cursor.execute(query_8, query_8_values)
    current_address = my_cursor.fetchone()
    address, city, state, zip_ = current_address

    query_9 = ("SELECT books.isbn, books.title, books.price, cart.qty FROM books INNER JOIN cart ON books.isbn = cart.isbn WHERE cart.userid = %s")
    query_9_values = (userid,)
    my_cursor.execute(query_9, query_9_values)
    cart_contents = my_cursor.fetchall()

    if cart_contents:
        print("Current Cart Contents: ")
        print()

        total = 0
        print("ISBN \t\t", "Title \t\t\t\t\t\t\t", "€ \t", "Qty \t", "Total")
        print("-" * 100)

        for (isbn, title, price, qty) in cart_contents:
            print(isbn, title, "\t", qty, "\t", price * qty)
            total = total + (price * qty)
        print("-" * 100)

        print("Total \t\t\t\t\t\t\t\t\t\t\t", total, "€")
        print("-" * 100)

    else:
        print("The cart is empty!")

    while True:
        to_checkout = input("Proceed to check out (Y/N)?: ")

        if to_checkout.lower() == "y":
            order_no = str(uuid.uuid4().int)[:10]
            display_order(order_no, address, city, state, zip_, total)
            display_invoice(userid, order_no, cart_contents, total)
            break

        elif to_checkout.lower() == "n":
            break

        else:
            print("Invalid input!")


def display_order(userid, order_no, address, city, state, zip_, cart_contents):
    my_cursor = db.cursor()

# saving order to 'orders' table
    query_9 = ("INSERT INTO orders (userid, received, shipped, shipAddress, shipCity, shipState, shipZip) VALUES (%s, NOW(), DATE_ADD(NOW(), INTERVAL 1 WEEK), %s, %s, %s, %s)")
    query_9_values = (userid, order_no, address, city, state, zip_)
    my_cursor.execute(query_9, query_9_values)

# saving order to 'odetails' table
    for i in cart_contents:
        query_10 = ("INSERT INTO odetails (ono, isbn, qty, price) VALUES (%s, %s, %s, %s)")
        query_10_values = (order_no, i[0], i[1], i[2])
        my_cursor.executemany(query_10, query_10_values)

# emptying items from cart
    my_cursor.execute("DELETE FROM cart")
    db.commit()
    print("The order is placed successfully!")


def display_invoice(userid, order_no, outcome, total):
    query_11 = ("SELECT fname, lname, address, city, state, zip FROM members WHERE userid = %s")
    query_11_values = (userid,)
    my_cursor.execute(query_11, query_11_values)

    member_details = my_cursor.fetchone()
    fname, lname, address, city, state, zip_ = member_details

    print("\t\t\t\t\tInvoice for Order No.", order_no)
    print()
    print("Shipping Address")
    print("Name:\t\t", fname, lname)
    print("Address:\t", address)
    print("\t\t", city)
    print("\t\t", state, zip_)
    print()
    print("-" * 100)

    print("ISBN \t\t", "Title \t\t\t\t\t\t\t", "€ \t", "Qty \t", "Total")
    print("-" * 100)

    for isbn, title, price, qty, total in outcome:
        print(isbn, "\t", title, "\t" * 2, price, "\t", qty, "\t", total)
    print("-" * 100)

    print("Total = \t\t\t\t\t\t\t\t\t\t", total, "€")
    print("-" * 100)
    print()

    current_date = datetime.date.today()
    estimated_delivery_date = current_date + datetime.timedelta(days=7)
    print("Estimated delivery date : ", estimated_delivery_date.strftime("%d/%m/%Y"))
    print()

    input("Press ENTER to go back to Menu")
