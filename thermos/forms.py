from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url



# class attributes = url, description
# wtform classes = URLField, StringField
# validators:
    # DataRequired() ensures field is not blank
    # url ensures that url is valid
    # NOTE: change URLField to StringField for this courses sake...
class BookmarkForm(FlaskForm):
    url = StringField('The URL for your bookmark:', validators=[DataRequired(), url()])
    description = StringField('Add an optional description:')

    def validate(self):
        if not self.url.data.startswith("http://") or\
            self.url.data.startswith("https://"):
            self.url.data = "http://" + self.url.data
        
        if not FlaskForm.validate(self):
            return False
        
        if not self.description.data:
            self.description.data = self.url.data

        return True

