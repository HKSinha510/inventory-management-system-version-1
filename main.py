'''
main.py
main file
'''
# TODO: add debug log, if debug set to true then print the step
# 2) write a check for system date, because orderid uses sysdate(), if system date will be incorerct it will mess up whole system
# 3) line 17, will possible have to rewrite many lines
# 4) if gui fails, then at least add colored text

import json
from time import sleep
import os
from tkinter import messagebox

#Checking & installing external modules
a = 0
while a < 3:
    try:
        import mysql.connector as ms
        from tabulate import tabulate
        break
        
    except ImportError as e:
        print("Press 'OK' in the dialog box.")
        messagebox.showwarning("Import Error", f"Module not found\n{e}\n\nClick OK to install module")
        os.system("pip install tabulate")
        os.system("pip install mysql-connector-python")
        os.system("cls")
        a += 1
    
else:
    os._exit(0)

def connection(password:str, host:str = 'localhost', user:str = 'root', db:str = None):  # use .is_connected to get status, if status == False then restart
    #print things only when debug set to true, because when running in program, it interupt between session
    try:
        cnx = ms.connect(host = host, user = user, passwd=password, database = db)
        cur = cnx.cursor()
        # print('Connection established!')

        return cnx, cur
    
    except ms.Error as err:
        if err.errno == ms.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == ms.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def place_order(cons_name:str, phno:int, address:str = None):   #lop ==>  {proid: number of item, proid2: number of item}
    #configure the whole 2) place order in this function
    con, cur = connection('myseql', db='shop')

    items = give_items()

    order_id = "REPLACE(REPLACE(REPLACE(SYSDATE(), '-', ''), ':', ''), ' ', '')"
    #add sleep(1) or else 2 order can have same order_id
    
    #performing activity using products
    print("+++++++++++ SELF BILLING WIZARD +++++++++++")
    print("b: billing\ne:exit the wizard")

    ordered_item = {}

    while True:
        print()
        opid = input("Enter Product ID: ").upper()
        if opid != 'B' and opid != 'B':
            if opid in items:
                q = int(input(f'Quantity for "{items[opid][0]}": '))
                if q <= items[opid][1]:
                    #pid = rate, quantity, cost, gst, cost with taxes
                    rate = items[opid][3]
                    cost = rate * q
                    gst = items[opid][4]/100
                    cost_with_tax = cost + (cost * gst)
                    ordered_item[opid] = [rate, q, cost, gst, cost_with_tax]
