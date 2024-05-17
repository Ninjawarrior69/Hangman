# Hangman

## Description

The Hangman game is a classic word-guessing game where the player tries to guess a word by suggesting letters within a certain number of guesses. The purpose of this application is to provide an engaging and educational experience where players can improve their vocabulary, spelling skills, and problem-solving abilities. It is designed to be fun and challenging, suitable for players of all ages.

## Design and Use

We provide users with 4 different game modes:

- **Easy Mode**:

  - Guessing words in this mode is more forgiving, with more attempts allowed.
  - Ideal for beginners or those looking for a relaxed gaming experience.

- **Hard Mode**:

  - This mode is for the more experienced players who seek a challenge.
  - Guessing words correctly in this mode requires precision and strategy.
  - Players have fewer attempts compared to easy mode.

- **Two-Player Mode**:

  - Challenge your friends or family members to a game of Hangman.
  - Send challenges to other players, specifying the word and providing a hint if desired.
  - Once the challenge is accepted, the challenging player competes to guess the word first.
  - Players who receive a challenge will be notified. Once the challenge is completed, the challenging player will also be notified.

- **Competitive Mode**:
  - Players are given random difficult words to guess.
  - Earn points for correctly guessing words and lose points for incorrect guesses.
  - Each player's score is displayed on the leaderboard, showcasing their Hangman skills.

|  UWA ID  |     Name      | GitHub Username |
| :------: | :-----------: | :-------------: |
| 22964473 | Devarsh Patel | Ninjawarrior69  |
| 22895688 | Jarrad McNeil |  oscarnator02   |
| 23356909 |  Josh Cooper  |  JohuaJCooper1  |
| 24250666 | Wei Shen Hong |   weishen1113   |

## Architecture

### Home Page (Menu)

- Provides navigation options to access different sections of the game.
- Allows the player to start a new game, view the leaderboard, or provide feedback.

### Login/Sign Up Page

- Users can log in or sign up to access their game progress and participate in leaderboards.
- Fields include username, password, and confirm password.

### Game Page

- Displays the Hangman game interface.
- Allows the player to select game mode, difficulty level, and hint options.
- Provides animations for visual feedback on correct/incorrect guesses.

### Leaderboard Page

- Displays rankings of players based on their scores.
- Shows player names and corresponding scores.

### Feedback Page

- Allows users to provide feedback on the game experience.
- Graphs previous games, user scores, and feedback of the game.

### Notifications Page

- Displays notifications for game-related events, such as requests to play specific words.
- Allows users to accept or decline game invitations.

## How to launch the game

1. Open New Terminal

2. Enter this command to update python version
python.exe -m pip install --upgrade pip

3. Enter these commands to install flask:
pip install flask

4. Enter these commands to install flask WTF:
pip install Flask-WTF


5. Enter this command to install Socket.IO:
pip install flask-socketio

6. Enter these commands to install  WTF forms :
 pip install WTForms

7. Enter this command to install sqlalchemy:
pip install flask-sqlalchemy

8. Enter this command to install flask_Migrate:
    pip install Flask-Migrate

9. Enter this command to install selenium:
    pip install selenium

10. Enter this command to run the app:
python App.py 


11. Click on the host link, eg. http://127.0.0.1:5005

To run the unit test :
type python -m unittest unit.py 

To run the selenium test :
run the application 
then open a new terminal and type python -m unittest seleniumTest.py 