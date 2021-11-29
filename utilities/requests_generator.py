
"""Creates random /get/ and /set/ requests for a given hostname"""


import requests
import threading
import secrets
import string
  


def function(n):
    from random import randrange, randint
    mydict = {generate_random_string(10)+str(i):generate_random_string(10) for i in range(n)}
    mydict['key'+str(randint(0,n-1))] = 'value3'
    return mydict

def generate_random_string(n):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))

def req_func(n, hostname):
    for key, value in function(n).items():
        response = requests.post(f"http://{hostname}/set/{key}", data={"value" : value})
        get_response = requests.get(f"http://{hostname}/get/{key}")
        print(response)
        print(get_response)

if __name__ == "__main__":
    n = 50
    hostname = "keyvdb-minikube.com"
    for item in range(0, n):
        threads = threading.Thread(target=req_func, args=(n,hostname))
        threads.start()

