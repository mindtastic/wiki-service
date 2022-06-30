# Wiki service

The Wiki Service of the mindtastic App provides the user with static information about mental health. The information displayed are carefully researched and put together by experts in mental health training and psychologists. Those articles should only be added by admins of Kopfsachen e.V.

The App uses FastAPI to create an API and uses mongoDB as a storage solution for the articles.
The following endpoint are provided:

| Endpoint | Functionality |
| :---: | :---: |
| GET wiki/  | get all avaiable articles |
| POST wiki/   | create a new article, Request JSON has to include "title" and "content", the articleID will be difined and returned by the wikiSerive |
| Delete wiki/{articleID}  | deletes the article which has the given ID  |

## Development

### Local development environment

For local development, a docker-compose.yml is provided. The project folder will be mounted into the container, so changes to the code will be applied automatically. You can start the environment with:

```bash
docker-compose up 
```

### Migrations

Because the wiki services uses mongoDB, no *traditional* migrations are required. However, to created indexes and e.g. insert data on app startup, a small system for migrations is provided. The app creates a MongoDB collection `migrations` to store meta information on the migrations that already ran.

To create a new migration, create a new class in the `wiki_service/db/migrations` folder and export it from the `migrations` package by adding it to the `init.py` file. Let your class inherit from `wiki_service.db.migrations.Migration` and implemented the `timestamp` method (that shall return the timestamp at what the migration was created, so they are executed in their order of creation) and the `migrate` method, that then executes the actual migration.
