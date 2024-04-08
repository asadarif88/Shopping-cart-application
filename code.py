import os
from datetime import datetime
import time  # importing time library to use sleep function

filename='productlist.txt'
cart={}


def checkout(): # In this function we are emptying the cart and putting all products in it with its subtotal and total in the history and also displaying bill to user at checkout.
    w=datetime.now()
    Date=w.date()
    Date=str(Date)
    Time=w.time()
    Time=str(Time)
    total=show_cart()
    subtotal=0
    ine=''
    line=''
    for product in cart:
        subtotal+=(cart[product]['price'])*(cart[product]['quantity'])
        ine+='Product : '+product+'  '+'Price : '+(str(cart[product]['price']))+'  '+'Quantity Bought : '+(str(cart[product]['quantity']))+'  '+'Subtotal : '+(str(subtotal))+'\n'
    line+='\n'+'History : '+'\n'+'Checkout date : '+Date+'\n'+'Checkout time : '+Time+'\n'+ine+'Total : '+(str(total))
    f=open(file,'a')
    f.write(line)
    f.close()
    cart.clear()


def history(): # In this fuction, we are just displaying history that we make with help of checkout function, to user
    f=open(file,'r')
    print(f.read())
    f.close()


def type():
    while True:
        global product
        product_user = input("Enter the name of the product you want to add to the cart (Enter 'done' to finish): ")
        if product_user.isalpha():
            product=product_user
        else:
            print('Enter valid name')
            type()
        if product.lower() == 'done':
            break
        global quantity
        while True:
            quantity_input = input('Enter quantity: ')
            if quantity_input.isdigit():
                quantity = int(quantity_input)
                break
            else:
                print("Please enter a valid integer.")
        add_to_cart_result = add_to_cart(product,quantity)
        if not add_to_cart_result:
            print("Please choose another item or type 'done' to finish.")


def add_to_cart(product, quantity):
    if product in products and products[product]["quantity"] >= quantity: # example if "gloves" in that product list
        #and if Product's quantity(in product list) is greater or equal to the quantity that user has entered.
        if product in cart: # if that product is already in cart.
            cart[product]["quantity"] += quantity # add their quantites
        else:
            cart[product] = {"price": products[product]["price"], "quantity": quantity}
        products[product]["quantity"] -= quantity
        update_product_list("product_list.txt")  # Update the product_list.txt after adding quantities
        print(f"Added {quantity} {product}(s) to the cart.") # after calling updateproductlist() function .
        return True
    else:
        print(f"Cannot add {quantity} {product}(s) to the cart.")
        return False
    type()


def remove_from_cart(): # if user doesnot want product that is in the cart. THIS FUNCTION WILL BE CALLED.
    if not cart:  # if cart is already empty
        print("Your cart is empty. Please add products to the cart before attempting to remove.")
        return

    product = input('Enter the name of the product to remove: ')
    quantity = int(input('Enter the quantity to remove: '))

    if product in cart and cart[product]["quantity"] >= quantity:
        cart[product]["quantity"] -= quantity
        products[product]["quantity"] += quantity
        if cart[product]["quantity"] == 0:
            del cart[product]
        print(f"Removed {quantity} {product}(s) from the cart.")
        update_product_list("product_list.txt")  # Update the product_list.txt file after removing items
    elif product not in cart:
        print(f"{product} is not in the cart. Please add it to the cart first.") # if user signup or login and he or she  chooses
        # option 4 "REMOVE" this line will print
    elif cart[product]["quantity"] < quantity:
        print(f"Cannot remove {quantity} {product}(s) from the cart. Not enough quantity in the cart.")
    else:
        print(f"Cannot remove {quantity} {product}(s) from the cart.")


def show_cart():  # this function display products user bought and their subtotal and total to user
    global total
    total = 0
    print("\nYour Shopping Cart:")
    for product, details in cart.items():
        print(f"{product} - {details['quantity']} units - Rs{details['price'] * details['quantity']}")
        total += details['price'] * details['quantity']
    print(f"Total Bill : Rs{total}")
    return total


def load_products(filename):
    global products
    if not os.path.exists(filename):  # Check if the file exists
        print(f"File '{filename}' does not exist. Saving products in the file...")
        products = {
            "gloves": {"price": 1000, "quantity": 100},
            "mouse": {"price": 5000, "quantity": 100},
            "keyboard": {"price": 2000, "quantity": 100},
            "slippers": {"price": 700, "quantity": 100},
            "notebook": {"price": 280, "quantity": 100},
            "shoes": {"price": 2500, "quantity": 100},
            "hairbands": {"price": 25, "quantity": 100},
            "hoodie": {"price": 899, "quantity": 100},
            "blackpen": {"price": 15, "quantity": 100},
            "eraser": {"price": 20, "quantity": 100},
        }
        with open(filename, 'w') as file:
            for product in products:
                file.write(
                    f"Product: {product}, Price: {products[product]['price']}, Quantity: {products[product]['quantity']}\n")
    else:
        print(f"File '{filename}' already exists. Loading products from the file...")
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        products = {} # initiating an empty dictionary. after iteration this dict will be updating.
        for line in lines: # iterated over each line
            product_info = line.strip().split(", ") # whole product info( name,quantity,price)
            product_name = product_info[0].split(": ")[1] # this will pick just product's name
            product_price = int(product_info[1].split(": ")[1]) # product's price
            product_quantity = int(product_info[2].split(": ")[1]) # pick product's quantity that are remaining.

            products[product_name] = {"price": product_price, "quantity": product_quantity}


