# Hamza Mart Backend
This project contains the backend API for the **Hamza Mart** application, built using **Django 5.1.3**. The project includes a Django app for managing products, users, orders, and more.

## Project Setup
Follow these steps to set up the development environment on your local machine.

### 1. **Clone the Repository**
 Clone the repository to your local machine:

```bash
git clone https://github.com/MianHamzaHussain/hamza-mart.git
cd hamza_mart/backend
```

### 2. Make sure you have Python 3.12.2 installed on your system. You can check the Python version by running:
```bash
python --version
```
 If it's not installed, download and install Python 3.12.2 from  [Python.org](https://www.python.org/) 

### 3. Now, create a virtual environment in the project directory:
```bash
# Linux/MacOS
python3 -m venv env
# Windows
python -m venv env
```

### 4. Activate the virtual environment:
```bash
# Linux/MacOS
source env/bin/activate
# Windows
env\Scripts\activate
```

### 5. Install Dependencies
Once the virtual environment is activated, install the required dependencies by running
```bash
pip install -r requirements/requirements.txt
```

### 6. Create .env File
#### 1. Copy the template .env file from backend/settings/.env.template to backend/settings/.env.
```bash
cp backend/settings/.env.template backend/settings/.env
```
#### 2. Open the .env file and update the values as needed. At a minimum, you should update the following:
-   SECRET_KEY: Generate a new secret key for your Django project. You can generate one [here](https://djecrety.ir/)
-   DEBUG: Set it to True for development and False for production.
-   DB_ENGINE, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, and DB_PORT to connect to your local or remote database.

### 7. Run Migrations
```bash 
python manage.y makemigrations
python manage.py migrate
```

### 8. Using the Default SQLite Database
The project includes a pre-configured SQLite database (db.sqlite3) with the following users:
- Admin User (Superuser)
    - Email: mian@gmail.com
    - Password: 12345678
- Normal User
    - Email: mian2@gmail.com
    - Password: 12345678

### 9. Using a Custom Database (PostgreSQL or Remote)
If you are using a custom database, follow these additional steps:
- Run migrations (as shown above in step 7) to set up the schema.
- Create a superuser:
```bash
python manage.py createsuperuser
```

### 10.  Start the Development Server
```bash
python manage.py runserver
```
The server will be available at  [Dev Sever](http://127.0.0.1:8000/)


## Import API Documentation and Environment in Postman
To use the API documentation in Postman, follow these steps:
### 1. Import the API Collection:
- Open Postman.
- Click the Import button in the top-left corner.
- Navigate to the postman/ folder in the repository.
- Select the collection.json file.
- Click Import
- The collection will be imported with the name Hamza Mart

### 2. Import the Environment Variables:
- In Postman, go to the Environments tab in the sidebar.
- Click the Import button.
- Navigate to the postman/ folder in the repository.
- Select the environment.json file.
- Click Import
- The environment will be imported with name  localHamzaMart

### 3. Update Environment Variables:
- Open the imported environment (localHamzaMart) in Postman:
- Go to Environments and select localHamzaMart.
- Update the following variables as needed:
- baseURL: Ensure it points to your backend URL, e.g., http://127.0.0.1:8000/api/ 
- token: Replace the placeholder JWT token with a valid token from your backend
- Click Save to apply the changes.

### 4. Verify the Setup
- Ensure the imported collection (Hamza Mart) is visible in the Collections tab.
- Confirm the localHamzaMart environment is selected in the top-right environment dropdown.

### 5. Test the API Endpoints
- Open the imported collection (Hamza Mart) in the Collections tab.
- Select an endpoint and click Send.
- Confirm that the response is as expected.