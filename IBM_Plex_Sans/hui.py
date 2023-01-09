
from guizero import App, PushButton, Text

# create the main app
app = App(title="Reaction Time Game")

# create a list to store the top scores
top_scores = []

# create a function to add a new score to the top scores list
# and sort the list in descending order
def add_score(name, score):
    top_scores.append( (name, score) )
    top_scores.sort(key=lambda x: x[1], reverse=True)

# create a function to display the top scores
def show_leaderboard():
    leaderboard = Text(app, text="Top Scores:")
    for i in range(min(len(top_scores), 5)):
        name, score = top_scores[i]
        Text(app, text="{}. {}: {}".format(i+1, name, score))

# create a function to start the game
def start_game():
    # ask for the player's name and age
    name = app.question("Enter your name:")
    age = app.question("Enter your age:")

    # run the game three times and calculate the average score
    total_score = 0
    for i in range(3):
        # ask the player to press the button as soon as they see it
        button = PushButton(app, text="Press Me!")
        app.wait_until_closed()
        total_score += button.time_held

    # calculate the average score and add it to the top scores list
    average_score = total_score / 3
    add_score(name, average_score)

# create the main menu with a start and leaderboard option
start_button = PushButton(app, text="Start", command=start_game)
leaderboard_button = PushButton(app, text="Leaderboard", command=show_leaderboard)

# display the main menu
app.display()
