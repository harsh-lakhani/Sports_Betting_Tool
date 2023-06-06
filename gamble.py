from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pickle
import pandas as pd


def result():
    top = Toplevel(root,width=2000)
    msg = Message(top, text=do_pred(), width=2000)
    msg.pack()
    ext = Button(top, command=top.destroy, text="Exit")
    ext.pack()
    return 0


def do_pred():
    temperature = temp.get()
    hometeam = HOME.get()
    awayteam = AWAY.get()
    date_unprocessed = cal.get()

    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)
    f.close()

    data_home = pd.DataFrame(pd.read_csv('AveragesHome.csv'))
    data_away = pd.DataFrame(pd.read_csv('AveragesAway.csv'))
    home_entries = ['Home Team Rating', 'Home Team Possession %',
                    'Home Team Off Target Shots',
                    'Home Team On Target Shots', 'Home Team Total Shots',
                    'Home Team Blocked Shots', 'Home Team Corners',
                    'Home Team Throw Ins', 'Home Team Pass Success %',
                    'Home Team Aerials Won', 'Home Team Clearances', 'Home Team Fouls',
                    'Home Team Yellow Cards', 'Home Team Red Cards']
    away_entries = ['Away Team Rating', 'Away Team Possession %', 'Away Team Off Target Shots',
                    'Away Team On Target Shots',
                    'Away Team Total Shots', 'Away Team Blocked Shots',
                    'Away Team Corners', 'Away Team Throw Ins',
                    'Away Team Pass Success %', 'Away Team Aerials Won',
                    'Away Team Clearances', 'Away Team Fouls',
                    'Away Team Yellow Cards', 'Away Team Red Cards']

    # Construct X


    X = {}
    for var in home_entries:
        X[var] = float(data_home.loc[data_home['Row Labels'] == hometeam, " Average of " + var + " "].values[0])
        # X[0, var] = data_home.loc[data_home['Row Labels'] == hometeam, " Average of "+var + " "]
    for var in away_entries:
        X[var] = float(data_away.loc[data_away['Row Labels'] == awayteam, " Average of " + var + " "].values[0])
        # X[0, var] = data_away.loc[data_away['Row Labels'] == awayteam, " Average of "+var + " "]
    # X.loc[0,'temperature'] = temperature
    X['Temperature'] = float(temperature)

    home_team_list = ['Home Team_ALAVÉS', 'Home Team_ALMERÍA', 'Home Team_ATHLETIC',
                      'Home Team_ATLETICO MADRID', 'Home Team_BARCELONA',
                      'Home Team_CELTA', 'Home Team_CÁDIZ CF', 'Home Team_CÓRDOBA',
                      'Home Team_DEPORTIVO', 'Home Team_EIBAR', 'Home Team_ELCHE',
                      'Home Team_ESPANYOL', 'Home Team_GETAFE', 'Home Team_GIJÓN',
                      'Home Team_GIRONA', 'Home Team_GRANADA', 'Home Team_HUESCA',
                      'Home Team_LAS PALMAS', 'Home Team_LEGANÉS', 'Home Team_LEVANTE',
                      'Home Team_MALLORCA', 'Home Team_MÁLAGA', 'Home Team_OSASUNA',
                      'Home Team_RAYO VALLECANO', 'Home Team_REAL BETIS',
                      'Home Team_REAL MADRID', 'Home Team_REAL SOCIEDAD',
                      'Home Team_SEVILLA FC', 'Home Team_VALENCIA',
                      'Home Team_VALLADOLID', 'Home Team_VILLARREAL']
    away_team_list = ['Away Team_ALAVÉS',
                      'Away Team_ALMERÍA', 'Away Team_ATHLETIC',
                      'Away Team_ATLETICO MADRID', 'Away Team_BARCELONA',
                      'Away Team_CELTA', 'Away Team_CÁDIZ CF', 'Away Team_CÓRDOBA',
                      'Away Team_DEPORTIVO', 'Away Team_EIBAR', 'Away Team_ELCHE',
                      'Away Team_ESPANYOL', 'Away Team_GETAFE', 'Away Team_GIJÓN',
                      'Away Team_GIRONA', 'Away Team_GRANADA', 'Away Team_HUESCA',
                      'Away Team_LAS PALMAS', 'Away Team_LEGANÉS', 'Away Team_LEVANTE',
                      'Away Team_MALLORCA', 'Away Team_MÁLAGA', 'Away Team_OSASUNA',
                      'Away Team_RAYO VALLECANO', 'Away Team_REAL BETIS',
                      'Away Team_REAL MADRID', 'Away Team_REAL SOCIEDAD',
                      'Away Team_SEVILLA FC', 'Away Team_VALENCIA',
                      'Away Team_VALLADOLID', 'Away Team_VILLARREAL']

    for team in home_team_list:
        if hometeam == team.split('_')[1]:
            X[team] = 1
        else:
            X[team] = 0
    for team in away_team_list:
        if awayteam == team.split('_')[1]:
            X[team] = 1
        else:
            X[team] = 0
    X = pd.DataFrame.from_dict(X, orient='index').T
    X = X[list(clf.feature_names_in_)]
    y_pred = clf.predict(X)
    if y_pred[0] == 0:
        return "Draw"
    elif y_pred[0] == 1:
        return "Hometeam Wins"
    elif y_pred[0] == -1:
        return "Awayteam Wins"


