import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import tensorboard
import datetime
import os

# inputs for teams and current patch
firstteam = input('Enter first team: ')
secondteam = input('Enter second team: ')
selected_patch = input('Enter current patch: ')
selected_patch = float(selected_patch)
previous_patch = selected_patch - .01
patches = {selected_patch:0, previous_patch:0}

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
percent1 = round((prediction1 / (prediction1 + prediction2)) * 100, 2)
percent2 = round((prediction2 / (prediction1 + prediction2)) * 100, 2)
print('Predicted win for {}: {}%'.format(firstteam, percent1))
print('Predicted win for {}: {}%'.format(secondteam, percent2))