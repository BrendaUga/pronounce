from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired


class AddWordPronouncingForm(FlaskForm):
    word = StringField(label='word', validators=[DataRequired(message='Word is mandatory')])
    audio_file = FileField(label='audio', validators=[FileRequired(), FileAllowed(['mp3'], '.mp3 files only')])
