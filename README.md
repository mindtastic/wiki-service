# wiki-service

The Wiki Service of the mindtastic App provides the user with static information about mental health. The information displayed are 
carefully researched and put together by experts in mental health training and psychologists. Those articles should only be added by admins of Kopfsachen e.V..


The App uses flask to create an API and uses mongoDB as a storage solution for the articles. 
The following endpoint are provided:

| Endpoint | Functionality |
| :---: | :---: |
| GET wiki/  | get all avaiable articles |
| POST wiki/   | create a new article, Request JSON has to include "title" and "content", the articleID will be difined and returned by the wikiSerive |
| Delete wiki/{articleID}  | deletes the article which has the given ID  |



The App uses flask to create an API and uses mongoDB as a storage solution for the articles. 

## Local development

For local development, a docker-compose.yml is provided. The project folder will be mounted into the container, so changes to the code will be applied automatically. You can start the environment with:

```
docker-compose up 
```


# Test the endpoints:
To test the endpoints, run the following command in the root directory (After installing pytest):

    pytest