## Intro
I have implemented the task using FastAPI, as it offers a good user and developer experience due to automatically generated documentation, few lines needed to code and fast speed. More details here: https://fastapi.tiangolo.com/


## How to run it
I have deployed the app on Google Cloud here: https://smg-rd-lojnve64ba-ey.a.run.app/docs , where you can test it by clicking on the each endpoint and then on 'Try it out'. You can also test it using curl (```curl -i https://smg-rd-lojnve64ba-ey.a.run.app/sentences/1```), or copy and change the suggested api call provided in the documentation. I did not implement any security for accessing the api for simplicity reasons, but in real life this would be a must (and also request limits, monitoring).


In order to check my solution locally you need to have the google cloud client installed, the json credentials saved in the ~/.credentials/gc.json file, a bigqeury table named sentences.sentences and the data from the file imported in it. Also, you need to have the python libraries in the requirements.txt installed in the virtual or conda environment. The URL to test it is localhoost:8080/docs.

For testing with docker, you need to have docker and docker-compose installed and the google cloud json credentials saved in the ~/.credentials/gc.json file.
Then run ```docker-compose -f ./docker-compose.yml up -d --build```. The URL is localhoost:18080/docs.


## Notes
1. I tried to use some of the FastAPI recommended practices by using routers, defining models (in ./routers/model.py) and setting parameters in the endpoints' definition in order to provide documentation automatically and enforce correct types of the parameters.

2. The way I understood the requirement for the POST endpoint, it was supposed to just add a new sentence and throw an error in case a sentence with the same id already exists. Normally these types of CRUD operations work best on a relational database (such as Psotgres, MySql), because there a primary key can be enforced by the RDBMS. Bigquery and data warehouses in general do not provide these types of guarantees, so I tried to implement it in the current app with a lock. This should be safe enough provided that only one instance of the app is running, but in real life I would strongly advise to use a RDBMS.

3. The way I understood the requirement for the GET endpoint, it was supposeds to return a 400 error in case the ID was not numeric and a 405 error in case the ID is not found. FastAPI has automatic validation of the parameter types and returns a 422 error for non-numeric input (see comments and reasons for this implementation here: https://github.com/tiangolo/fastapi/issues/643#issuecomment-548139778). If a 400 return code is reannly needed, I have provided 2 solutions:

 - to have the SentenceID type as string (implemented in the /sentences_id_string/ endpoint); this would break the requirement which specifies the type as int, but would provide a good compromise and it would be my preffered solution if a return code of 400 is needed

 - override the default behaviour of FastAPI, as I have done in the app.py file, if you uncomment the lines 11-22; this workaround still does not provide the expected custom message

4. I have written also tests for the GET and POST methods, which should be run with running ```pytest .``` inside the app root folder. For the POST I have chosen to create a new id using a very big integer (based on unix timestamp milliseconds, to ensure its uniqueness), test which should be normally run only in a dev environment, and never in prod - this can be done in the CI/CD process by using a different credentials json file, which points to a dev project.


I am looking forward to discuss my solution during an interview!