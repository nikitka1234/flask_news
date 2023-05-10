from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


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
