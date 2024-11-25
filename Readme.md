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
SECRET_KEY: Generate a new secret key for your Django project. You can generate one [here](https://djecrety.ir/)
DEBUG: Set it to True for development and False for production.
DB_ENGINE, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, and DB_PORT to connect to your local or remote database.

### 6. Run Migrations
```bash 
python manage.y makemigrations
python manage.py migrate
```

### 7.  Start the Development Server
```bash
python manage.py runserver
```
The server will be available at  [Dev Sever](http://127.0.0.1:8000/)
