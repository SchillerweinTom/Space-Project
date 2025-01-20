# Space-Project
Flask Space API and web interface. 🚀 🪐


#### Enviroment
- SQLALCHEMY_DATABASE_URI
- SECRET_KEY


#### Setup
- Database:
  - CREATE SCHEMA 'space_project';
  - CREATE USER 'tom'@'localhost' IDENTIFIED BY 'Admin$00';
  - GRANT ALL PRIVILEGES ON space_project.* TO 'tom'@'localhost';
- Migration:
  - flask db upgrade

