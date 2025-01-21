# Space-Project
Flask Space API and web interface. 🚀 🪐

## Features
- Estimate the cost and fuel needed for a space mission
- Get SpaceX rocket information
- Generate a route from earth to destination

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/SchillerweinTom/Space-Project
    ```
2. Navigate to the project directory:
    ```bash
    cd Space-Project
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Create DB:
    ```bash
        - CREATE SCHEMA space_project;
        - CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
        - GRANT ALL PRIVILEGES ON space_project.* TO 'your_user'@'localhost';
    ```
7. Run Migration:
    ```bash
    flask db upgrade
    ```

#### Enviroment Variables
- Before running the application, you need to set up some environment variables. Create a `.env` file in the root directory of the project and add the following variables:
    ```
    SQLALCHEMY_DATABASE_URI=mysql+pymysql://your_user:your_password@localhost/space_project
    SECRET_KEY=your_secret_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```

## Use
- On Windows:
    ```bash
    python app.py
    ```
- On macOS/Linux:
    ```bash
    python3 app.py
    ```
- Open your web browser and go to `http://localhost:5000`.