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


