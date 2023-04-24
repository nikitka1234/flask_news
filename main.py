from flask import Flask, render_template


app = Flask(__name__)

content = [
    {"title": "Название для шаблона из словаря", "text": "Текст для шаблона из словаря"},
    {"title": "Экс-глава регионального СК назначен главным федеральным инспектором", "text": "Бывший руководитель следственного управления Следственного комитета по Свердловской области Михаил Богинский назначен главным федеральным инспектором региона. Как сообщили в пресс-службе полпредства, соответствующее распоряжение подписал полномочный представитель президента в УрФО Владимир Якушев."},
    {"title": "Посол Швейцарии выступил в защиту отказа от передачи Украине боеприпасов", "text": "Посол Швейцарии в Берлине Пауль Зегер выступил в защиту решения правительства страны об отказе передавать Украине боеприпасы швейцарского производства. О своей позиции он заявил изданию Augsburger Allgemeine."}
]

dt = {"key1": 125371856, "key2": "Hello, world!", "key3": "<h1>Текст для проверки</h1>"}


def index():
    return render_template("index.html", content=content)


def news():
    return "Новости"


def news_detail(id):
    return render_template("news_detail.html", **content[id])


def category(name):
    print(type(name))
    return f"Категория {name}"


app.add_url_rule("/", "index", index)
app.add_url_rule("/news", "news", news)
app.add_url_rule("/news_detail/<int:id>", "news_detail", news_detail)
app.add_url_rule("/category/<string:name>", "category", category)
