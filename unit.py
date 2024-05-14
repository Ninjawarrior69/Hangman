import unittest
from sqlalchemy import func
from app import TestHangmanReviews, app, db
from datetime import datetime
 
class TestReviews(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()      
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        TestHangmanReviews.__table__.drop(db.engine)
        db.session.remove()
        self.app_context.pop()

    def test_average_GameRatings(self):   #Testing correct averages to ensure correct data gets plotted for the /charts route
        HangManReview1 = TestHangmanReviews(reviewID='ID_1', username='TestUser1', datePlayed=datetime.now(),Game_Rating=5,General_Comments="")
        HangManReview2 = TestHangmanReviews(reviewID='ID_2', username='TestUser2', datePlayed=datetime.now(),Game_Rating=6,General_Comments="")
        HangManReview3 = TestHangmanReviews(reviewID='ID_3', username='TestUser3', datePlayed=datetime.now(),Game_Rating=8,General_Comments="")
        db.session.add_all([HangManReview1, HangManReview2, HangManReview3])
        db.session.commit()

        # Calculate the manually calculated average SELECT AVERAGE(game_rating) FROM TestHangmanReviews
        hand_calculated_mean = (5 + 6 + 8) / 3
        average_value = db.session.query(func.avg(TestHangmanReviews.Game_Rating)).scalar()

        # Assert that the hand calculated mean matches the database mean (TESTING  INSERTION)
        self.assertEqual(average_value, hand_calculated_mean)

       
    def test_database_insertion(self):
        # Adding test data within the hangman reviews test database 
        HangManReview = TestHangmanReviews(reviewID='ID_1', username='TestUser1', datePlayed=datetime.now(),Game_Rating=5,General_Comments="")
        db.session.add(HangManReview)
        db.session.commit()

        # Retrieve the review from  db and assert that it has inserted the correct values into the db 
        HangmanReview_FROM_DB = TestHangmanReviews.query.first()
        self.assertEqual(HangmanReview_FROM_DB.username, "TestUser1")
        self.assertEqual(HangmanReview_FROM_DB.Game_Rating, 5)
        


    def test_HangmanReview_score_range(self):
         # Adding test data within the hangman reviews test database 
        HangManReview5 = TestHangmanReviews(reviewID='ID_5', username='TestUser1', datePlayed=datetime.now(),Game_Rating=5,General_Comments="")
        HangManReview6 = TestHangmanReviews(reviewID='ID_6', username='TestUser1', datePlayed=datetime.now(),Game_Rating=5,General_Comments="")
        HangManReview7 = TestHangmanReviews(reviewID='ID_7', username='TestUser2', datePlayed=datetime.now(),Game_Rating=6,General_Comments="")
        HangManReview8 = TestHangmanReviews(reviewID='ID_8', username='TestUser3', datePlayed=datetime.now(),Game_Rating=8,General_Comments="")
        db.session.add_all([HangManReview5,HangManReview6,HangManReview7,HangManReview8])
        db.session.commit()

        # Retrieve the review from  db and assert that the game ratings are between 0 and 10 
        ALL_DATA = TestHangmanReviews.query.all()
        game_ratings= []
        for Review in ALL_DATA:
            game_ratings.append(Review.Game_Rating)

        self.assertGreaterEqual(min(game_ratings), 0)
        self.assertLessEqual(max(game_ratings), 10)

 
if __name__ == '__main__':
    unittest.main()