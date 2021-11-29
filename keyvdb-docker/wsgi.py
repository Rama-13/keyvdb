from gevent import monkey
monkey.patch_all()
from keyvdb import app

if __name__=="__main__":
    app.run(host='0.0.0.0', port=7000, debug=False, threaded=True)