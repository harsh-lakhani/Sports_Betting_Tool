import pandas as pd
from sklearn.metrics import classification_report
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier


def winning_team(goal_diff):
  if goal_diff > 0:
    return 1
  elif goal_diff == 0:
    return 0
  else:
    return -1


data = pd.read_csv("combined_data_laliga v1.csv")
df = pd.DataFrame(data)
df["goal_diff"] = df["Home Team Goals Scored"] - df["Away Team Goals Scored"]
df = df.drop('Score', axis=1)
df["Result"] = df.goal_diff.apply(lambda x:winning_team(x))

df = pd.get_dummies(df,columns=['Home Team','Away Team'],dtype = int)
X = df.loc[ : , [i for i in df.columns if i not in ["Ref", "Match Excitement","Location","Date","goal_diff", "Rain","year","Half Time Score", "Home Team Second Yellow Cards", "Away Team Second Yellow Cards","Home Team Goals Scored","Away Team Goals Scored","Home Team Goals Conceeded","Away Team Goals Conceeded"]]]
df_train = X[df["year"]<2020]
df_test = X[df["year"]>2019]
x_train = df_train.loc[:,df_train.columns != "Result"]
y_train = df_train.loc[:,"Result"]
x_test = df_test.loc[:,df_test.columns != "Result"]
y_test = df_test.loc[:,"Result"]

# Model 1
# lg = LGBMClassifier()
# lg.fit(x_train, y_train)
# y_pred_lg = lg.predict(x_test)
# print(classification_report(y_test, y_pred_lg))


# rf = RandomForestClassifier(criterion='entropy')
# rf.fit(x_train,y_train)
# Y_pred_rf = rf.predict(x_test)
# print(classification_report(y_test, Y_pred_rf))



gb = GradientBoostingClassifier()
gb.fit(x_train,y_train)
Y_pred_gb = gb.predict(x_test)
print(classification_report(y_test, Y_pred_gb))