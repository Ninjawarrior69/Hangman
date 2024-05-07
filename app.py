import uuid
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#init.py
app = Flask(__name__)
app.secret_key = 'your_secret_key'  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Hangman_reviews.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class HangmanReviews(db.Model):
    reviewID = db.Column(db.String(36), nullable=False, unique=True,default=str(uuid.uuid4),primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    datePlayed = db.Column(db.Date, nullable=False)
    Game_Rating = db.Column(db.Integer, nullable=False)
    General_Comments = db.Column(db.Text)
    


class HangmanReviewForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    datePlayed = DateField("Last Played", validators=[DataRequired()])
    Game_Rating = IntegerField("Game Rating (out of 10):", validators=[NumberRange(min=1, max=10)])
    General_Comments = TextAreaField('General Comments')
    submit = SubmitField('Submit your Response')

@app.route('/CreateFeedback', methods=['GET', 'POST'])
def CreateFeedback():
    form = HangmanReviewForm()
    if form.validate_on_submit():
        # Extract form data
        DATA_username = form.username.data
        DATA_datePlayed = form.datePlayed.data
        DATA_Game_Rating = form.Game_Rating.data
        DATA_General_Comments = form.General_Comments.data

        # Create HangmanReviews object
        REVIEW_NEW = HangmanReviews(username=DATA_username, datePlayed=DATA_datePlayed, Game_Rating=DATA_Game_Rating, General_Comments=DATA_General_Comments)
        db.session.add(REVIEW_NEW)
        db.session.commit()

        return redirect(url_for('Hangman_Reviews'))
    return render_template('CreateFeedback.html', form=form)

@app.route('/ExistingFeedback')
def Hangman_Reviews():
    Hangman_Reviews_Data = HangmanReviews.query.all()
    return render_template('ListFeedback.html', Hangman_Reviews_Data=Hangman_Reviews_Data)


@app.route('/charts')
def charts():
     return "Work in Progress"


def init_db():
    with app.app_context():
        db.create_all()

init_db()

if __name__ == '__main__':
    #socketio.run(app, debug=True, port=5005)
    app.run(debug=True, port=5005)