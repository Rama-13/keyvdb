

from flask import Flask, request
from keyvdb_restful import keyvDB

app = Flask(__name__)

keyvdb = keyvDB()



@app.route("/hello/<string:name>")
def hello(name):
    return keyvdb.greet(name)

@app.route("/greet/")
def greet():
    return keyvdb.get_keys()


# keyvdb.set_key()

# request.form.get('value')
# request.args.get('prefix', '')
# if 'prefix' in request.args

if __name__=="__main__":
    app.run(host='0.0.0.0', port=7000, debug=True, threaded=True)