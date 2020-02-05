# importing all the necessary libraries
import random  # to get random move for the computer
import matplotlib.figure  # to draw the pie char
import pandas as pd  # to handle time
import matplotlib.pyplot as plt  # to draw pie chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # to draw pie chart
from tkinter import Label, Frame, messagebox, Tk, Button  # GUI

# 0 1 2
# 3 4 5
# 6 7 8

winningCombos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                 [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
turn = "X"  # current turn
board = [" "]*9
computer = "O"
human = "X"
Labels = {}
wins = 0
loses = 0
gamesPlayed = 0
winRate = 0
loseRate = 0
tieGames = 0
timeWhenStarted = 0
timeWhenEnded = 0
duration = 0
gameInfo = {}


def start():
    # global means use variables that were defined in lines 14 - 30 !!!IF WE WANT TO CHANGE THEM!!!
    global timeWhenStarted
    # save current time when start button is clicked
    timeWhenStarted = pd.datetime.now()
    frame.pack()  # show game window
    startBtn.destroy()  # remove start button


# finding winner
def findWinner(_board):  # passing current board
    for i in range(len(winningCombos)):  # len(winningCombos) returns length of the array
        # example. winningCombo might me [0, 1, 2] which is the array
        winningCombo = winningCombos[i]
        if(_board[winningCombo[0]] == _board[winningCombo[1]] and _board[winningCombo[1]] == _board[winningCombo[2]]  # if (_board[0] == _board[1] and _board[1] == _board[2] and _board[0] != " "
           and _board[winningCombo[0]] != " "):  # if (X == X and X == X and X != " ") return X
            return _board[winningCombo[0]]
    return " "  # no winner


def nextTurn():
    global turn

    if turn == "X":
        turn = "O"
    else:
        turn = "X"

    if (turn == computer):
        # get a random slot in the array empty strings
        randomLabel = random.choice(availableSpaces())
        # function call and passing label its positions
        click(Labels[randomLabel], int(randomLabel % 3), int(randomLabel/3))


def availableSpaces():
    emptyArr = [] # creating array which will hold items like " "
    for i in range(len(board)):
        if (board[i] == " "): # if element is not X and/or O add this element to the empty array
            emptyArr.append(i)
    return emptyArr


def clean():
    global board, timeWhenStarted
    timeWhenStarted = pd.datetime.now() # current time
    board = [" "] * 9 # cleaning the board
    for x in range(3):
        for y in range(3):
            addLabel(frame, " ", x, y) # cleaning the labels


def saveStats(winner):
    global tieGames, wins, loses, winRate, loseRate, gamesPlayed, timeWhenStarted, timeWhenEnded, gameInfo
    if (winner == "X"):
        wins += 1 # increasing number of wins
        winRate = wins / (wins + loses) * 100 # calculating winrate
    elif (winner == "O"):
        loses += 1
        loseRate = loses / (wins + loses) * 100
    else:
        tieGames += 1

    duration = timeWhenEnded - timeWhenStarted # calculation difference
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    gamesPlayed = wins + loses + tieGames

    if (winner == " "):
        winner = "Tie"


    gameInfo[gamesPlayed] = {"Game №": gamesPlayed, "Game result": winner if winner ==
                             "Tie" else winner + " won", "Duration": str(minutes) + "min" + ":" + str(seconds) + "sec"}


def click(label, x, y):
    global turn, timeWhenEnded
    label["text"] = turn # changing text of label to turn (X or O)
    board[x + y * 3] = turn # changing array's element to turn e.g. if x = 1, y = 2 then 1 + 2 * 3 = 7 that means board[7] = turn (x or O)
    label.unbind("<Button-1>") # once label is clicked it cannot be clicked again
    winner = findWinner(board) # finding winner
    if (len((availableSpaces())) == 0 and winner == " "): # if the length of board == 0 and winner = " " then its a tie game
        timeWhenEnded = pd.datetime.now() # saving time
        messagebox.showinfo("Tie", "it's a tie...") # popup with a message
        unbindLabels() # making all label unclickable
        showStatsBtn.pack() # show button to see stats
        cleanBtn.pack() # show button to clear board
        saveStats(winner) # saving game data
        turn = None 
    if (winner != " "):
        timeWhenEnded = pd.datetime.now()
        messagebox.showinfo("Win!", winner + " has won!")
        unbindLabels()
        saveStats(winner)
        showStatsBtn.pack()
        cleanBtn.pack()
        turn = None
    nextTurn() # proceed to next turn (computer or user)


def unbindLabels():
    for label in frame.winfo_children(): # in labels
        label.unbind("<Button-1>") # removing click event


def addLabel(frame, text, x, y): # creating squares
    label = Label(
        frame,
        text=text,
        font=("Arial ", 32),
        borderwidth=10,
        relief="ridge",
        width=2,
        bg="white")
    label.grid(row=y, column=x, padx=10, pady=10)
    label.bind("<Button-1>", lambda event: click(label, x, y))
    Labels[x + y * 3] = label


def showStats():
    statsWindow = Tk()
    statsWindow.wm_title("Game results")
    statsFrame = Frame(statsWindow)

    winsLabel = Label(
        statsFrame,
        text="Wins: " + str(wins),
        font=("Arial", 16),
        width=15)

    winsLabel.pack()

    losesLabel = Label(
        statsFrame,
        text="Loses: " + str(loses),
        font=("Arial", 16),
        width=15)

    losesLabel.pack()

    tiesLabel = Label(
        statsFrame,
        text="Tie games: " + str(tieGames),
        font=("Arial", 16),
        width=15)

    tiesLabel.pack()

    gamesPlayedLabel = Label(
        statsFrame,
        text="Games played: " + str(gamesPlayed),
        font=("Arial", 16),
        width=15)

    gamesPlayedLabel.pack()

    for stat in gameInfo:
        text = str(gameInfo[stat]).replace(
            "{", "").replace("}", "").replace("'", "") # removing unnecessary chars
        statLabel = Label(
            statsFrame,
            text=text,
            font=("Arial", 16),
            width=60
        )
        statLabel.pack()

    # winrate, loserate display STARTING POINT
    if (wins != 0 or loses != 0): # if wins or loses = 0 no point to display chart
        labels = 'Winrate', 'Loserate'
        sizes = [winRate,  loseRate]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels,
                autopct='%1.1f%%', startangle=90, radius=0.5)
        ax1.axis('equal')
        fig1.set_size_inches(3.5, 3)

        pieCanvas = FigureCanvasTkAgg(fig1, master=statsWindow)
        pieCanvas.get_tk_widget().pack()
        pieCanvas.draw()
    # winrate, loserate display ENDING POINT

    statsFrame.pack()
    statsFrame.mainloop()


gameWindow = Tk()
gameWindow.wm_title("Tic Tac Toe")
frame = Frame(gameWindow)

showStatsBtn = Button(
    gameWindow,
    text="Show game results",
    width="20",
    height="2",
    padx="1",
    pady="1",
    command=showStats
)

startBtn = Button(
    gameWindow,
    text="Start",
    width="20",
    height="2",
    padx="1",
    pady="1",
    command=start)

cleanBtn = Button(
    gameWindow,
    text="Clean board",
    width="20",
    height="2",
    padx="1",
    pady="1",
    command=clean)

for x in range(3):
    for y in range(3):
        addLabel(frame, "", x, y)

startBtn.pack()
frame.mainloop()
