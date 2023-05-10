from flask import render_template, redirect, url_for

from . import app, db
from .forms import FeedbackForm, NewsForm
from .models import Category, News, Feedback


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
