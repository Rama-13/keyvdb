# keyvdb
A flask based in-memory key-value store


APP DETAILS:

The app is created using flask and served through gunicorn.<br>
The following HTTP endpoints are available <br> <br>
GET : <br>
      ```/```  <br>
      ```/get/```   (returns the dict)<br> 
      ```/get/<id>``` <br>
      ```/search/```   (queriable using prefix and suffix)<br> 
      ```/len/```   (returns the no. of keys)<br>
      ```/dumpdb/```   (creates a json file with the timestamp in the dump_db folder)<br>
      ```/flush```    (EMPTIES THE DICTIONARY)<br>
  <br>
POST: <br> 
      ```/set/<id>``` ( set "id" as the key and Takes the value as form-data ("value" : <value>) <br><br>
  See utilities/requests_generator.py for more info)<br><br><br><br>
  
 
  
TO RUN THE DOCKER DEPLOYMENT:<br>
  <br>
  cd into keyvdb-docker<br>
  Run : ``` docker-compose build ```<br>
  Run : ``` docker-compose up ```<br>
  <br>
  The Endpoints for keyvdb will be available at localhost:7000, prometheus at localhost:9090 and grafana at localhost:3000. KeyvDBMetrics should have the metrics dashboard. <br>
  If not, load the same from /keyvdb-docker/grafana/dashboards/keyvDBMetrics.json or /keyvdb-docker/grafana/dashboards/keyvDBMetrics-snapshot.json<br>
  <br>
  <br>
  <br>
  <br>
  MINIKUBE DEPLOYMENT:<br>
  <br>
  Make sure minikube has enough CPU (3CPUs) and Memory allocated (>4GB).<br>
  Enable Nginx ingress add on in Minikube<br>
  ``` minikube addon enable nginx ```<br>
  Open Minikube tunnel to be able to access the exposed ingress and services.<br><br>
``` minikube tunnel ```<br><br>
  
  Deploy the keyvdb application from keyvdb-kubernetes/keyvdb-deployment directory<br>
<br>
``` kubectl apply -f deployment.yaml ```<br>
```kubectl apply -f service.yaml```<br>
```kubectl apply -f ingress.yaml ```<br>
  <br>
 Add an entry in the /etc/hosts file for ```127.0.0.1 keyvdb-minikube.com``` so we can access the url from our local browser.<br>
  <br>
 Add a similar entry in /etc/hosts for ```127.0.0.1 prometheus.minikube.com``` as well if you're deploying Prometheus.<br>
  <br>
  <br>
 The corresponding Prometheus and Grafana spec files are present in /keyvdb-kubernetes/prometheus and /keyvdb-kubernetes/grafana directories respectively.<br>
  <br>
  <br>
  For the grafana endpoint to be accessible, use ```minikube service <grafana-service-name> --url -n monitoring```<br>

