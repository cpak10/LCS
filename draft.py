from selenium import webdriver
import re
import time
import matplotlib.pylab as plt
from scipy.interpolate import interp1d
import numpy as np

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)

# input first team
team_name1 = input('Enter first team name here: ')
first_1 = input('Enter top champion here: ')
first_2 = input('Enter jungle champion here: ')
first_3 = input('Enter mid champion here: ')
first_4 = input('Enter adc champion here: ')
first_5 = input('Enter support champion here: ')

# input second team
team_name2 = input('Enter second team name here: ')
second_1 = input('Enter top champion here: ')
second_2 = input('Enter jungle champion here: ')
second_3 = input('Enter mid champion here: ')
second_4 = input('Enter adc champion here: ')
second_5 = input('Enter support champion here: ')

# dictionaries
first_team = {
    0: first_1,
    1: first_2,
    2: first_3,
    3: first_4,
    4: first_5
}

second_team = {
    0: second_1,
    1: second_2,
    2: second_3,
    3: second_4,
    4: second_5
}

positions = {
    0: 'Top',
    1: 'Jungle',
    2: 'Middle',
    3: 'ADC',
    4: 'Support'
}

team1_dict = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

team2_dict = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

time_dict = {
    0: 20,
    1: 25,
    2: 30,
    3: 40,
    4: 50
}

# calculating chance
def final_calc(time_index):
    timex = time_dict.get(time_index)
    total = team1_dict.get(time_index) + team2_dict.get(time_index)
    team1_chance = round(team1_dict.get(time_index)/total * 100, 2)
    team2_chance = round(team2_dict.get(time_index)/total * 100, 2)
    return 'Chances at ' + str(timex) + ' minutes for ' + team_name1 + ' to win is ' + str(team1_chance) + '%, ' + team_name2 + ' is ' + str(team2_chance) + '%.'

# web scraping
for i in range(0, 5):
    champ = first_team.get(i)
    champ_position = positions.get(i)
    driver.get('https://champion.gg/champion/' + champ + '/' + champ_position)
    time.sleep(1)
    html = driver.page_source
    time.sleep(1)
    game_length = html.find('\"gameLength\"')
    window = html[game_length:game_length+300]
    first_bracket = window.find('[')
    close_bracket = window.find(']') + 1
    stats_str = window[first_bracket:close_bracket]
    stats_str_replace = stats_str.replace('\"', ' ', 10)
    stats = re.findall(r'[\d\.\d]+', stats_str_replace)
    stats_int = [float(i) for i in stats]
    for i in range(len(stats_int)):
        team1_dict[i] = (stats_int[i]/100)**10 + team1_dict[i]

for i in range(0, 5):
    champ = second_team.get(i)
    champ_position = positions.get(i)
    driver.get('https://champion.gg/champion/' + champ + '/' + champ_position)
    time.sleep(1)
    html = driver.page_source
    time.sleep(1)
    game_length = html.find('\"gameLength\"')
    window = html[game_length:game_length+300]
    first_bracket = window.find('[')
    close_bracket = window.find(']') + 1
    stats_str = window[first_bracket:close_bracket]
    stats_str_replace = stats_str.replace('\"', ' ', 10)
    stats = re.findall(r'[\d\.\d]+', stats_str_replace)
    stats_int = [float(i) for i in stats]
    for i in range(len(stats_int)):
        team2_dict[i] = (stats_int[i]/100)**10 + team2_dict[i]

for i in range (0, 5):
    print(final_calc(i))

# plotting 
team1_dict1 = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

team2_dict1 = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

def final_calc1(time_index):
    timex = time_dict.get(time_index)
    total = team1_dict.get(time_index) + team2_dict.get(time_index)
    team1_chance = round(team1_dict.get(time_index)/total * 100, 2)
    return team1_chance

def final_calc2(time_index):
    timex = time_dict.get(time_index)
    total = team1_dict.get(time_index) + team2_dict.get(time_index)
    team2_chance = round(team2_dict.get(time_index)/total * 100, 2)
    return team2_chance

for i in range(0, 5):
    team1_dict1[i] = final_calc1(i)
    team2_dict1[i] = final_calc2(i)

lists = sorted(team1_dict1.items())
x1, y1 = zip(*lists)
lists2 = sorted(team2_dict1.items())
x2, y2 = zip(*lists2)
f1 = interp1d(x1, y1, kind='cubic')
f2 = interp1d(x2, y2, kind='cubic')
xnew1 = np.linspace(0, 4, 300)
xnew2 = np.linspace(0, 4, 300)
plt.plot(xnew1, f1(xnew1), label=team_name1)
plt.plot(xnew2, f2(xnew2), label=team_name2)
plt.xticks((0, 1, 2, 3, 4), ('20', '25', '30', '40', '50'))
plt.xlabel('minutes')
plt.ylabel('percent chance of win')
plt.legend()
plt.show()