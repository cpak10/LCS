import pandas as pd

stats = pd.read_excel('Stats.xlsx')
stats_all = pd.read_excel('Stats_all.xlsx')
matches = pd.read_excel('matches.xlsx')
points = pd.read_excel('standings.xlsx')

# user input
first_team = input('Enter Team 1: ')
second_team = input('Enter Team 2: ')
team_changes = input('Are there any changes to original roster? (Yes/No): ')
if team_changes == 'Yes':
    team_changed = input('Enter which team was changed: ')
    player_position = input('Enter player position here: ')
    old_player = input('Enter player to switch out: ')
    new_player = input('Enter player to switch in: ')
    more_changes = input('Are there more changes to the roster? (Yes/No): ')
    if more_changes == 'Yes':
        team_changed1 = input('Enter which team was changed: ')
        player_position1 = input('Enter player position here: ')
        old_player1 = input('Enter player to switch out: ')
        new_player1 = input('Enter player to switch in: ')
        more_changes1 = input('Are there more changes to the roster? (Yes/No): ')
        if more_changes1 == 'Yes':
            team_changed2 = input('Enter which team was changed: ')
            player_position2 = input('Enter player position here: ')
            old_player2 = input('Enter player to switch out: ')
            new_player2 = input('Enter player to switch in: ')
            more_changes2 = input('Are there more changes to the roster? (Yes/No): ')
            if more_changes2 == 'Yes':
                team_changed3 = input('Enter which team was changed: ')
                player_position3 = input('Enter player position here: ')
                old_player3 = input('Enter player to switch out: ')
                new_player3 = input('Enter player to switch in: ')
                more_changes3 = input('Are there more changes to the roster? (Yes/No): ')
                if more_changes3 == 'Yes':
                    team_changed4 = input('Enter which team was changed: ')
                    player_position4 = input('Enter player position here: ')
                    old_player4 = input('Enter player to switch out: ')
                    new_player4 = input('Enter player to switch in: ')
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass
else:
    pass

# team data
team_dict = {
            'TL': ['Impact', 'Broxah', 'Jensen', 'Tactical', 'CoreJJ'], 
            'TSM': ['Broken Blade', 'Spica', 'Bjergsen', 'Doublelift', 'Biofrost'], 
            'GG': ['Hauntzer', 'Closer', 'Damonte', 'FBI', 'Huhi'], 
            '100T': ['ssumday', 'Contractz', 'Ryoma', 'Cody Sun', 'Poome'], 
            'C9': ['Licorice', 'Blaber', 'Nisqy', 'Zven', 'Vulcan'], 
            'CLG': ['Ruin', 'Wiggily', 'Pobelter', 'Stixxay', 'Smoothie'], 
            'DIG': ['Lourlo', 'Dardoch', 'FeniX', 'Johnsun', 'Aphromoo'], 
            'EG': ['Kumo', 'Svenskeren', 'Jiizuke', 'Bang', 'Zeyzal'], 
            'FLY': ['solo', 'Santorin', 'PowerOfEvil', 'Mash', 'IgNar'], 
            'IMT': ['allorim', 'Xmithie', 'Insanity', 'Apollo', 'Hakuho']
}

# adjusted team
adjusted_team = []

# operative teams
team1 = {0: [], 1: [], 2: [], 3: [], 4: []}
team2 = {0: [], 1: [], 2: [], 3: [], 4: []}

# adjusted team function
def adjust_team(team, switchout_player, switchin_player):
    adjusted_team = team_dict.get(team)
    for i in range(len(adjusted_team)):
        if adjusted_team[i] == switchout_player:
            adjusted_team[i] = switchin_player
        else:
            pass
    team_dict[team] = adjusted_team
    adjusted_team = []

# average position stats
positions = {'TOP': 0, 'JUNGLE': 0, 'MID': 0, 'ADC': 0, 'SUPPORT': 0}
def avg_position_stat():
    for role in positions:
        position_stats = stats.loc[stats['Position'] == role]
        sum_all_position = position_stats['GPM'].sum()
        row_count = position_stats.shape[0]
        position_avg = sum_all_position/row_count
        positions[role] = position_avg
    print('Here are the average gold stats for each position: ' + str(positions))
avg_position_stat()

