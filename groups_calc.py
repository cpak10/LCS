# this script should calculate the chances of each team making it out of their respective group
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import tensorboard
import datetime
import os

# setting up region averages
worlds_2019 = {
    'NA': 1.054666666666667, 'KR': 36.06533333333333, 'CN': 31.974000000000007, 'EU': 24.131999999999998,
    'JAP': -19.940909090909088, 'PCS': -14.320999999999996, 'BR': -69.27454545454546, 'CIS': -0.26181818181818123,
    'LAT': -12.009090909090908, 'OCE': -31.6, 'TR': -29.60727272727273, 'VCS': -27.500952380952384
}
worlds_2018 = {
    'NA': 15.561333333333334, 'KR': 1.8130000000000015, 'CN': 39.564666666666675, 'EU': 32.348333333333336, 
    'JAP': -34.01454545454545, 'PCS': -23.739, 'BR': -4.218181818181819, 'CIS': -1.3563636363636355, 
    'LAT': -45.89095238095236, 'OCE': -48.85, 'TR': 8.096363636363636, 'VCS': -10.815454545454543
}
worlds_2017 = {
    'NA': 0.9209523809523829, 'KR': 34.72476190476191, 'CN': 37.371428571428595, 'EU': 28.714285714285715, 
    'JAP': -70.00608695652173, 'PCS': -2.3431746031746044, 'BR': -19.016521739130436, 'CIS': -80.77304347826087, 
    'LAT': -28.496818181818185, 'OCE': -32.15304347826087, 'TR': 2.6973913043478253, 'VCS': -9.655
}
avg_group = {}
for i in [worlds_2019, worlds_2018, worlds_2017]:
    for j in i:
        if j not in avg_group:
            avg_group[j] = [i.get(j)]
        else:
            avg_group.get(j).append(i.get(j))
for i in avg_group:
    total = avg_group.get(i)
    avg_group[i] = [sum(total)/3]

# stopping too much information from printing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(3)

# setting up groups results dict here
results = {
    'groupa': {'G2 Esports': [0, 0, 'EU'], 'Suning': [0, 0, 'CN'], 'Machi Esports': [0, 0, 'PCS'], 'Team Liquid': [0, 0, 'NA']}, 
    'groupb': {'DAMWON Gaming': [0, 0, 'KR'], 'Rogue': [0, 0, 'EU'], 'JD Gaming': [0, 0, 'CN'], 'PSG Talon':[0, 0, 'PCS']},
    'groupc': {'Team SoloMid': [0, 0, 'NA'], 'Gen.G': [0, 0, 'KR'], 'Fnatic': [0, 0, 'EU'], 'LGD Gaming': [0, 0, 'CN']}, 
    'groupd': {'FlyQuest': [0, 0, 'NA'], 'DRX': [0, 0, 'KR'], 'Top Esports': [0, 0, 'CN'], 'MAD Lions': [0, 0, 'EU']}
}

playins = {
    'groupa': {'MAD Lions': [0, 0, 'EU'], 'Team Liquid': [0, 0, 'NA'], 'Papara SuperMassive': [0, 0, 'TR'], 'Legacy Esports': [0, 0, 'OCE'], 'INTZ': [0, 0, 'BR']},
    'groupb': {'V3 Esports': [0, 0, 'JAP'], 'PSG Talon': [0, 0, 'PCS'], 'Rainbow7': [0, 0, 'LAT'], 'Unicorns Of Love.CIS': [0, 0, 'CIS'], 'LGD Gaming': [0, 0, 'CN']}
}

# setting up patch information, only one patch
selected_patch = input('Enter current patch: ')
selected_patch = float(selected_patch)
previous_patch = selected_patch
patches = {selected_patch:0, previous_patch:0}


