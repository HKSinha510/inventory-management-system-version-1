'''
main.py
main file
'''
# TODO: add debug log, if debug set to true then print the step
# 2) write a check for system date, because orderid uses sysdate(), if system date will be incorerct it will mess up whole system
# 3) line 17, will possible have to rewrite many lines
# 4) if gui fails, then at least add color text

import json
import mysql.connector as ms
from tabulate import tabulate

def connection(password:str, host:str = 'localhost', user:str = 'root', db:str = None):  # use .is_connected to get status, if status == False then restart
    #print things only when debug set to true, because when running in program, it interupt between session
    try:
        cnx = ms.connect(host = host, user = user, passwd=password, database = db)
        print('Connection established!')

        return cnx #also return cursor, so in case of error it won't error up
    
    except ms.Error as err:
        if err.errno == ms.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == ms.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
    

def place_order(cons_name:str, phno:int, list_of_products:dict, address:str = None):   #lop ==>  {proid: number of item, proid2: number of item}
    con = connection('myseql', db='shop')
    cur = con.cursor()

    cur.execute('select * from inventory')
    data = cur.fetchall()

    copy_lop = list_of_products.copy()
    items = {}

    #sorting data to use it for checks
    for item in data:
        pid, name, stock, expiry, rate, gst, mnftr = item
        if stock:
            items[pid] = [name, stock, expiry, rate, gst, mnftr]

    order_id = "REPLACE(REPLACE(REPLACE(SYSDATE(), '-', ''), ':', ''), ' ', '')"

    total_amount = 0
    base_amount = 0
    
    #performing activity using products
    for product in copy_lop: 
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
    print(query)
    cur.execute(query)
    con.commit()

    con.close()

def give_data():
    con = connection('myseql', db='shop')
    cur = con.cursor()

    cur.execute('select * from inventory')
    data = cur.fetchall()

    items = {}

    #sorting data to use it for checks
    for item in data:
        pid, name, stock, expiry, rate, gst, mnftr = item
        if stock:
            items[pid] = [name, stock, expiry, rate, gst, mnftr]

    return items

def perform_action(ipt):
    while ipt != '2':
        if ipt == '1':
            lst = give_data()
            header = ["Product ID", "Product Name", "Price"]
            table = []
            for product in lst:
                table.append([product,lst[product][0],lst[product][3]])

            print(tabulate(table, header, tablefmt="pretty"))

        elif ipt == '3':
            print("Made Using Python🐍, by Hardik")

        elif ipt == '4':
            return

        else:
            print("Please enter a valid number")

        ipt = input("Available action(use numbers to select):\n1: View Items\n2: Place Order\n3: Credits\n4: Exit\nAction:")

    print("To place Order Enter Product Id and then the quantity of that product")

    while True:
        pid = input("Enter Product Id: ")
        quantity = input(f"Quantity of {give_data()[pid.upper()][0]}: ")

        print(pid, quantity)

        ask = input("Enter to Continue, b for billing")
        if ask == 'b': break
    
def admin(): #admin commands, direct access to database and table, eval access for direct interpretation of code
    pass

if __name__ == '__main__': 
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