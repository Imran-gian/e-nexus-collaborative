import sqlite3

from sqlite3 import Error

from flask import Flask
from flask import request
from flask import session
from flask_session import Session
import multiprocessing
import find_email_addresses
from email_scraper import search_email
import send_email
from flask_cors import CORS
from flask import render_template
from werkzeug import secure_filename
import pprint
import json
from json import dumps
from flask import make_response

app = Flask(__name__, static_url_path='/static')
CORS(app)


def create_connection(path):

    connection = None

    try:

        connection = sqlite3.connect(path,timeout=30000.0)

        print("Connection to SQLite DB successful")

    except Error as e:

        print(f"The error '{e}' occurred")


    return connection

def create_store(conn, store):
    """
    Create a new store
    :param conn:
    :param store:
    :return:
    """

    sql = '''INSERT OR REPLACE INTO reseller(website,b_name, country, lat,long,email,status_code, sentiment)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, store)
    conn.commit()

    return cur.lastrowid
def create_biz(conn, biz):
    """
    Create a new biz
    :param conn:
    :param biz:
    :return:
    """

    sql = '''INSERT OR REPLACE INTO bdata(website,b_name, rating, cat, emails)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, biz)
    conn.commit()

    return cur.lastrowid
def update_sentiment(conn, store):
    """
    Create a new store
    :param conn:
    :param store:
    :return:
    """
    
    sql = 'UPDATE reseller set sentiment = '+str(store[1])+' WHERE website = \''+str(store[0])+'\''
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    return cur.lastrowid
def update_status_code(conn, store):
    """
    Create a new store
    :param conn:
    :param store:
    :return:
    """

    sql = 'UPDATE reseller set status_code = '+str(store[1])+' WHERE website = \''+str(store[0])+'\''
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    return cur.lastrowid

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def exec_sql(conn, exec_command):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(exec_command)
    except Error as e:
        print(e)


def send_sql_2_email(websites):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT website FROM reseller")

    rows = cur.fetchall()
    websites = []
    for row in rows:
        if len(row)>0:
            print(row)
            websites.append(row)
    return websites