#!issue date says none
                else:
                    print(f"There are only {items[opid][1]} {items[opid][0]} remaining in our stock. Sorry we can't proceed with your request.")

            else:
                print(f"product id {opid} not found. \nPlease check and enter again.")

        elif opid == "B":
            total_amount = 0
            total_amount_with_taxes = 0
            print("Making you bill. Please wait...")
            #sleep(1) i think all this computation with account for 1 sec
            for item in ordered_item:
                total_amount += ordered_item[item][2]
                total_amount_with_taxes += ordered_item[item][-1]

            table = []
            sqlset = {}
            l = 0
            for i in ordered_item:
                tmp = [items[i][0]]
                sqlset[i] = ordered_item[i][1]
                l = len(items[i][0])
                for j in ordered_item[i]:
                    tmp.append(j)

                table.append(tmp)
            table.append(["_"*l, "______", "__________", "______", "______", "___________"])
            table.append(["", "", "Total Cost:", total_amount, "", ""])
            table.append(["_"*l, "______", "__________", "______", "______", "___________"])
            table.append(["", "", "", "", "Total Cost\n(including tax)", total_amount_with_taxes])

            header = ["name", "rate", "quantity", "cost", "gst", "cost with taxes"]

            print(tabulate(table, header, tablefmt="pretty"))
            print()
            print(f"Grand Total: {total_amount_with_taxes}Rs.")

            i = input("Press enter to continue with payment, c to cancel order")
            if i != "c":
                print()
                print("Payment Done!")

                query = f"INSERT INTO orders VALUES({order_id}, '{cons_name}', {phno}, '{address or None}', '{json.dumps(sqlset)}', {total_amount_with_taxes}, {total_amount})"
                cur.execute(query)
                con.commit()
                print()
                print("Order placed!")
                print()
            
            return

        else:
            a = input("are you sure you want to close the wizard?(y/n)").lower()
            if a == "y":
                return
            else:
                continue

    """
    for product in list_of_products: 
        if product in items:    #checking if product is listed in database, if stock = 0 then product will not be listed
            if list_of_products[product] <= items[product][1]:   #checking if stock is avaible 
                #product is avaiable
                cost = items[product][3] + (items[product][3] * (items[product][4]/100))
                total_amount += cost * list_of_products[product] #list_of_products[product] means the amount, like 2 
                base_amount += items[product][3] * list_of_products[product]

            else:
                #use bool to ask for each loop,
                #instead do doing it in this loop, subtract the product avaible from list_of_product to be what is in_stock
                #TODO: ask if less is good, eg ordered 2 and 1 avaible, then ask if 1 is ok 
                print("product is short on stock, the amount you've entred in not avaaible")
        
        else:
            list_of_products.pop(product)
            print(f'Product({product}) not found')

    query = f"INSERT INTO orders VALUES({order_id}, '{cons_name}', {phno}, '{address or None}', '{json.dumps(list_of_products)}', {total_amount}, {base_amount})"
    cur.execute(query)
    con.commit()

    con.close()"""

def give_items():
    con, cur = connection('myseql', db='shop')
    #cur = con.cursor()

    cur.execute('select * from inventory')
    data = cur.fetchall()

    items = {}

    #sorting data to use it for checks
    for item in data:
        pid, name, stock, expiry, rate, gst, mnftr = item
        if stock:       #this elimates item with no stock
            items[pid] = [name, stock, expiry, rate, gst, mnftr]

    return items

def perform_action(ipt):
    if ipt == '1':
        lst = give_items()
        header = ["Product ID", "Product Name", "Price"]
        table = []
        for product in lst:
            table.append([product,lst[product][0],lst[product][3]])

        print(tabulate(table, header, tablefmt="pretty"))

    elif ipt == '2':
        place_order(name, phno, address)

    elif ipt == '3':
        print("Made Using Python🐍, by Hardik")

    elif ipt == '4':
        return

    else:
        print("Please enter a valid number")

    #ipt = input("Available action(use numbers to select):\n1: View Items\n2: Place Order\n3: Credits\n4: Exit\nAction:")
    
def admin(): #admin commands, direct access to database and table, eval access for direct interpretation of code
    pswd = input("Enter password: ")
    if pswd:
        while True:
            adm = int(input("0, 1"))
            if not adm:
                print("Eval")
                text = input("Enter text for evalution: ")
                eval(text)
        
            elif adm:
                print("db access")
                con, cur = connection('myseql', db="shop")
                #cur = con.cursor()

                query = input("query: ")
                cur.execute(query)
                try:
                    print(cur.fetchall())
                except:
                    pass

            else:
                return

if __name__ == '__main__': 
    print("SHOP MANAGEMENT SYSTEM")
    print("Made by Hardik Kumar Sinha - XII")
    print()
    inner_loop = True
    while True:
        while inner_loop:
            name = input('Enter your name: ')
            if name == 'HKSinha5100':
                admin()
                break
            phno = int(input('Enter your Phone Number(10 Digits): '))
            address = input('Enter your address(optional, enter to skip): ')
            action = input("Available action(use numbers to select):\n1: View Items\n2: Place Order\n3: Credits\nAction: ")
            perform_action(action)
            inner_loop = False
        q = input('Press Enter to continue...\n\n')
        inner_loop = True
        
    #place_order('raju', 9927368361, {"ET04": 1, "EM03":1})