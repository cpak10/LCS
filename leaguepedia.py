import mwclient
from selenium import webdriver
import time
import pandas as pd

site = mwclient.Site('lol.gamepedia.com', path='/')

# filtering for specific tournament
page_to_query = 'Data:2020 Season World Championship/Play-In'

# calling games played, filtering for just link to match history
response = site.api('cargoquery',
	limit = 'max',
	tables = 'MatchScheduleGame=MSG, MatchSchedule=MS',
	fields = 'MSG.MatchHistory, MSG.Blue, MSG.Red, MS.Patch',
	where = r'MSG._pageName="%s" AND MSG.MatchHistory IS NOT NULL' % page_to_query,
    join_on = 'MSG.UniqueMatch=MS.UniqueMatch'
)
response = response.get('cargoquery')

# creating a list of match histories
match_histories = {}
count = 0
for i in response:
    match_info = i.get('title')
    history = match_info.get('MatchHistory')
    blue_team = match_info.get('Blue')
    red_team = match_info.get('Red')
    patch = match_info.get('Patch')
    match_histories[count] = [blue_team, red_team, patch, history]
    count += 1

# scraping the web data
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)
login_test = 'http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1531478?gameHash=24089c4324842f15'
driver.get(login_test)
time.sleep(10)

# there may be a bot detector for riot that prevents the auto input here
# login = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div/input')
# password = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/input')
# login.send_keys('squishycrispy')
# password.send_keys('[INSERT PASS]')
# login_button = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[1]/div/button')
# login_button.click()

# setting up final dict
database = {}
data_count = 0

def fill_database(i):
    global data_count
    driver.get(match_histories.get(i)[3])
    time.sleep(5)
    blue_result = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/header/div/div[1]/div[2]')
    blue_towers = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/footer/div/div/div[3]/span')
    red_result = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/header/div/div[1]/div[2]')
    red_towers = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div/footer/div/div/div[3]/span')
    game_time = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span[2]/div')

    # cleaning numbers
    blue_result = blue_result.text
    if blue_result == 'VICTORY':
        blue_result = 1
    else:
        blue_result = 0
    blue_towers = blue_towers.text
    red_result = red_result.text
    if red_result == 'VICTORY':
        red_result = 1
    else:
        red_result = 0
    red_towers = red_towers.text
    game_time = game_time.text
    game_time = game_time.split(':')
    minute = int(game_time[0])
    sec = round(int(game_time[1])/60, 2)
    game_time = int((minute + sec) * 60)

    # placing the items into the final dict
    op_match = match_histories.get(i)
    blue_team = op_match[0]
    red_team = op_match[1]
    patch = op_match[2]
    history = op_match[3]
    database[data_count] = [blue_team, patch, game_time, blue_towers, red_towers, blue_result]
    data_count += 1
    database[data_count] = [red_team, patch, game_time, red_towers, blue_towers, red_result]
    data_count += 1
    print(data_count)

# iterating through all matches
for i in match_histories:
    try:
        fill_database(i)
    except:
        driver.refresh()
        time.sleep(5)
        fill_database(i)
        print('refreshed')
	
# exporting the df
df = pd.DataFrame.from_dict(database, orient='index', columns=['team', 'patch', 'gamelength', 'towers', 'opp_towers', 'result'])
df.to_excel('update_data.xlsx')
print(df)
