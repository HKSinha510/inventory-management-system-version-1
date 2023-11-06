from main import connection
from datetime import datetime  #date time for convertion

def stnd_date(input_date:str, input_format:str = "%d-%m-%Y", output_format:str = "%Y-%m-%d") -> str:  #convert_to_standard_date
    '''Convert any date format to standard date'''
    # Parse input date string to datetime object
    parsed_date = datetime.strptime(input_date, input_format)

    # Convert datetime object to desired output format
    standard_date = parsed_date.strftime(output_format)

    return standard_date

def check_database(cur) -> None:
    '''
    This function check database and tables.\n
    This function will make sure that the db and tables exists and are empty before entering any data.\n

    :mod:`mysql_conenction`: mysql connector data pool
    '''
    DB = "shop"
    TABLES = ["orders", "inventory", "employee"]
    CREATE_TABLE = {"orders": "CREATE TABLE orders(orderid VARCHAR(255) NOT NULL, consumer_name VARCHAR(255) NOT NULL, consumer_phnno bigint NOT NULL, consumer_address varchar(255), order_item json NOT NULL, total_amount INT NOT NULL, base_amount INT NOT NULL);", "inventory": "CREATE TABLE inventory(product_id VARCHAR(50) UNIQUE PRIMARY KEY NOT NULL, name VARCHAR(250) UNIQUE, in_stock INT NOT NULL, expiry DATE, rate INT NOT NULL, gst SMALLINT, manufacturer VARCHAR(200));", "employee": "CREATE TABLE employee(emp_id VARCHAR(255) PRIMARY KEY NOT NULL, name VARCHAR(128) UNIQUE, slary INT, dsgn VARCHAR(128), dpmt VARCHAR(128), phno BIGINT NOT NULL, age INT NOT NULL, dob DATE NOT NULL, address VARCHAR(255), benifit INT);"}
    DATABASE_EXIST = False
    TABLES_EXIST = False        #VARIABLE ARE NAMED SIMMILAR, BUT THEY POTRAIT DIFEERENT CHARACTER/PROPERTIES IN TERMS 

    if len(TABLES) != len(CREATE_TABLE): raise Exception("Table tally check failed\nlength of `TABLES` and `CREATE_TABLE` is not same") 

    cur.execute("SHOW DATABASES;")  #CHEKING DATABASE
    for i in cur.fetchall():
        if DB in i[0]:
            DATABASE_EXIST = True
            cur.execute(f"USE {DB};")

    if not DATABASE_EXIST:
        cur.execute(f"CREATE DATABASE {DB};")
        cur.fetchall()
        cur.execute(f"USE {DB};")
        cur.fetchall()

    #CHEKING TABLES
    cur.execute("SHOW TABLES;")
    temp_list_of_tables = []
    list_of_table_in_db = cur.fetchall()
    for i in list_of_table_in_db:
        if list_of_table_in_db != "":
            TABLES_EXIST = True
            temp_list_of_tables.append(str(i[0]))

    #checking if the tables in database are same as what we need
    if set(temp_list_of_tables) == set(TABLES): #if yes, then clear the data of the table
        for i in temp_list_of_tables:
            
            cur.execute(f"delete from {i};")
            cur.fetchall()
    else: #delete exisiting table and create new table for data to be entered in insert_data()
        if TABLES_EXIST:        #cheking in table exists in db, if yes then remove the tables, 
            for i in temp_list_of_tables:
                cur.execute(f"drop table {i}")           #then make new tables

        #creating new tables
        for i in TABLES:
            cur.execute(CREATE_TABLE[i])


def insert_data(FILENAME : str = "data.csv", MODE : str = 'a'): 
    '''This function is used to make and insert data in a database.
Use this function when there is no data to use the program, as this program requires some data to perform activities. Using this function you can get a sample database\nCAUTION: if a database with name `shop` exists then it will be cleared and new data will be inserted

MODE = 'a' for automatic, i for inventory, o for order & e for employee table'''

    status = False
    #table = 'inventory' if MODE == 'i' else 'orders' if MODE == 'o' else 'employee'

    con, cur = connection('myseql')

    check_database(cur)

    path = f"bin/{FILENAME}"
    data = open(path, 'r').read().split('\n')

    if len(data) != 1:
        #data  nt corrupedd       
        for i in data:
            if i != '':
                #checks for null, check for table
                if MODE == 'i':
                    data_table = i.split(',')
                    pid, name, stk, epry, rate, gst, mnftr = data_table
                    query = f"INSERT INTO inventory VALUES(%s, %s, %s, %s, %s, %s, %s);"

                    # Prepare the parameter values
                    params = (pid, name or None, stk, epry or None, rate, gst or None, mnftr or None)

                elif MODE == 'o':
                    data_table = i.split(',')
                    s = data_table
                    query = f"INSERT INTO orders VALUES(%s, %s, %s, %s, %s, %s, %s);"

                    # Prepare the parameter values
                    params = ()

                elif MODE == 'e':
                    data_table = i.split(',')
                    emp_id, name, salary, designation, department, phno, age, dob, address, benifits = data_table
                    query = f"INSERT INTO employee VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

                    # Prepare the parameter values
                    params = (emp_id, name or None, salary or None, designation or None, department or None, phno, age, stnd_date(dob), address or None, benifits or None)

                # Execute the query with parameters
                cur.execute(query, params)
                
            
        con.commit()    
        con.close()
        status = True
        return ('Clear' if status else 'Failed')

    else:
        try:
            print('f')
            print(data) #close connection and return
        except:
            pass #return, connection doesnot exist

if __name__ == '__main__':
    print(insert_data('data.csv', 'i'))