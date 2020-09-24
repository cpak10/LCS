# the goal of this is to calibrate the regions to accurately predict this worlds
# essentially the model will calculate a certain team winning in the patch for playoffs and then the patch for world
# the difference will be the weight
# when moving from year to year, change the teams, the patch, and dataset
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import tensorboard
import datetime
import os

# stopping too much information from printing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(3)

# 2019 setting up regions here, MEGA in PCS was left out for lack of data
# 2018 ascension was left out in PCS
regions = {
    'NA': ['Immortals', 'Team SoloMid', 'Cloud9'],
    'KR': ['Samsung Galaxy', 'SK Telecom T1', 'Longzhu Gaming'],
    'CN': ['EDward Gaming', 'Team WE', 'Royal Never Give Up'],
    'EU': ['G2 Esports', 'Fnatic', 'Misfits Gaming'],
    'JAP': ['Rampage'],
    'PCS': ['ahq eSports Club', 'Hong Kong Attitude', 'Flash Wolves'],
    'BR': ['Team oNe eSports'],
    'CIS': ['Gambit Esports'],
    'LAT': ['Kaos Latin Gamers', 'Lyon Gaming'],
    'OCE': ['Dire Wolves'],
    'TR': ['1907 Esports'],
    'VCS': ['GAM Esports', 'Young Generation']
}

# difference dict
diff_dict ={
    'NA': [],
    'KR': [],
    'CN': [],
    'EU': [],
    'JAP': [],
    'PCS': [],
    'BR': [],
    'CIS': [],
    'LAT': [],
    'OCE': [],
    'TR': [],
    'VCS': []
}

# setting up patch information, only one patch, might want to narrow for last possible patch in region
playoff_patches = [6.12, 6.13, 6.14, 6.15, 6.16]
worlds_patch = [6.18]

# function for the model
def ml_playoffs(firstteam, secondteam, region):
    playoff_diff = 0
    worlds_diff = 0
    int_difference = 0
    for i in [playoff_patches, worlds_patch]:
        # reading the data from oracle's elixir, filtering down to just teams and operative columns
        df = pd.read_csv('2017 data.csv')
        df = df[['position', 'team', 'patch', 'gamelength', 'towers', 'opp_towers', 'result']]
        df = df.loc[df['position'] == 'team']
        trash = df.pop('position')

        # average towers per minute for teams in the past two patches
        team_gain_lost_time = {}
        def team_total_towers(row):
            team, patch, time, gain, lost, result = row
            if patch in i:
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
        team1 = team_total.loc[firstteam]
        prediction1 = model.predict([[team1[3], team1[4]]])
        prediction1 = round(float(prediction1) * 100, 2)
        print('Predicted win (raw) for {}: {}%'.format(firstteam, prediction1))
        team2 = team_total.loc[secondteam]
        prediction2 = model.predict([[team2[3], team2[4]]])
        prediction2 = round(float(prediction2) * 100, 2)
        print('Predicted win (raw) for {}: {}%'.format(secondteam, prediction2))
        percent1 = round((prediction1 / (prediction1 + prediction2)) * 100, 2)
        percent2 = round((prediction2 / (prediction1 + prediction2)) * 100, 2)
        print('Predicted win for {}: {}%'.format(firstteam, percent1))
        print('Predicted win for {}: {}%'.format(secondteam, percent2))
        difference = round((percent1 - percent2), 2)
        print('Difference is {}'.format(difference))
        if i == playoff_patches:
            playoff_diff = difference
        else:
            worlds_diff = difference
    int_difference = worlds_diff - playoff_diff
    region_append = diff_dict.get(region)
    region_append.append(int_difference)
    print(int_difference)

# inputs for teams and applying the teams
for h in regions:
    for i in regions.get(h):
        firstteam = i
        for j in regions:
            if j != h:
                for k in regions.get(j):
                    secondteam = k
                    ml_playoffs(i, k, h)

for i in diff_dict:
    avg_diff = sum(diff_dict.get(i))/len(diff_dict.get(i))
    diff_dict[i] = avg_diff
print(diff_dict)
