# wiki-service

The Wiki Service of the mindtastic App provides the user with static information about mental health. The information displayed are 
carefully researched and put together by experts in mental health training and psychologists. Those articles should only be added by admins of Kopfsachen e.V..

From inside the app, via two endpoints, the users can get the content of the articles.

GET mongodb/                  get all avaiable articles

GET mongodb/{article_ID}      get a specific article

The App uses flask to create an API and uses mongoDB as a storage solution for the articles. 

## Local development

For local development, a docker-compose.yml is provided. The project folder will be mounted into the container, so changes to the code will be applied automatically. You can start the environment with:

```
docker-compose up 
```
