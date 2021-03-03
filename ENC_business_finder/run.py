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
from json import dumps
from flask import make_response

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
def web_2_email(pump_, conn, websites_data):
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
def send_email_(pump_, bname, country, website, receiver_email):
    #receiver_email = next(iter(receiver_email))
    #receiver_email = "garadadil@gmail.com"
    
    try:
        send_email.send_email(receiver_email, bname, country)
    except:
        pass
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


@app.route('/upload', methods = ['GET', 'POST'])
def upload_page():
   return app.send_static_file('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fname = secure_filename(f.filename)
      f.save(fname)
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
            store = (web, bname, 'country',0,0,ems, 0,0)
            biz = (web, bname, review,cat, ems)
            ret += '<br>Business: '+str(biz)
            pump = Pump()
            pump.create_store_(store)
            pump.create_biz_(biz)

        return ret
      return 'file uploaded successfully'
@app.route('/home', methods = ['GET', 'POST'])
def home():
    return app.send_static_file('index.html')
@app.route('/new_reseller', methods = ['GET'])
def hello():
    pump = Pump()
    website = str(request.args.get('website').strip())
    bname = str(request.args.get('bname').strip())
    country = str(request.args.get('country').strip())
    lat = float(request.args.get('lat').strip())
    lon = float(request.args.get('long').strip())
    return str(pump.sql_in(website, bname, country, lat, lat))
@app.route('/email_sent', methods = ['GET'])
def email_sent():
    pump = Pump()
    website = str(request.args.get('website').strip())
    status_code = int(request.args.get('status_code').strip())
    return str(pump.email_sent(website, status_code))
@app.route('/sentiment', methods = ['GET'])
def sentiment():
    pump = Pump()
    website = str(request.args.get('website').strip())
    sentiment = int(request.args.get('sentiment').strip())
    return str(pump.sentiment(website, sentiment))
@app.route('/sql_dump', methods = ['GET'])
def sql_dump():
    pump = Pump()
    return str(pump.sql_dump())
@app.route('/sendall', methods = ['GET'])
def sendall():
    pump = Pump()
    return str(pump.sendall())



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
    





