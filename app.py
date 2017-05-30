from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import time 
import redis

r = redis.Redis(host='redis',port=6379)

import socket
ip = socket.gethostname()

app = Flask(__name__)

@app.route('/')
def index():
    note=''
    if 'uid' in request.cookies:
        note=getNote(request.cookies['uid']).decode("utf-8")
    return render_template('index.html',name=str(ip),note=note)

@app.route('/note',methods=['GET','POST'])
def note():
    if request.method == 'POST':
        request.get_data()
        note = request.data
        resp = make_response('ok')
        uid = 'x'
        if 'uid' not in request.cookies:
            uid = str("%.20f" % time.time())
            resp.set_cookie('uid',uid)
            print("UID: "+uid)
        else:
            uid = request.cookies['uid']
        setNote(uid,note)
        return resp
    else:
        if 'uid' in request.cookies:
            res = getNote(request.cookies['uid'])
            if res == None:
                return ''
            return res
        else:
            return ''

def setNote(uid, note):
    r.set(uid,note)

def getNote(uid):
    return r.get(uid)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