def reseller_websites(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT website, status_code, sentiment FROM reseller")

    rows = cur.fetchall()
    websites = []
    for row in rows:
        if len(row)>0:
            print(row)
            websites.append(row[0])
    return websites


def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

def resellers_todo(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    print("...")
    cur = conn.cursor()
    cur.execute("SELECT * FROM reseller WHERE status_code = 0")

    rows = cur.fetchall()
    websites = []
    for row in rows:
        if True or len(row)>0:
            print("...",row)
            web = row[0]
            websites.append(row+(biz_info_dump(conn, web)))
    return websites#jsonify(indent=2, sort_keys=False, result=websites)
def biz_info_dump(conn, web):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    print("...")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bdata WHERE website = '"+web+"'")

    rows = cur.fetchall()
    websites = ()
    for row in rows:
        if True or len(row)>0:
            print("...",row)
            websites += row
    return websites
def resellers(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    print("...")
    cur = conn.cursor()
    cur.execute("SELECT * FROM reseller")

    rows = cur.fetchall()
    websites = []
    for row in rows:
        if True or len(row)>0:
            print("...",row)
            websites.append(row)
    return websites




'''
Send get emails from the websites' contact form. This is probably the most important function.

How: look for the contact form via url name ("contact" in the title), then scrape it.

'''
def web_2_email(pump_, conn, websites_data):
    # read data from business database
    emails = []
    for data in websites_data:
        website = data[0]
        bname = data[1]
        country = data[2]
        status_code = int(data[6])
        if status_code == 0:
            pass
        else:
            continue
        email = []
        ''' Find any emails in the contact forms.
        - look for an email.
        - if the email does not exist, then just add a placeholder of value "email"
        - if the email does exist, then add it to the list of emails.
        '''
        try:
            email = search_email(website)
        except:
            send_email_(pump_, bname, country, website, "email")
            continue
        if((email  is None) or (len(email)==0)):
            send_email_(pump_, bname, country, website, "email")
            continue
        print(bname, country, website, email)
        send_email_(pump_, bname, country, website, email)
        emails.append(email)
    return emails

'''
Send the emails to any businesses in the database.

'''
def send_email_(pump_, bname, country, website, receiver_email):
    #receiver_email = next(iter(receiver_email))
    #receiver_email = "garadadil@gmail.com"
    
    try:
        # use your email service provider's servers to send a message automatically to recipient.
        send_email.send_email(receiver_email, bname, country)
    except:
        pass
    # Update the database to let it know that an email was sent to a certain recipient.
    pump_.email_sent(website,1)
    return "email sent successfully to: " +  str(receiver_email)

create_reseller_table = '''
CREATE TABLE IF NOT EXISTS reseller (
	website text PRIMARY KEY,
	b_name text NOT NULL,
	country text NOT NULL,
        lat float NOT NULL,
        long float NOT NULL,
	email text NOT NULL,
        status_code integer NOT NULL,
        sentiment integer NOT NULL
);
'''
create_bdata_table = '''
CREATE TABLE IF NOT EXISTS bdata (
	website text PRIMARY KEY,
	b_name text NOT NULL,
	rating text NOT NULL,
	cat text NOT NULL,
	emails text NOT NULL
);
'''

#create_store(conn, store0)


#exec_sql(conn, "drop table reseller")
from io import StringIO
import csv
from flask import make_response
'''
Create the upload page.

How: serve an html file.

'''
@app.route('/', methods = ['GET', 'POST'])
def upload_page():
   return app.send_static_file('upload.html')
	
'''
upload the file to populate the sql databse.

How: Read the business names (bname field) and the website from the output FROM THE CHROME EXTENSION.
Then add it to the sql database. 

'''
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':

      # Just read the json file (the output from the ENC chrome extension)

      f = request.files['file']
      fname = secure_filename(f.filename)
      f.save(fname)

      # Time to parse the json from the input file

      with open(fname) as f:
        d = json.loads(f.read())
        ret = ""
        for site in d:
            web = site['website']
            try:
                bname = site['bname'].split("\n")[0] 
            except:
                pass
            try:
                review = site['bname'].split("\n")[1] 
            except:
                pass
            try:
                cat = site['bname'].split("\n")[2] 
            except:
                pass
    
            print("evaluating: '", web)
            ems = ''
            

            try:
                emails = search_email('http://'+web)
                for e in emails:
                    ems += ','+e
            except Exception as e:
                print("ERROR: ", e)
                continue
            
            # add fields to touples that are going to be used in the sql database.
            store = (web, bname, 'country',0,0,ems, 0,0)
            biz = (web, bname, review,cat, ems)
            ret += '<br>Business: '+str(biz)

            # open the sql database and add data from the input file.
            pump = Pump()
            pump.create_store_(store)
            pump.create_biz_(biz)

        return ret
      return 'file uploaded successfully'

'''
Create a reseller. This is the "seller" in the collaboration agreement between two businesses


How: put all parameters into a touple and append that touple to the appropriate database

params: 
- website: the website of the business found on google maps (required)
- bname: the actual name of the business .. (required)
- country: the country .. (optional)
- lat: the latitude .. (optional)
- long: the longitude .. (optional)


'''
@app.route('/new_reseller', methods = ['GET'])
def new_reseller():
    pump = Pump()
    website = str(request.args.get('website').strip())
    bname = str(request.args.get('bname').strip())
    country = str(request.args.get('country').strip())
    lat = float(request.args.get('lat').strip())
    lon = float(request.args.get('long').strip())
    return str(pump.sql_in(website, bname, country, lat, lat))
'''
Update whether or not the email has been sent.


How: put all parameters into a touple and append that touple to the appropriate database

params: 
- website: the website of the business found on google maps (required)
- status_code: Whether or not the email has been sent. (required)
'''
@app.route('/email_sent', methods = ['GET'])
def email_sent():
    pump = Pump()
    website = str(request.args.get('website').strip())
    status_code = int(request.args.get('status_code').strip())
    return str(pump.email_sent(website, status_code))

'''
Update how positive (or negative) the email response was (from the other business)


How: put all parameters into a touple and append that touple to the appropriate database

params: 
- website: the website of the business found on google maps (required)
- sentiment: The positivity index of the email response. (required)
'''
@app.route('/sentiment', methods = ['GET'])
def sentiment():
    pump = Pump()
    website = str(request.args.get('website').strip())
    sentiment = int(request.args.get('sentiment').strip())
    return str(pump.sentiment(website, sentiment))

'''
Export all the business data into a neat CSV that you can import to MailChimp to have all the businesses recieve your email campaign.


How: Dump the root table in the database and then parse to make a readable CSV.

'''
@app.route('/sql_dump.csv', methods = ['GET'])
def sql_dump():
    pump = Pump()
    data = pump.sql_dump()
    # now we will open a file for writing 
    data_file = open('static/data_file.csv', 'w+') 
  
    # create the csv writer object 
    csv_writer = csv.writer(data_file, delimiter=',') 
  
    # Counter variable used for writing  
    # headers to the CSV file 
    count = 0
  
    for emp in data: 
        if count == 0: 
            # Writing headers of CSV file 
            header = emp
            csv_writer.writerow(header) 
            count += 1
  
        # Writing data of CSV file 
        row = []
        for c in emp:
            print(c)
            d = str(c).replace(",", " ")
            row.append(d)
            print(d)
        csv_writer.writerow(row) 
  
    data_file.close() 
    return app.send_static_file('data_file.csv')

'''
Send a collaboration invitation to all the businesses in the database.


How: Depreciated. You should use MailChimp to do this and this program exports to a csv as for MailChimp as well.

'''

@app.route('/sendall', methods = ['GET'])
def sendall():
    pump = Pump()
    return str(pump.sendall())


'''
This is just a simple class that takes any arguments and outputs them into their appropriate SQL table and column.


'''
class Pump:
    def create_biz_(self, biz):
        create_biz(self.conn, biz)
    def sql_in(self, website, bname, country, lat, lon):
        #self.sql_init()

        store_0 = (website, bname, country, lat, lon, 'email',0,0)
        create_store(self.conn, store_0)
        return
    def create_store_(self, store_0):
        #self.sql_init()

        create_store(self.conn, store_0)
        return
    def email_sent(self, website,status_code):
        #self.sql_init()
        
    
        store_0 = [website,status_code]
        update_status_code(self.conn, store_0)
        return
    def sentiment(self, website, sentiment):
        #self.sql_init()
        
    
        store_0 = [website, sentiment]
        update_sentiment(self.conn, store_0)
        return
    def sendall(self):
        #self.sql_init()
        
        websites_data = resellers(self.conn)
        emails = web_2_email(self, self.conn, websites_data)
        
        return emails
    def sql_dump(self):
        #self.sql_init()
        return resellers_todo(self.conn)
    def __init__(self):
        self.conn = create_connection('./sb_test.db')
        # create tables
        if self.conn is not None:
            # create projects table
            create_table(self.conn, create_bdata_table)

            # create tasks table
            create_table(self.conn, create_reseller_table)
        else:
            print("Error! cannot create the database connection.")
        #store_0 = ('https://website.com', 'business', 'Country', 0, 0, 'email',0,0)
        #create_store(self.conn, store_0)
if __name__ == '__main__':
    
    
    pump = Pump()
    app.run(host='0.0.0.0', port=5003)
    





