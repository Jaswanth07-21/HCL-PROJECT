from json import JSONEncoder
from flask import *
import mysql.connector
from flask_cors import CORS
from datetime import datetime
from flask_sessionstore import Session
import pandas as pd
mydb = mysql.connector.connect(user = 'root',port = 3306,database ='livechart')
cur = mydb.cursor()

app = Flask(__name__)
app.secret_key = "jai balayya"
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin",methods=["POST","GET"])
def signin():
    global email
    if request.method == "POST":
        email = request.form['useremail']
        session['useremail'] = email
        print(session['useremail'])

        password= request.form['password']
        sql = "select * from userdata where UserEmail = '%s' and Password ='%s'"%(email,password)
        cur.execute(sql)
        d = cur.fetchall()
        mydb.commit()

        if d == []:
            msg = "Invalid Credentials"
            return render_template("signin.html",msg=msg)
        else:
            return render_template("userhome.html",useremail = d[0][2])
    return render_template("signin.html")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        f = request.form
        name = f['name']
        useremail =  f['useremail']
        age = f['age']
        contact = f['contact']
        password = f['password']
        confirmpassword = f['confirmpassword']
        sql = "select * from userdata where UserEmail = '%s' and Password = '%s'"%(useremail,password)
        cur.execute(sql)
        d= cur.fetchall()
        mydb.commit()

        if password == confirmpassword :
            if d  == []:

                sql= "insert into userdata(UserName,userEmail,Age,Contact,Password)values(%s,%s,%s,%s,%s)"
                values = (name,useremail,age,contact,password)
                cur.execute(sql,values)
                mydb.commit()
                return render_template("signin.html")
            else:
                msg="Password and confirm password not matched"
            return render_template("signup.html",msg=msg)
        else:
            msg="details already exists"
            return render_template("signup.html",msg=msg)


    return render_template("signup.html")

@app.route("/chat")
def chat():
    sql="select * from usermessages"
    cur.execute(sql)
    d = cur.fetchall()
    mydb.commit()
    sql="select UserName from userdata"
    cur.execute(sql)
    dc = cur.fetchall()
    mydb.commit()
    return render_template("chat.html",dd = d,useremail = email,names=dc)

@app.route("/getdata")
def temp():
    sql="select * from usermessages"
    cur.execute(sql)
    d = cur.fetchall()
    # d =pd.read_sql_query(sql,mydb)
    mydb.commit()
    return jsonify(d)

@app.route("/chat1")
def chat1():
    msg = request.args.to_dict()['result']
    ti = datetime.today().strftime("%H:%M %p")
    print(msg)
    print(email)
    sql="insert into usermessages(Email,Message,Time) values ('%s','%s','%s')"%(email,msg,ti)
    cur.execute(sql)
    mydb.commit()
    # return msg
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(debug = True)