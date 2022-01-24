from flask import Flask
from flask import jsonify
import requests
import psycopg2
import json
import datetime as dt
import psycopg2.extras
conn = psycopg2.connect('')
##cur=conn.cursor()

app = Flask(__name__) 

cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
@app.route('/pwd=<var>/name=<name>/unreadmessage')
def h2(var,name):
    if var=='1234':
##        cur=conn.cursor()
        cur.execute(f"select * from storage where seen = 0 and rname='{name}'")
        vr=cur.fetchall()
        
        for inf in vr:
            sn=inf[0]
            cur.execute(f"update storage set seen=1 where sno ='{sn}'")
            conn.commit()
        vr=json.loads(vr)
        return str(vr);
##m=''
##
@app.route('/pwd=<var>/newmessage/<sen>/<rec>')
def k1(var,sen,rec):
    if var=='1234':
        cur.execute(f"select sno,msg,sname,rname from storage where seen=0 and sname='{sen}' and rname='{rec}'")
        vr=cur.fetchall()
        for i in vr:
            cur.execute(f"update storage set seen=1 where sno={i[0]} and sname='{i[2]}' and rname='{i[3]}'")
            conn.commit()
        return jsonify(vr);


@app.route('/pwd=<var>/allmessage')
def a1(var):
    if var=='1234':
##        cur=conn.cursor()
        cur.execute('select msg,sname,rname from storage')
        vr=cur.fetchall()
        
        return jsonify(vr);


@app.route('/pwd=<var>/add_username=<usr>')
def d1(var,usr):
    if var=='1234':
        cur.execute(f"insert into storage (uname) values('{usr}')")
        conn.commit()
    return str(usr);
@app.route('/pwd=<var>/username')
def c1(var):
    if var=='1234':
        cur.execute('select uname from storage where uname is not null')
        vr=cur.fetchall()
        return jsonify(vr);
@app.route('/pwd=<var>/conversation/<name1>/<name2>')
def b1(var,name1,name2):
    if var=='1234':
        
##        cur=conn.cursor()
        cur.execute(f"select msg,sname,rname from storage where (sname='{name1}' and rname='{name2}') or (sname='{name2}' and rname='{name1}')")
##        cur.execute           
        
        vr=cur.fetchall()
        return jsonify(vr);
    
    
d=[]
##e=[]
##f=[]
b=''
@app.route('/pwd=<var>/<frm>/<msg>/to/<rec>')
def h3(var,frm,msg,rec):
    global b
##    di={}
##    cur.execute('select sname from storage')
##    sn=cur.fetchall()
##    global m
    a=dt.datetime.now()
    if var=='1234':
        b=a.strftime('%d')+'-'+a.strftime('%b')+'  '+a.strftime('%H')+':'+a.strftime('%M')
##        cur=conn.cursor()
        cur.execute('select uname from storage')
    
        un=cur.fetchall()
        for i in un:
            for j in i:
                d.append(j)
##        d=tuple(d)    
##        return d;
##        cur.execute('select sno from storage')
##        s=cur.fetchall()
        if frm in d:
            
            cur.execute(f'''insert into storage (sno,msg,sname,rname,seen,time) values (default,'{msg}','{frm}','{rec}','0','{b}')''')
            conn.commit()
            return msg+" sent to "+rec+" at "+b;
##            cur.execute('select * from storage where seen = 0')
##            conn.commit()
##            vr=cur.fetchall()
##            for inf in vr:
##                sn=inf[0]
##                cur.execute(f'update storage set seen=1 where sno ={sn}')
##            conn.commit()
##
##            return str(vr)
        
        else:
            return 'error';

    else:
        return 'wrong password';
           
             
   
 
##    di['from']=frm
##    di['to']=rec
##    di['msg']=v
##    return str(di);
  
if __name__ =='__main__':  
    app.run(debug = True)

