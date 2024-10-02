# Blogging Platform API

## Overview
This project is a RESTful API for a personal blogging platform, implemented using Flask and MySQL. It provides basic CRUD (Create, Read, Update, Delete) operations for managing blog posts.

## Features
- Create new blog posts
- Retrieve individual posts
- Update existing posts
- Delete posts
- List all posts
- Search posts by title, content, or category

## Technology Stack
- Python 3.x
- Flask: Web framework
- MySQL: Database
- Flask-MySQLdb: MySQL database adapter for Flask
- python-dotenv: For managing environment variables

## Setup and Installation
1. Clone the repository
2. Install dependencies: `pip install flask flask-mysqldb python-dotenv`
3. Set up a MySQL database
4. Create a `.env` file in the project root with the following variables:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DB=blog_api
   ```
5. Run the application: `python app.py`

## API Endpoints

### 1. Create a Post
- **URL:** `/posts`
- **Method:** POST
- **Body:** JSON object with `title`, `content`, `category`, and optional `tags`

### 2. Get a Post
- **URL:** `/posts/<id>`
- **Method:** GET

### 3. Update a Post
- **URL:** `/posts/<id>`
- **Method:** PUT
- **Body:** JSON object with `title`, `content`, `category`, and optional `tags`

### 4. Delete a Post
- **URL:** `/posts/<id>`
- **Method:** DELETE

### 5. List All Posts
- **URL:** `/posts`
- **Method:** GET
- **Query Parameter:** `term` (optional) for searching posts

## Data Model
Posts are stored with the following fields:
- id (auto-generated)
- title
- content
- category
- tags (stored as a comma-separated string)
- createdAt (auto-generated)
- updatedAt

## Error Handling
The API returns appropriate HTTP status codes and error messages for various scenarios, such as missing required fields or non-existent posts.

## Security Considerations
- Ensure to use strong, unique passwords for the database
- Consider implementing authentication and authorization for the API in a production environment
- Use HTTPS in production to encrypt data in transit

## Future Enhancements
- User authentication and authorization
- Pagination for listing posts
- More advanced search and filtering options
- API rate limiting
- Logging and monitoring

src: https://roadmap.sh/projects/blogging-platform-api