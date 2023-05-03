from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class FeedbackForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(message='Поле "Имя" не должно быть пустым')])
    text = TextAreaField('Отзыв', validators=[DataRequired(message='Поле "Отзыв" не должно быть пустым')])
    email = EmailField('Почта', validators=[Optional()])
    rating = SelectField('Оценка', choices=[1, 2, 3, 4, 5], default=5)
    submit = SubmitField('Отправить')


class NewsForm(FlaskForm):
    title = StringField('Название новости',
                        validators=[DataRequired(message='Поле "Название новости" не должно быть путым'),
                                    Length(max=255, message="В названии не должно быть более 255 символов")])
    text = TextAreaField('Текст новости',
                         validators=[DataRequired(message='Поле "Текст новости" не должно быть путым'),
                                     Length(min=50, message="В тексте должно быть минимум 50 символов")])
    category = SelectField("Категория")
    submit = SubmitField('Добавить')


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    news = db.relationship("News", back_populates="category")

    def __repr__(self):
        return f"Category: {self.id}, {self.title}"


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    category = db.relationship("Category", back_populates="news")

    def __repr__(self):
        return f"News: {self.id}, {self.title}"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())


with app.app_context():
    db.create_all()


def index():
    db_news = News.query.all()
    categories = Category.query.all()

    return render_template("index.html", content=db_news, categories=categories)


def feedback():
    form = FeedbackForm()
    categories = Category.query.all()

    if form.validate_on_submit():
        feedback_model = Feedback()
        feedback_model.name = form.name.data
        feedback_model.text = form.text.data
        feedback_model.email = form.email.data
        feedback_model.rating = form.rating.data
        db.session.add(feedback_model)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("feedback.html", form=form, categories=categories)


def add_news():
    form = NewsForm()
    categories = Category.query.all()
    form.category.choices = [category_t.title for category_t in categories]

    if form.validate_on_submit():
        news_table = News()
        news_table.title = form.title.data
        news_table.text = form.text.data
        news_table.category_id = Category.query.filter(Category.title == form.category.data).first().id
        db.session.add(news_table)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_news.html", form=form, categories=categories)


def news_detail(id):
    nd_news = News.query.get(id)
    categories = Category.query.all()

    return render_template("news_detail.html", nd_news=nd_news, categories=categories)


def category(id):
    category_id = Category.query.get(id)
    news = category_id.news
    categories = Category.query.all()

    return render_template("category.html", content=news, categories=categories)


app.add_url_rule("/", "index", index)
app.add_url_rule("/feedback", "feedback", feedback, methods=["GET", "POST"])
app.add_url_rule("/add_news", "add_news", add_news, methods=["GET", "POST"])
app.add_url_rule("/news_detail/<int:id>", "news_detail", news_detail)
app.add_url_rule("/category/<int:id>", "category", category)
