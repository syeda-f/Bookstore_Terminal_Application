# Bookstore-Terminal-Application
A terminal-based bookstore application where users can register, browse books by subject or search by author/title, add books to a cart, and check out with invoice generation.

## Features
+ User registration and login
+ Browse books by subject (displayed 2 at a time)
+ Search by author or title (displayed 3 at a time)
+ Add books to shopping cart with quantity
+ Checkout with shipping address and order summary
+ Automatic invoice generation with estimated delivery date
+ Unique order number generation (UUID)

## Database Schema
+ `members`: user accounts (fname, lname, address, city, state, zip, phone, email, userid, password)
+ `books`: book catalog (isbn, author, title, price, subject)
+ `cart`: shopping cart (userid, isbn, qty)
+ `orders`: order header (userid, order_no, received, shipped, shipAddress, shipCity, shipState, shipZip)
+ `odetails`: order details (order_no, isbn, qty, price)

## Tools Used
+ Python
+ MySQL