# strength of sched
def strength_sched(team1, team2):
    team1_op = []
    team2_op = []
    team1_calc = []
    team2_calc = []
    team1_point_total = 0
    team2_point_total = 0
    matches_narrow_team1 = matches.loc[matches['Team'] == first_team]
    matches_narrow_team2 = matches.loc[matches['Team'] == second_team]
    team1_num_matches = len(matches_narrow_team1.index)
    team2_num_matches = len(matches_narrow_team2.index)
    for i in range(team1_num_matches):
        team1_op.append(matches_narrow_team1.iloc[i]['Oppose'])
    for i in range(len(team1_op)):
        asso_point = points.loc[points['Team'] == team1_op[i]]
        team1_calc.append(asso_point.iloc[0]['Points'])
    for i in range(team2_num_matches):
        team2_op.append(matches_narrow_team2.iloc[i]['Oppose'])
    for i in range(len(team2_op)):
        asso_point = points.loc[points['Team'] == team2_op[i]]
        team2_calc.append(asso_point.iloc[0]['Points'])
    for i in team1_calc:
        team1_point_total += i
    for i in team2_calc:
        team2_point_total += i
    team1_str_sch = team1_point_total / team1_num_matches
    team2_str_sch = team2_point_total / team2_num_matches
    total_point_total = team1_str_sch + team2_str_sch
    team1_str = team1_str_sch / total_point_total
    team2_str = team2_str_sch / total_point_total
    conversion_str_sch = (team1_str - team2_str) * 10
    print('Raw strength of schedule for ' + first_team + ': ' + str(round(conversion_str_sch, 2)))
    return conversion_str_sch

# filling player stats
def player_stats(row, team):
    player, position, dmg, gpm, win = row
    if position == 'TOP':
        team[0].append(player)
        team[0].append(position)
        team[0].append(dmg)
        team[0].append(gpm)
        team[0].append(win)
    if position == 'JUNGLE':
        team[1].append(player)
        team[1].append(position)
        team[1].append(dmg)
        team[1].append(gpm)
        team[1].append(win)
    if position == 'MID':
        team[2].append(player)
        team[2].append(position)
        team[2].append(dmg)
        team[2].append(gpm)
        team[2].append(win)
    if position == 'ADC':
        team[3].append(player)
        team[3].append(position)
        team[3].append(dmg)
        team[3].append(gpm)
        team[3].append(win)
    if position == 'SUPPORT':
        team[4].append(player)
        team[4].append(position)
        team[4].append(dmg)
        team[4].append(gpm)
        team[4].append(win)
    else:
        pass

# filling altered stats
position_index = {
                    'TOP': 0,
                    'JUNGLE': 1,
                    'MID': 2,
                    'ADC': 3,
                    'SUPPORT': 4
                    }
def alt_player_stats(row, position, team):
    player, position, dmg, gpm, win = row
    switch_player = position_index.get(position)
    if team == first_team:
        team1[switch_player].append(player)
        team1[switch_player].append(position)
        team1[switch_player].append(dmg)
        team1[switch_player].append(gpm)
        team1[switch_player].append(win)
    if team == second_team:
        team2[switch_player].append(player)
        team2[switch_player].append(position)
        team2[switch_player].append(dmg)
        team2[switch_player].append(gpm)
        team2[switch_player].append(win)
    else:
        pass

# refactor position index
rev_position_index = {
                0: 'TOP',
                1: 'JUNGLE',
                2: 'MID',
                3: 'ADC',
                4: 'SUPPORT'
                }
def player_stats_win(player):
    best_position = rev_position_index.get(player)
    position_average = positions.get(best_position)
    team1_player_win = team1.get(player)[4] * 100
    team2_player_win = team2.get(player)[4] * 100
    team1_gold = team1.get(player)[3]
    team2_gold = team2.get(player)[3]
    if team1_gold > position_average:
        gold_perf1 = ((team1_gold / position_average)**3) * ((200 - team1_player_win)/100)
    if team2_gold > position_average:
        gold_perf2 = ((team2_gold / position_average)**3) * ((200 - team2_player_win)/100)
    if team1_gold < position_average:
        gold_perf1 = ((team1_gold / position_average)**3) / ((team1_player_win + 100)/100)
    if team2_gold < position_average:
        gold_perf2 = ((team2_gold / position_average)**3) / ((team2_player_win + 100)/100)
    return (gold_perf1/gold_perf2 * 100)

def player_stats_win2(player):
    best_position = rev_position_index.get(player)
    position_average = positions.get(best_position)
    team1_player_win = team1.get(player)[4] * 100
    team2_player_win = team2.get(player)[4] * 100
    team1_gold = team1.get(player)[3]
    team2_gold = team2.get(player)[3]
    if team1_gold > position_average:
        gold_perf1 = ((team1_gold / position_average)**3) * ((200 - team1_player_win)/100)
    if team2_gold > position_average:
        gold_perf2 = ((team2_gold / position_average)**3) * ((200 - team2_player_win)/100)
    if team1_gold < position_average:
        gold_perf1 = ((team1_gold / position_average)**3) / ((team1_player_win + 100)/100)
    if team2_gold < position_average:
        gold_perf2 = ((team2_gold / position_average)**3) / ((team2_player_win + 100)/100)
    return (gold_perf2/gold_perf1 * 100)

