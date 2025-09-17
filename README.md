# Billboard

**Billboard** is an article and newsletter application.  
It allows readers to browse published content, follow their favorite journalists or publishers, and stay up to date with new releases.  

---

## Features

- **Reader Registration**  
  - Register and log in.  
  - Browse articles and newsletters.  
  - Follow specific journalists or publishers.  

- **Journalist Registration**  
  - Register and join the publisher they work for.  
  - **Add, edit, delete, and view** articles/newsletters.  
  - Articles/newsletters can only be edited or deleted **before approval**.  

- **Editor Registration**  
  - Register and join their publisher.  
  - **Approve or reject** articles/newsletters submitted by journalists.  
  - Once approved, editors can **publish** content, making it visible to all readers.  

---

## Technologies Used

- **Backend:** Django (Python)  
- **Database:** MariaDB (configurable to SQLite/PostgreSQL/MySQL)  
- **Frontend:** Django Templates, HTML, CSS  
- **Authentication:** Django’s built-in authentication system  

---

## Installation

1. **Download the project**  
   Clone or download the ZIP file from the repository:  
   [Repository Link](https://github.com/hyperiondev-bootcamps/KT25040017912/tree/main/Level%202%20-%20Introduction%20to%20Software%20Engineering/M06T08%20%E2%80%93%20Capstone%20Project%20%E2%80%93%20News%20Application)  

   Extract the ZIP file and ensure you are in the project root directory (where `manage.py` is located).  
   ```bash
   cd path/to/project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install MariaDB**  
   Make sure MariaDB is installed on your system.  
   Download: [MariaDB Download Page](https://mariadb.org/download/?t=mariadb&p=mariadb&r=12.0.2&os=windows&cpu=x86_64&pkg=msi&mirror=liquidtelecom)  

   After installation, log into MariaDB:  
   ```bash
   cd "C:\Program Files\MariaDB 12.0\bin"
   mysql -u root -p
   ```

   Create a database and grant permissions:  
   ```sql
   CREATE DATABASE billboard_db;
   GRANT ALL PRIVILEGES ON billboard_db.* TO 'billboard_user'@'localhost' IDENTIFIED BY 'secure_password';
   FLUSH PRIVILEGES;
   ```

   Update your `billboard/settings.py` with your database details:  
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'billboard_db',
           'USER': 'billboard_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. Open the app in your browser:  
   👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

## Usage

- **Readers**: Browse and follow journalists or publishers.  
- **Journalists**: Create and manage their own content.  
- **Editors**: Approve, reject, and publish content.  
- **Admins**: Manage users, groups, publishers and permissions via the Django Admin Panel.  

---

## Contributing

Contributions are welcome!  

1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push your branch:  
   ```bash
   git push origin feature-name
   ```
5. Create a Pull Request.  

---

## License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software with proper attribution.  

---

## Author

- **Kelvin** – Developer of Billboard  
