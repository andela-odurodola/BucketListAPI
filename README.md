## BucketListAPI
A flask-RESTful project for Bucketlists. A BucketList is a list of all the goals you want to achieve, dreams you want to fulfill and life experiences you desire to experience before you die (or hit the bucket). This API helps to create and manage bucketlists through protected API endpoints. That is, it requires authorization.

## Development
This application was developed using [FlaskRestful](http://flask-restful.readthedocs.io/en/0.3.5/quickstart.html). Sqlite was used for persisting data with [SQLAlchemy](https://www.sqlalchemy.org/) as [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping).

## Application Features
# User Authentication
Users are authenticated and validated using  Python's `itsdangerous` library. It generates a token on login and ensures each account is unique to a user and can't be accessed by an authenticated user.

# Creation of BucketLists and BucketListItems
Authenticated users can create as many bucketlists and bucketlist items inside each bucketlist created.

# Pagination
Authenticated Users have the flexibility to specify how many Bucketlists they want to see on each page. The default is 20 and the maximum number of items is 100.

# Search
Authenticated users can also search for Bucketlists based on the bucketlist's name

## Installation
* Start up your terminal (or Command Prompt on Windows OS).
* Ensure that you've `python` installed on your PC.
* Clone the repository by entering the command `git clone https://github.com/andela-odurodola/BucketListAPI/tree/develop` in the terminal.
* Navigate to the project folder using `cd BucketListAPI` on your terminal (or command prompt)
* After cloning, create a virtual environment then install the requirements with the command:
`pip install requirements.txt`.
* After this, you'll need to migrate data scheme to the database using the command: `python manage.py init_db`.

## Testing
To ensure that your installation is successful you'll need to run tests.
Enter the command `python manage.py test` in your terminal (or command prompt) to run test

## Usage
* A customized interactive python shell can be accessed by passing the command `python manage.py shell` on your terminal.
* Once this is done, the application can be started using `python manage.py runserver` and by default the application can be accessed at `http://127.0.0.1:5000`. The application starts using the configuration settings defined in the config.py file

## Configuration
The API currently has 4 different configuration which can be defined in the .env file.
- `Production`: this configuration starts the app ready for production to be deployed on any cloud application platform such as Heroku, AWS etc.
- `Development`: this configuration starts the application in the development mode.
- `Testing`: this configuration starts the application in a testing mode.

## API Documentation
-----
The API uses the class-based view, with each routed to an endpoint that uses HTTP response codes to indicate API status and errors.

# API Resource Endpoints
URL Prefix = `http://127.0.0.1:5000/api/v1` where sample domain is the root URL of the server HOST.


| EndPoint                                 | Functionality                 | Public Access|
| -----------------------------------------|:-----------------------------:|-------------:|
| **POST** /auth/register                  | Register a user               |    TRUE      |
| **POST** /auth/login                     | Logs a user in                |    TRUE      |
| **POST** /bucketlists/                   | Create a new bucket list      |    FALSE     |
| **GET** /bucketlists/                    | List all created bucket lists |    FALSE     |
| **GET** /bucketlists/id                  | Get single bucket list        |    FALSE     |
| **PUT** /bucketlists/id                  | Update a bucket list          |    FALSE     |
| **DELETE** /bucketlists/id               | Delete a bucket list          |    FALSE     |
| *POST* /bucketlists/id                   | Create a new item bucket list |    FALSE     |
| *PUT* /bucketlists/id/items/item_id      | Update a bucket list item     |    FALSE     |
| *DELETE* /bucketlists/id/items/item_id   | Delete an item in bucket list |    FALSE     |

## Authentication
# POST HTTP Request
-   `POST /auth/login`
    # HTTP Response
-   HTTP Status: `202: Accepted`
```
{
  "Output": "logged in successfully as dee",
  "Token": "eyJpYXQiOjE0OTE1NjcyMjYsImV4cCI6MTQ5MTYwMzIyNiwiYWxnIjoiSFMyNTYifQ.eyJpZCI6Mn0._Fdpr7MVaBEkMCScnmOHZhGVpYDv1OOVX4n2-LH6ARY"
}
```

# POST HTTP Request
-   `POST /auth/register`
    ###### HTTP Response
-   HTTP Status: `201: Created`
```
{
  "message": "Welcome dee to the Bucketlist Service."
}
```


# BucketLists
# GET HTTP Request
-   `GET /api/v1/bucketlists/`
-   Requires: User Authentication
    HTTP Response
-   HTTP Status: `200: OK`
```
{
  "count": 1,
  "next": null,
  "posts": [
    {
      "created_by": "dee",
      "date_created": "2017-04-07 11:09:18.776900",
      "date_modified": "2017-04-07 11:09:18.776911",
      "id": 1,
      "items": [
        {
          "date_created": "2017-04-07 11:16:16.043620",
          "date_modified": "2017-04-07 11:17:28.982945",
          "done": true,
          "id": 1,
          "name": "Travel to paris"
        }
      ],
      "name": "Travel to places"
    },
```

# GET HTTP Request
-   `POST /api/v1/bucketlists/`
-   Requires: User Authentication
    HTTP Response
-   HTTP Status: `201: Created`
```
{
  "created_by": "dee",
  "date_created": "2017-04-07 14:30:14.673854",
  "date_modified": "2017-04-07 14:30:14.673888",
  "id": 6,
  "items": [],
  "name": "Lose Weight"
}
```

# Author
**Durodola Damilola**

## Acknowledgments

Thanks to my facilitator **Njira Perci**