# finding top players and further calculation
def top_player():
    print('Stats of ' + first_team + ': ' + str(team1))
    print('Stats of ' + second_team + ': ' + str(team2))
    team1_dmg = []
    team2_dmg = []
    for player in team1:
        team1_dmg.append(team1.get(player)[2])
    for player in team2:
        team2_dmg.append(team2.get(player)[2])
    team1_best = team1_dmg.index(max(team1_dmg))
    team2_best = team2_dmg.index(max(team2_dmg))
    team1_raw = player_stats_win(team1_best)
    print('Here is ' + first_team + ' raw number: ' + str(round(team1_raw)))
    team2_raw = player_stats_win2(team2_best)
    print('Here is ' + second_team + ' raw number: ' + str(round(team2_raw)))

    # carry potential
    carry_player1 = team1.get(team1_best)[0]
    carry_player1_role = team1.get(team1_best)[1]
    carry_player1_loc1 = stats_all.loc[stats_all['Player'] == carry_player1]
    carry_player1_loc2 = carry_player1_loc1.loc[carry_player1_loc1['Position'] == carry_player1_role]
    carry_player1_dmg = carry_player1_loc2.iloc[0]['DMG%']
    carry_player1_win = carry_player1_loc2.iloc[0]['Win rate']
    carry_player1_potential = carry_player1_dmg * carry_player1_win
    carry_player2 = team2.get(team2_best)[0]
    carry_player2_role = team2.get(team2_best)[1]
    carry_player2_loc1 = stats_all.loc[stats_all['Player'] == carry_player2]
    carry_player2_loc2 = carry_player2_loc1.loc[carry_player2_loc1['Position'] == carry_player2_role]
    carry_player2_dmg = carry_player2_loc2.iloc[0]['DMG%']
    carry_player2_win = carry_player2_loc2.iloc[0]['Win rate']
    carry_player2_potential = carry_player2_dmg * carry_player2_win
    print(carry_player1 + ' of ' + first_team + ' has a carry potential of: ' + str(round(carry_player1_potential, 2)))
    print(carry_player2 + ' of ' + second_team + ' has a carry potential of: ' + str(round(carry_player2_potential, 2)))

    # team1 
    team1_win_factor = team1_raw + (carry_player1_potential * 2)
    
    # team2
    team2_win_factor = team2_raw + (carry_player2_potential * 2)
    
    # total
    gold_total = team1_win_factor + team2_win_factor
    str_sched = strength_sched(first_team, second_team)
    team1_percentage = round(team1_win_factor/gold_total * 100 + (str_sched), 2)
    team2_percentage = round(team2_win_factor/gold_total * 100 - (str_sched), 2)
    
    # damage discrepency
    dmg_total1 = 0
    for i in range(len(team1)):
        dmg_total1 += float(team1.get(i)[2])
    disc_dmg1 = 100 - dmg_total1
    print('Damange discrepency for ' + first_team + ' with new player added: ' + str(round(disc_dmg1, 2)))
    if disc_dmg1 > 0:
        team1_percentage -= round(disc_dmg1, 2)
        team2_percentage += round(disc_dmg1, 2)
    if disc_dmg1 < 0:
        team1_percentage += round(disc_dmg1, 2)
        team2_percentage -= round(disc_dmg1, 2)
    dmg_total2 = 0
    for i in range(len(team2)):
        dmg_total2 += float(team2.get(i)[2])
    disc_dmg2 = 100 - dmg_total2
    print('Damange discrepency for ' + second_team + ' with new player added: ' + str(round(disc_dmg2, 2)))
    if disc_dmg2 > 0:
        team2_percentage -= round(disc_dmg2, 2)
        team1_percentage += round(disc_dmg2, 2)
    if disc_dmg2 < 0:
        team2_percentage += round(disc_dmg2, 2)
        team1_percentage -= round(disc_dmg2, 2)
    team1_percentage = str(round(team1_percentage, 2)) + '%'
    team2_percentage = str(round(team2_percentage, 2)) + '%'
    return team1_percentage, team2_percentage

