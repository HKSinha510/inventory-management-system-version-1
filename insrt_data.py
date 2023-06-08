from main import connection
from datetime import datetime  #date time for convertion

def stnd_date(input_date:str, input_format:str = "%d-%m-%Y", output_format:str = "%Y-%m-%d") -> str:  #convert_to_standard_date
    '''Convert any date format to standard date'''
    # Parse input date string to datetime object
    parsed_date = datetime.strptime(input_date, input_format)

    # Convert datetime object to desired output format
    standard_date = parsed_date.strftime(output_format)

    return standard_date


def insert_data(FILENAME : str, MODE : str = 'a'): 
    '''This function is used to make and insert data in a database.
Use this function when there is no data to use the program, as this program requires some data to perform activities. Using this function you can get a sample database\nCAUTION: if a database with name `shop` exists then it will be cleared and new data will be inserted

MODE = 'a' for automatic, i for inventory, o for order & e for employee table'''

    status = False
    # Todo 1) add logik to remove and recreate table if it exisits in future, 2) set up auto
    #table = 'inventory' if MODE == 'i' else 'orders' if MODE == 'o' else 'employee'

    path = f"bin/{FILENAME}"
    data = open(path, 'r').read().split('\n')
    if len(data) != 1:
        #data  nt corrupedd
        con = connection('myseql', db='shop')
        cur = con.cursor()
       
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
    #insert_data()
    print(insert_data('data.csv', 'i'))