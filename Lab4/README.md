#Lab 4
In this lab you will continue working on your project. Here is the list of what you shoud do:

1) Deploy a web application for the search engine. Users should be able to send a query to the main page and get a list of links to the relevant documents. Clicking on the link he or she should get the content of the document. You might need Flask application instruction https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/, if needed.
2) Move all documents from the RAM to the hard drive.
3) Move the inverted index to the hard drive.
4) Run another service that simulates the crawler. It should add new documents and remove old ones. You don’t need to update the file with the index all the time. Instead, store the auxiliary index for new documents and set of removed documents.
5) Merge main and auxiliary index periodically, remove the outdated documents from the index.
6) (bonus 50 points) Make a load balancing on the search engine.

## Report

implemented using ```redis```, ```nginx```, ```flask``` and ```docker-compose``` 