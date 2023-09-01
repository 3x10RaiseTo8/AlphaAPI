# AlphaAPI
A FastAPI application

## About the project
- The project is a web API backend application.
- It is a social media type application in which users can see and posts any form of data.
- Users can vote on posts
- They can retrieve all the posts while applying many filters
- Based on an emerging framework for Python called FastAPI
- Entire project uses Python as a sole language
- Automatic documentation generation by Swagger

## Specifications
- Live data validation by Pydantic Python library.
- Database used – PostgreSQL
- Login implementation using web standard JSON Web Tokens.
- Object-Relational Mapper SQLAlchemy for used for all SQL CRUD operations.
- Implementation of Database migration tool Alembic in the project in order to support future scale up or roll down.
- Use of environment variables
- Hashed password

**App was deployed publicly on https://alpha-api-social.herokuapp.com but since Heroku removed its free tier, the domain has been taken down.**

Run the application locally by downloading the code.

Go to /docs route to use interactive 
documentation to get the feel of it.

### Steps to try out
1. Create an account by providing a JSON data of email and 
password at /users endpoint
2. Log yourself in. Provide username, which is in this case email, 
and password. Your session is valid till 12 hours
3. Send a POST request on /posts endpoint to post content. You 
must provide Title and Content in the body of the request in 
JSON format.
4. Now you can send GET request for individual or all posts.
5. To vote on a post, send POST request with JSON providing 
post id you want to vote on.
