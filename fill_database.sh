#!/bin/bash

# Загрузка фикстур
python3.11 manage.py loaddata filling/authors.json
python3.11 manage.py loaddata filling/categories.json
python3.11 manage.py loaddata filling/publishers.json
python3.11 manage.py loaddata filling/books.json
#python3.11 manage.py loaddata filling/book_categories.json
python3.11 manage.py loaddata filling/book_offers.json