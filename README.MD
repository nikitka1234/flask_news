# Новостной портал
Новостной сайт на котором любой желающий может поделиться выдуманной новостью!

## Описание
Новостной сайт созданный с использованием микрофреймворка Flask в рамках обучения по программе Python Pro.

## Технологии
- Python
- Flask
- Flask-WTF
- Flask-SQLAlchemy

## Как запустить
1. клонировать репозиторий
```
git clone [link]
```
2. установить виртуальное окружение и запустить его
```commandline
python -m venv venv
Windows: venv\Scripts\activate
Linux: source venv/bin/activate
GitBash: source venv/Scripts/activate
```
3. установить зависимости
```commandline
pip install -r requirements.txt
```
4. создать файл .env и добавить конфигурацию
```commandline
nano .env
```
```text
YOUR_SECRET_KEY=SECRET_KEY
DATABASE_URI=sqlite:///db.sqlite3
```
5. запуск приложения
```commandline
flask --debug run
```