# reading and applying data
if team_changes == 'No':
    stats['DMG%'] = pd.to_numeric(stats['DMG%'], errors='coerce').fillna(0)
    stats['GPM'] = pd.to_numeric(stats['GPM'], errors='coerce').fillna(0)
    team1_narrowed = stats.loc[stats['Player'].isin(team_dict.get(first_team))]
    team2_narrowed = stats.loc[stats['Player'].isin(team_dict.get(second_team))]
    team1_apply = team1_narrowed[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
    team2_apply = team2_narrowed[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
    team1_apply.apply(player_stats, axis=1, team=team1)
    team2_apply.apply(player_stats, axis=1, team=team2)
else:
    adjust_team(team_changed, old_player, new_player)
    if more_changes == 'Yes':
        adjust_team(team_changed1, old_player1, new_player1)
        if more_changes1 == 'Yes':
            adjust_team(team_changed2, old_player2, new_player2)
            if more_changes2 == 'Yes':
                adjust_team(team_changed3, old_player3, new_player3)
                if more_changes3 == 'Yes':
                    adjust_team(team_changed4, old_player4, new_player4)
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass
    stats['DMG%'] = pd.to_numeric(stats['DMG%'], errors='coerce').fillna(0)
    stats['GPM'] = pd.to_numeric(stats['GPM'], errors='coerce').fillna(0)
    team1_narrowed = stats.loc[stats['Player'].isin(team_dict.get(first_team))]
    team2_narrowed = stats.loc[stats['Player'].isin(team_dict.get(second_team))]
    team1_apply = team1_narrowed[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
    team2_apply = team2_narrowed[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
    team1_apply.apply(player_stats, axis=1, team=team1)
    team2_apply.apply(player_stats, axis=1, team=team2)
    first_new_player_narrowed = stats_all.loc[stats_all['Player'] == new_player]
    new_player_narrowed = first_new_player_narrowed.loc[stats_all['Position'] == player_position]
    new_player_narrowed['DMG%'] = pd.to_numeric(new_player_narrowed['DMG%'], errors='coerce').fillna(0)
    new_player_narrowed['GPM'] = pd.to_numeric(new_player_narrowed['GPM'], errors='coerce').fillna(0)
    new_player_narrowed_apply = new_player_narrowed[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
    new_player_narrowed_apply.apply(alt_player_stats, axis=1, position=player_position, team=team_changed)
    if more_changes == 'Yes':
        second_new_player_narrowed = stats_all.loc[stats_all['Player'] == new_player1]
        new_player_narrowed1 = second_new_player_narrowed.loc[stats_all['Position'] == player_position1]
        new_player_narrowed1['DMG%'] = pd.to_numeric(new_player_narrowed1['DMG%'], errors='coerce').fillna(0)
        new_player_narrowed1['GPM'] = pd.to_numeric(new_player_narrowed1['GPM'], errors='coerce').fillna(0)
        new_player_narrowed_apply1 = new_player_narrowed1[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
        new_player_narrowed_apply1.apply(alt_player_stats, axis=1, position=player_position1, team=team_changed1)
        if more_changes1 == 'Yes':
            third_new_player_narrowed = stats_all.loc[stats_all['Player'] == new_player2]
            new_player_narrowed2 = third_new_player_narrowed.loc[stats_all['Position'] == player_position2]
            new_player_narrowed2['DMG%'] = pd.to_numeric(new_player_narrowed2['DMG%'], errors='coerce').fillna(0)
            new_player_narrowed2['GPM'] = pd.to_numeric(new_player_narrowed2['GPM'], errors='coerce').fillna(0)
            new_player_narrowed_apply2 = new_player_narrowed2[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
            new_player_narrowed_apply2.apply(alt_player_stats, axis=1, position=player_position2, team=team_changed2)
            if more_changes2 == 'Yes':
                fourth_new_player_narrowed = stats_all.loc[stats_all['Player'] == new_player3]
                new_player_narrowed3 = fourth_new_player_narrowed.loc[stats_all['Position'] == player_position3]
                new_player_narrowed3['DMG%'] = pd.to_numeric(new_player_narrowed3['DMG%'], errors='coerce').fillna(0)
                new_player_narrowed3['GPM'] = pd.to_numeric(new_player_narrowed3['GPM'], errors='coerce').fillna(0)
                new_player_narrowed_apply3 = new_player_narrowed3[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
                new_player_narrowed_apply3.apply(alt_player_stats, axis=1, position=player_position3, team=team_changed3)
                if more_changes3 == 'Yes':
                    fifth_new_player_narrowed = stats_all.loc[stats_all['Player'] == new_player4]
                    new_player_narrowed4 = fifth_new_player_narrowed.loc[stats_all['Position'] == player_position4]
                    new_player_narrowed4['DMG%'] = pd.to_numeric(new_player_narrowed4['DMG%'], errors='coerce').fillna(0)
                    new_player_narrowed4['GPM'] = pd.to_numeric(new_player_narrowed4['GPM'], errors='coerce').fillna(0)
                    new_player_narrowed_apply4 = new_player_narrowed4[['Player', 'Position', 'DMG%', 'GPM', 'Win rate']]
                    new_player_narrowed_apply4.apply(alt_player_stats, axis=1, position=player_position4, team=team_changed4)
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

# result
print(first_team + ' and ' + second_team + ' will have a respective chance at winning: ' + str(top_player()))