root = Tk()
root.title("GAMblE")

ttk.Label(root, text="Date").grid(column=0, row=3)
ttk.Label(root, text="Temperature").grid(column=0, row=4)

HOME = StringVar()
ttk.Label(root, text="Home Team").grid(column=0, row=1)
home_team = ttk.Combobox(root, state='readonly', textvariable=HOME)
home_team['values'] = (
'ALAVÉS', 'ALMERÍA', 'ATHLETIC', 'ATLETICO MADRID', 'BARCELONA', 'CÁDIZ CF', 'CELTA', 'CÓRDOBA', 'DEPORTIVO', 'EIBAR',
'ELCHE', 'ESPANYOL', 'GETAFE', 'GIJÓN', 'GIRONA', 'GRANADA', 'HUESCA', 'LAS PALMAS', 'LEGANÉS', 'LEVANTE', 'MÁLAGA',
'MALLORCA', 'OSASUNA', 'RAYO VALLECANO', 'REAL BETIS', 'REAL MADRID', 'REAL SOCIEDAD', 'SEVILLA FC', 'VALENCIA',
'VALLADOLID', 'VILLARREAL',)
home_team.grid(column=1, row=1)
home_team.current(0)

AWAY = StringVar()
ttk.Label(root, text="Away Team").grid(column=0, row=2)
away_team = ttk.Combobox(root, textvariable=AWAY, state='readonly', )
away_team['values'] = (
'ALAVÉS', 'ALMERÍA', 'ATHLETIC', 'ATLETICO MADRID', 'BARCELONA', 'CÁDIZ CF', 'CELTA', 'CÓRDOBA', 'DEPORTIVO', 'EIBAR',
'ELCHE', 'ESPANYOL', 'GETAFE', 'GIJÓN', 'GIRONA', 'GRANADA', 'HUESCA', 'LAS PALMAS', 'LEGANÉS', 'LEVANTE', 'MÁLAGA',
'MALLORCA', 'OSASUNA', 'RAYO VALLECANO', 'REAL BETIS', 'REAL MADRID', 'REAL SOCIEDAD', 'SEVILLA FC', 'VALENCIA',
'VALLADOLID', 'VILLARREAL',)
away_team.grid(column=1, row=2)
away_team.current(0)

ttk.Label(root, text="Date").grid(column=0, row=3)
# date.grid(column=1, row=3)
cal = DateEntry(root, width=20, year=2022, month=11, day=24)
cal.grid(column=1, row=3)

ttk.Label(root, text="Temperature").grid(column=0, row=4)
temp = ttk.Entry(root, width=21)
temp.grid(column=1, row=4)

predict = ttk.Button(root, text="Predict", command=result)

predict.grid(column=0, columnspan=2, row=5)

root.mainloop()