def update_product_list(filename):  # this will update the file.
    with open(filename, 'r') as file:
        lines = file.readlines()  # after adding product to the cart. Now remaining products quantites are left

    updated_products = {} # initiating an empty dictionary. after iteration this dict will be updating.
    for line in lines: # iterated over each line
        product_info = line.strip().split(", ") # whole product info( name,quantity,price)
        product_name = product_info[0].split(": ")[1] # this will pick just product's name
        product_price = int(product_info[1].split(": ")[1]) # product's price
        product_quantity = int(product_info[2].split(": ")[1]) # pick product's quantity that are remaining.

        if product_name in products:
            remaining_quantity = products[product_name]['quantity'] # will show remaining quantity like if 97 gloves are left.
            updated_products[product_name] = { # dict is updating
                "price": product_price,
                "quantity": remaining_quantity
            }
        else:
            # If the product is not in the current products dictionary,
            # write the original line back to the file
            updated_products[product_name] = {
                "price": product_price,
                "quantity": product_quantity
            }

    with open(filename, 'w') as file: # writing back to the file(remaining quantity)
        for product, details in updated_products.items(): # details showing product quantity and price.
            file.write(f"Product: {product}, Price: {details['price']}, Quantity: {details['quantity']}\n")


def display(filename):  # this will display all products line by line when user wants to see products.

    with open(filename, 'r') as file:  # it will read file (product_list.txt)
        lines = file.readlines()  # will read each line. All compliled in List
        if not lines:  # if file will not have data
            print("No products found.")
        else:  # else products are stored in product_list.txt file
            print("Products In Stock:")
            idx = 1  # it shows index. The first product will be having index 1.
            for line in lines: # will pick each product info one by one (iteration)
                print(f"{idx}. {line.strip()}")
                idx += 1
    type()  # after displaying all products in CONSOLE then type function will be called.


def show_options():  # after calling load_products() function this function will call
    print("Choose an option:")
    print("1. Show Product List")
    print("2. Show Cart")
    print("3. Show History")
    print('4. Remove')
    print('5. Checkout')
    print("6. Exit")
    return input("Enter your choice (1-6): ")  # will ask user for choice


def main():  # this function will allow user to choose options he/she wants.
    filename = "product_list.txt"
    load_products(filename)  # calling this function to create product_list.txt file

    while True:
        choice = show_options()  # here user will choose options.

        if choice == '1':  # if user will choose 1 option then display() function will be called.
            display(filename)  # this will take you to the display()function.
        elif choice == '2':
            show_cart()
        elif choice == '3':
            history()
        elif choice == '4':
            remove_from_cart()
        elif choice == '5':
            checkout()
        elif choice == '6':
            print("THANKYOU FOR SHOPPING!!!\nExiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


def create_account():  # creating a function for creating account(signup)
    username = input("Enter your username, user name should be of 7 or more than 7 character: ")
    password = None
    confirm_password = None
    while True:
        password = input("Enter your password (should be of minimum 7 seven characters): ")
        confirm_password = input("Confirm password: ")
        if len(password) >= 7:
            break
        print("YOUR PASSWORD DOESN'T MEET THE SPECIFIED CRITERIA, PLEASE TRY NEW PASSWORD!")

    now = datetime.now()
    current_date = now.date()
    current_date = str(current_date)
    current_time = now.time()
    current_time = str(current_time)
    if len(username) < 7:
        print("USERNAME TOO SHORT, USERNAME SHOULD BE OF 7 OR MORE THAN 7 CHARACTERS")
        create_account()
    elif os.path.exists(username + '.txt'):
        print("ACCOUNT WITH THIS USERNAME ALREADY EXISTS!")
        create_account()
    elif password == confirm_password:
        print("YOU HAVE SUCCESSFULLY CREATED YOUR ACCOUNT")
        with open('database.txt', 'a') as db:
            db.write(username + "," + password + "\n")
        global file
        file = username + '.txt'
        f = open(file, 'w')  # writing data to file of individual user
        f.write(
            'username : ' + username + '\n' + 'password : ' + password + '\n' + 'account created date : ' + current_date + '\n' + 'account created time : ' + current_time)
        f.close()
        main()
    else:
        print("PASSWORD DOSEN'T MATCH")
        create_account()


def login():  # creating a function for creating account(login)
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    l = []  # initializing empty lists to append usernames and passwords to save in txt file
    l2 = []
    db = open("database.txt", "r")
    for i in db:
        a, b = i.split(",")
        l.append(a)
        l2.append(b)
    data = dict(zip(l, l2))

    now = datetime.now()
    current_date = now.date()
    current_date = str(current_date)
    current_time = now.time()
    current_time = str(current_time)
    if username in data:
        print("login successful")
        global file
        file = username + '.txt'
        f = open(file, 'a')  # writing data to file of individual user
        f.write('\n' + 'account login date : ' + current_date + '\n' + 'account login time : ' + current_time)
        f.close()
        main()
    else:
        print('account does not exist')
        choice()

def choice():  # creating a function for user to ;etting them login or signup to the application
    ch = input("login or signup:")
    ch=ch.lower()
    if ch == "login":
        login()
    elif ch == "signup":
        create_account()
    else:
        print("Invalid choice")
        choice()


def start():
    for i in range(15):
        if i == 0:
            print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t*", end='')
            time.sleep(0.15)
        else:
            print("*", end='')
            time.sleep(0.15)
    time.sleep(0.1)
    print("\n\t\t\t\t\t\t\t\t\t\t\t\t\t*SHOPEASE MALL*")
    for i in range(15):
        if i == 0:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t*", end='')
            time.sleep(0.15)
        else:
            print("*", end='')
            time.sleep(0.15)
    print("\n\t\t\t\t\t\t\t\t\t\t     WELCOME TO OUR MALL, READY TO SHOP?")


start()
choice()