# function for the model
def ml(firstteam, secondteam, group):
    # reading the data from oracle's elixir, filtering down to just teams and operative columns
    df = pd.read_csv('data.csv')
    df = df[['position', 'team', 'patch', 'gamelength', 'towers', 'opp_towers', 'result']]
    df = df.loc[df['position'] == 'team']
    trash = df.pop('position')

    # average towers per minute for teams in the past two patches
    team_gain_lost_time = {}
    def team_total_towers(row):
        team, patch, time, gain, lost, result = row
        if patch in patches:
            if team in team_gain_lost_time:
                x, y, z = team_gain_lost_time.get(team)
                x += gain
                y += lost
                z += time
                team_gain_lost_time[team] = (x, y, z)
            else:
                team_gain_lost_time[team] = (gain, lost, time)
        else:
            pass
    df.apply(team_total_towers, axis=1)
    team_total = pd.DataFrame.from_dict(team_gain_lost_time, orient='index')
    # average towers taken per minute for teams 
    team_total[3] = team_total[0] / team_total[2]
    # average towers lost per minute for teams
    team_total[4] = team_total[1] / team_total[2]

    # average towers per minute for each individual game
    df['avg_gain'] = df['towers'] / df['gamelength']
    df['avg_loss'] = df['opp_towers'] / df['gamelength']

    # machine learning
    row, col = df.shape
    df = df[df.columns[-3:]]
    train_file = df.head(row-300)
    test_file = df.tail(300)
    train_result = train_file.pop('result')
    test_result = test_file.pop('result')
    tf.random.set_seed(10)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    # log_dir = 'logs/fit/' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    checkpoint_path = 'checkpoint/cp.ckpt'
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=True,
        verbose=1
    )
    # model.fit(train_file, train_result, epochs=10000, callbacks=[cp_callback])
    model.load_weights(checkpoint_path)
    test_loss, test_acc = model.evaluate(test_file, test_result)
    print('\n\nTest Loss: {}, Test Accuracy: {}'.format(test_loss, test_acc))
    
    # printing out the results, raw
    team1 = team_total.loc[firstteam]
    prediction1 = model.predict([[team1[3], team1[4]]])
    prediction1 = round(float(prediction1) * 100, 2)
    print('Predicted win (raw) for {}: {}%'.format(firstteam, prediction1))
    team2 = team_total.loc[secondteam]
    prediction2 = model.predict([[team2[3], team2[4]]])
    prediction2 = round(float(prediction2) * 100, 2)
    print('Predicted win (raw) for {}: {}%'.format(secondteam, prediction2))
    difference = round((prediction1 - prediction2), 2)
    print('Difference is {}'.format(difference))
    
    # calculating head-to-head percentages
    percent1 = round((prediction1 / (prediction1 + prediction2)) * 100, 2)
    percent2 = round((prediction2 / (prediction1 + prediction2)) * 100, 2)
    print('Predicted win for {} before region weights: {}%'.format(firstteam, percent1))
    print('Predicted win for {} before region weights: {}%'.format(secondteam, percent2))
    
    # weighing by region, take off after first round robin
    region_weight1 = playins.get(group)
    region_weight1 = region_weight1.get(firstteam)
    region_weight1 = region_weight1[2]
    region_weight1 = avg_group.get(region_weight1)[0]
    region_weight2 = playins.get(group)
    region_weight2 = region_weight2.get(secondteam)
    region_weight2 = region_weight2[2]
    region_weight2 = avg_group.get(region_weight2)[0]
    percent1 = round(percent1 + ((region_weight1 - region_weight2)/2), 2)
    percent2 = round(percent2 + ((region_weight2 - region_weight1)/2), 2)
    if percent1 > 100:
        percent1 = 100
    if percent1 < 0:
        percent1 = 0
    if percent2 > 100:
        percent2 = 100
    if percent2 < 0:
        percent2 = 0    
    print('Predicted win for {} after region weights: {}%'.format(firstteam, percent1))
    print('Predicted win for {} after region weights: {}%'.format(secondteam, percent2))

    # adding the results to the main dict
    if percent1 > percent2:
        specific_group = playins.get(group)
        specific_team = specific_group.get(firstteam)
        specific_team[0] = specific_team[0] + 1
        specific_team = specific_team.append(percent1)
    else:
        specific_group = playins.get(group)
        specific_team = specific_group.get(firstteam)
        specific_team[1] = specific_team[1] + 1
        specific_team = specific_team.append(percent1)

# inputs for teams and applying the teams
for h in playins:
    for i in playins.get(h):
        firstteam = i
        for j in playins.get(h):
            if j != i:
                secondteam = j
                ml(i, j, h)
print(playins)

# top two divided by 200, after first round robin, take number games needed to win for weach team and then find the percentage of winning those games
# for playins, add one more pop and number
for i in playins:
    op_group = playins.get(i)
    for j in op_group:
        op_team = op_group.get(j)
        num1 = op_team[3]
        num2 = op_team[4]
        num3 = op_team[5]
        num4 = op_team[6]
        op_list = []
        op_list.append(num1)
        # op_list.append(num2)
        op_min = min(op_list)
        if num2 > op_min:
            count = 0
            for k in op_list:
                if k == op_min:
                    op_list[count] = num2
                else:
                    count += 1
        op_min = min(op_list)
        if num3 > op_min:
            count = 0
            for k in op_list:
                if k == op_min:
                    op_list[count] = num3
                else:
                    count += 1
        op_min = min(op_list)
        if num4 > op_min:
            count = 0
            for k in op_list:
                if k == op_min:
                    op_list[count] = num4
                else:
                    count += 1
        percent_top2 = round((sum(op_list)/100) * 100, 2)
        op_team.pop(6)
        op_team.pop(5)
        op_team.pop(4)
        op_team.pop(3)
        op_team.append(percent_top2)

# creating dataframes with the results
groupa_df = pd.DataFrame.from_dict(playins.get('groupa'), orient='index', columns=['wins', 'losses', 'region', 'chance'])
groupa_df = groupa_df.sort_values(by='wins', ascending=False)
groupb_df = pd.DataFrame.from_dict(playins.get('groupb'), orient='index', columns=['wins', 'losses', 'region', 'chance'])
groupb_df = groupb_df.sort_values(by='wins', ascending=False)
# groupc_df = pd.DataFrame.from_dict(results.get('groupc'), orient='index', columns=['wins', 'losses', 'region', 'chance'])
# groupc_df = groupc_df.sort_values(by='wins', ascending=False)
# groupd_df = pd.DataFrame.from_dict(results.get('groupd'), orient='index', columns=['wins', 'losses', 'region', 'chance'])
# groupd_df = groupd_df.sort_values(by='wins', ascending=False)

print('\ngroup a')
print(groupa_df)
print('\ngroup b')
print(groupb_df)
print('\n')
# print('\ngroup c')
# print(groupc_df)
# print('\ngroup d')
# print(groupd_df)