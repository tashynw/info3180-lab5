from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email


class MovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    poster = FileField("Poster", validators=[FileRequired(), FileAllowed(
        ['jpg', 'png'], 'Upload a .png or .jpg file')])
