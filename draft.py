import pandas as pd
import matplotlib.pylab as plt

# input first team
first_team = input('Enter first team here: ')
first_1 = input('Enter champion here: ')
first_2 = input('Enter champion here: ')
first_3 = input('Enter champion here: ')
first_4 = input('Enter champion here: ')
first_5 = input('Enter champion here: ')

# input second team
second_team = input('Enter second team here: ')
second_1 = input('Enter champion here: ')
second_2 = input('Enter champion here: ')
second_3 = input('Enter champion here: ')
second_4 = input('Enter champion here: ')
second_5 = input('Enter champion here: ')

# lists
first_team_lst = [first_1, first_2, first_3, first_4, first_5]
second_team_lst = [second_1, second_2, second_3, second_4, second_5]

# team dictionaries does math
team1_dict = {
            15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0,
            21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0,
            27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0,
            33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0,
            39: 0, 40: 0, 41: 0, 42: 0, 43: 0, 44: 0,
            45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0,
            51: 0, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0,
            57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0,
}
team2_dict = {
            15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0,
            21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0,
            27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0,
            33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0,
            39: 0, 40: 0, 41: 0, 42: 0, 43: 0, 44: 0,
            45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0,
            51: 0, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0,
            57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0,
}

# calculator
def team_avg_time(close_time, team):
    if close_time == 0:
        return
    if team == first_team:
        for i in range(-9, 10):
            time_var = close_time + i
            var = team1_dict.get(time_var)
            team1_dict[time_var] = var + (100 - (abs(i) * 10))
    if team == second_team:
        for i in range(-9, 10):
            time_var = close_time + i
            var = team2_dict.get(time_var)
            team2_dict[time_var] = var + (100 - (abs(i) * 10))
    else:
        pass

# odds calculator
def final_calc(time):
    team1 = team1_dict.get(time)
    team2 = team2_dict.get(time)
    total = team1 + team2
    if total == 0:
        return 'Almost no chance of either team winning at ' + str(time) + ' minutes.'
    else:
        team1_chance = round(team1/total * 100, 2)
        team2_chance = round(team2/total * 100, 2)
    return 'Chances at ' + str(time) + ' minutes for ' + first_team + ' to win is ' + str(team1_chance) + '%, ' + second_team + ' is ' + str(team2_chance) + '%.'

# read teams
team_stats = pd.read_excel('team_stats.xlsx')
team1_stats = team_stats.loc[team_stats['Name'] == first_team]
close_time = int(team1_stats['Game Duration'])
print('Average time for ' + first_team + ' to close out a game: ' + str(close_time))
team_avg_time(close_time, first_team)
team2_stats = team_stats.loc[team_stats['Name'] == second_team]
close_time2 = int(team2_stats['Game Duration'])
print('Average time for ' + second_team + ' to close out a game: ' + str(close_time2))
team_avg_time(close_time2, second_team)

# read champions first team
champ_stats = pd.read_excel('champion_stats.xlsx')
for i in first_team_lst:
    champ = champ_stats.loc[champ_stats['Champion'] == (i + ' ' + i)]
    champ_close = int(champ['GTR'])
    team_avg_time(champ_close, first_team)

# read champions second team
for i in second_team_lst:
    champ = champ_stats.loc[champ_stats['Champion'] == (i + ' ' + i)]
    champ_close = int(champ['GTR'])
    team_avg_time(champ_close, second_team)

# outputs
print(final_calc(20))
print(final_calc(25))
print(final_calc(30))
print(final_calc(35))
print(final_calc(40))
print(final_calc(45))
print(final_calc(50))
print(final_calc(55))
print(final_calc(close_time))
print(final_calc(close_time2))

# graph
team1_dict1 = {
            15: 'nan', 16: 'nan', 17: 'nan', 18: 'nan', 19: 'nan', 20: 'nan',
            21: 'nan', 22: 'nan', 23: 'nan', 24: 'nan', 25: 'nan', 26: 'nan',
            27: 'nan', 28: 'nan', 29: 'nan', 30: 'nan', 31: 'nan', 32: 'nan',
            33: 'nan', 34: 'nan', 35: 'nan', 36: 'nan', 37: 'nan', 38: 'nan',
            39: 'nan', 40: 'nan', 41: 'nan', 42: 'nan', 43: 'nan', 44: 'nan',
            45: 'nan', 46: 'nan', 47: 'nan', 48: 'nan', 49: 'nan', 50: 'nan',
            51: 'nan', 52: 'nan', 53: 'nan', 54: 'nan', 55: 'nan', 56: 'nan',
            57: 'nan', 58: 'nan', 59: 'nan', 60: 'nan', 61: 'nan', 62: 'nan',
}
team2_dict1 = {
            15: 'nan', 16: 'nan', 17: 'nan', 18: 'nan', 19: 'nan', 20: 'nan',
            21: 'nan', 22: 'nan', 23: 'nan', 24: 'nan', 25: 'nan', 26: 'nan',
            27: 'nan', 28: 'nan', 29: 'nan', 30: 'nan', 31: 'nan', 32: 'nan',
            33: 'nan', 34: 'nan', 35: 'nan', 36: 'nan', 37: 'nan', 38: 'nan',
            39: 'nan', 40: 'nan', 41: 'nan', 42: 'nan', 43: 'nan', 44: 'nan',
            45: 'nan', 46: 'nan', 47: 'nan', 48: 'nan', 49: 'nan', 50: 'nan',
            51: 'nan', 52: 'nan', 53: 'nan', 54: 'nan', 55: 'nan', 56: 'nan',
            57: 'nan', 58: 'nan', 59: 'nan', 60: 'nan', 61: 'nan', 62: 'nan',
}

def final_calc1(time):
    team1 = team1_dict.get(time)
    team2 = team2_dict.get(time)
    total = team1 + team2
    if total == 0:
        return 0
    else:
        team1_chance = round(team1/total * 100, 2)
    return team1_chance

def final_calc2(time):
    team1 = team1_dict.get(time)
    team2 = team2_dict.get(time)
    total = team1 + team2
    if total == 0:
        return 0
    else:
        team2_chance = round(team2/total * 100, 2)
    return team2_chance

for i in range(15, 63):
    team1_dict1[i] = final_calc1(i)
    team2_dict1[i] = final_calc2(i)
    if team1_dict1[i] == 0 or team1_dict1[i] == 100:
        team1_dict1.pop(i)
    if team2_dict1[i] == 0 or team2_dict1[i] == 100:
        team2_dict1.pop(i)

lists = sorted(team1_dict1.items())
x, y = zip(*lists)
lists2 = sorted(team2_dict1.items())
x1, y1 = zip(*lists2)
plt.plot(x, y, label=first_team)
plt.plot(x1, y1, label=second_team)
plt.xlabel('minutes')
plt.ylabel('percent chance of win')
plt.legend()
plt.show()