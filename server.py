from flask import Flask,render_template,request
from flask import json as fJson
from flaskext.mysql import MySQL
import secrets
import json


secret_key = secrets.token_hex(16)


mysql = MySQL()
app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = "new_password"
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/',methods=['GET','POST'])
def index():
   if request.method=='POST':
      name=request.form['uname']
      username=request.form['userName']
      passw=request.form['userPassword']
      conctn=mysql.connect()
      db=conctn.cursor()
      db.execute('INSERT INTO USERS VALUES(%s,%s,%s)',(name,username,passw))
      conctn.commit()
      db.close()
      return render_template('index.html')

   return render_template('index.html')

@app.route('/signup.html',methods=['GET','POST'])
def newuser():
   return render_template('signup.html')

@app.route('/login.html',methods=['GET','POST'])
def login():

   return render_template('login.html')


@app.route('/fileload.html',methods=['GET','POST'])
def fileload():

   if request.method=='POST':
      username=request.form['userName']
      passw=request.form['userPassword']
      conctn=mysql.connect()
      db=conctn.cursor()
      db.execute("SELECT * FROM USERS where username='"+username+"' and passw='"+passw+"'")  # For Selection
      cnt=db.rowcount
      db.close()
      if cnt==0:
         error = "Sorry but the username or password you entered is wrong "
         return error
      elif cnt==1:
         return render_template('fileload.html',username=username)
      else:
         return "More than 1 user presents"


   return render_template('fileload.html')

@app.route('/result.html', methods = ['GET', 'POST'])
def res():
   if request.method == 'POST':
      f = request.files['jsonfile']
      fin=open(f.filename,'r')
      array=json.loads(fin.read())

      conctn=mysql.connect()
      db=conctn.cursor()
      for i in array: 
         userId=str(i["userId"])
         uid=str(i["id"])
         title=i["title"]
         body=i["body"]
         db.execute('INSERT INTO JSON_FILE VALUES(%s,%s,%s,%s)',(userId,uid,title,body))
         conctn.commit()
      db.close()
      msg='Data successfully Uploaded'
      return render_template('result.html',msg=msg)


@app.route('/jsondata.html', methods = ['GET', 'POST'])
def getData():
   if request.method == 'POST':
      conctn=mysql.connect()
      db=conctn.cursor()
      users=db.execute("SELECT * FROM JSON_FILE") 
      if users>0:
         userData=db.fetchall()
         db.close()
         return render_template('jsondata.html',userData=userData)
    	
if __name__ == '__main__':
   app.run(debug=True)

