# KnigArch

## EN

KnigArch is a Django web application that serves as a book catalog/archive. The project supports user registration and authentication, book browsing and searching, categories, reviews, and password recovery.

### Main Features

- User registration and authentication
- Book browsing and searching
- Book categories
- Book reviews
- Password recovery

### Project Structure

The project consists of the following applications:

- **user**: user management
- **main**: main application
- **book**: book management
- **category**: category management
- **registration**: user registration
- **login**: user authentication
- **rest_password**: password recovery
- **filling**: database filling (fixtures)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KnigArch
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # for Linux/Mac
   venv\\Scripts\\activate  # for Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

### Running the Project

1. Start Redis (if used):
   ```bash
   brew services start redis  # for Mac
   ```

2. Start the server:
   ```bash
   python3.11 manage.py runserver
   ```

3. After stopping the project, do not forget to stop Redis:
   ```bash
   brew services stop redis  # for Mac
   ```

### Filling the Database

To fill the database, use the `fill_database.sh` script:
```bash
./fill_database.sh
```

### Technologies Used

- Django 4.2.9
- SQLite
- Redis (optional)
- HTML/CSS/JavaScript
- Pillow
- NumPy
- Django Debug Toolbar (optional)

### Static Files and Templates

- Templates: `templates/`
- Static files: `static/`
  - CSS: `static/main/css/`
  - JavaScript: `static/main/js/`
  - Images: `static/main/img/`

## RUS

KnigArch — это веб-приложение на Django, представляющее собой каталог/архив книг. Проект поддерживает регистрацию и авторизацию пользователей, просмотр и поиск книг, категории, отзывы, а также восстановление пароля.

### Основные функции

- Регистрация и авторизация пользователей
- Просмотр и поиск книг
- Категории книг
- Отзывы на книги
- Восстановление пароля

### Структура проекта

Проект состоит из следующих приложений:

- **user**: управление пользователями
- **main**: основное приложение
- **book**: управление книгами
- **category**: управление категориями
- **registration**: регистрация пользователей
- **login**: авторизация пользователей
- **rest_password**: восстановление пароля
- **filling**: наполнение базы данных (фикстуры)

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <url-репозитория>
   cd KnigArch
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\\Scripts\\activate  # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirement.txt
   ```

### Запуск проекта

1. Запустите Redis (если используется):
   ```bash
   brew services start redis  # для Mac
   ```

2. Запустите сервер:
   ```bash
   python3.11 manage.py runserver
   ```

3. После остановки проекта не забудьте отключить Redis:
   ```bash
   brew services stop redis  # для Mac
   ```

### Наполнение базы данных

Для наполнения базы данных используйте скрипт `fill_database.sh`:
```bash
./fill_database.sh
```

### Используемые технологии

- Django 4.2.9
- SQLite
- Redis (опционально)
- HTML/CSS/JavaScript
- Pillow
- NumPy
- Django Debug Toolbar (опционально)

### Статические файлы и шаблоны

- Шаблоны: `templates/`
- Статические файлы: `static/`
  - CSS: `static/main/css/`
  - JavaScript: `static/main/js/`
  - Изображения: `static/main/img/`


### FrontEnd:
[Михаил](https://github.com/mihali444)

### BackEnd
[dkzzum](https://github.com/dkzzum)
