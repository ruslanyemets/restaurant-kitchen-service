# Restaurant Kitchen Service

Restaurant Kitchen Service is a web application for kitchen management.
Cooks can search, create, edit, and delete dishes, dish types and ingredients.
The app is built with Django and uses SQLite for the database.


# Installation Instructions

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ruslanyemets/restaurant-kitchen-service

2. Navigate to the project directory:
   ```bash
   cd restaurant-kitchen-service

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate  # For Windows

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

5. Set up environment variables by creating a .env file in the root directory with the following content:
   ```bash
   SECRET_KEY=your_secret_key
   DEBUG=True

6. Run database migrations:
   ```bash
   python manage.py migrate

7. Load data to database from JSON:
   ```bash
   python manage.py loaddata restaurant_kitchen_service_db_data.json

8. Start the development server:
   ```bash
   python manage.py runserver

9. Open your browser and go to http://127.0.0.1:8000/ to see the app in action.


# Usage

Once the server is running, you can access the application through your browser:

1. Create superuser:
   ```bash
    python manage.py createsuperuser

2. Use created username and password to log in.


# Running Tests

To run tests for the application, use the following command:
   ```bash
    python manage.py test
