# Test task

Let me speak from the bottom of my heart

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)


## Features

3 endpoints:
- POST sign_up: creating user and retrieving user_id and signature
- POST sign_in: creating auth token for user by email and password and retrieving it
- GET user: retrieving user info by token

    
## Prerequisites

Make sure you have the following software installed on your machine:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository to your local machine:
    ```bash
    git clone git@github.com:gluhovSemen/test_task.git
    ```
   
2. Create an .env file in the root directory of your project with the following content as in env_template

3. Open a terminal and navigate to your project's directory.

4. Build the Docker images by running:
    ```bash
    docker-compose build  
    ```

5. Start the Docker containers:
    ```bash
    docker-compose up
    ```
   This will start the Django development server, database, and any other services defined in the docker-compose.yml file.

6. Access the application:
Open your web browser or Postman and navigate to http://localhost:8000/ or http://0.0.0.0:8000/.

7. When you're done, stop the containers by pressing Ctrl + C in the terminal where you started them. To remove the containers and associated resources, run:
    ```bash
    docker-compose down --volumes
    ```
