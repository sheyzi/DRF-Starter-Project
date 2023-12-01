# Spek & Boonen Backend

This is the backend for the Spek & Boonen ERP System. It is a REST API written in Python using the Django Rest Framework. It contains endpoints for all components of the ERP system.

## Installation

### Requirements

- Python 3.8 or higher
- Pip

### Setup

1. Clone the repository

   To start working on the project, you first need to clone the repository. You can do this by running the following command in your terminal:

   ```bash
   git clone https://github.com/Mafflle/Spek-N-Boonen-Backend.git
   ```

2. Create a virtual environment

   We recommend using a virtual environment to install the dependencies. This separates the dependencies of this project from the dependencies of other projects on your system. To create a virtual environment, run the following command in your terminal:

   ```bash
   $ python -m venv venv
   ```

3. Activate the virtual environment

   After creating the virtual environment, you need to activate it. To do this, run the following command in your terminal:

   ```bash
   $ source venv/bin/activate # Linux / MacOS
   $ venv\Scripts\activate # Windows
   ```

4. Install the requirements

   Our environment is almost ready. The only thing left to do is to install the dependencies needed to run the project. All dependencies are listed in the requirements.txt file. To install them, run the following command in your terminal:

   ```bash
   $ pip install -r requirements.txt
   ```

5. Setup the `.env` file

   The project uses environment variables to store sensitive information. To setup the environment variables, create a file called `.env` in the root of the project. You can then copy the contents of the `example.env` file into the `.env` file and fill in the values.

6. Start PostgreSQL database (optional)

   The project comes with a docker-compose file that starts a PostgreSQL database. If you want to use this database, you need to have Docker installed on your system.

   You also need to set some docker-compose environment variables. These are listed in the `example.env` file. They are commented out by default. To use the docker-compose file, you need to uncomment these variables and fill in the values.

   After setting the environment variables, you can start the database by running the following command in your terminal:

   ```bash
   $ docker-compose up -d
   ```

   For our application to connect to the database, you need to update the DATABASE_URL environment variable in the `.env` file. Example of a valid PostgreSQL database URL:

   ```
   postgres://user:password@localhost:5432/db_name
   ```

   > **Note:** If you don't want to use PostgreSQL, you can use any other database supported by Django. You can find more information about this [here](https://docs.djangoproject.com/en/3.2/ref/databases/).

   > Using a different database will require you to update the `DATABASE_URL` environment variable in the `.env` file.

7. Run the migrations

   After setting up the database, you need to run the migrations. This will create the tables in the database. To run the migrations, run the following command in your terminal:

   ```bash
    $ python manage.py migrate
   ```

8. Create a superuser (optional)

   To access the admin panel, you need to create a superuser. You can do this by running the following command in your terminal:

   ```bash
   $ python manage.py createsuperuser
   ```

   > **Note:** You can skip this step if you don't want to access the admin panel.

   > The admin panel can be accessed at `http://localhost:8000/admin/`.

9. Run the server

   The project is now ready to run. To start the server, run the following command in your terminal:

   ```bash
   $ python manage.py runserver
   ```

   The server will now be running at `http://localhost:8000/`.

## API Documentation

The API has been documented using Swagger and Redoc. You can access the documentation at `http://localhost:8000/api/swagger/` or `http://localhost:8000/api/redoc/`.

## Testing

To run the tests, run the following command in your terminal:

```bash
$ python manage.py test
```
