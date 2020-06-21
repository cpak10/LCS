import pandas as pd

# user input
first_team = input('Enter Team 1: ')
second_team = input('Enter Team 2: ')
team_changes = input('Are there any changes to original roster? (Yes/No): ')
if team_changes == 'Yes':
    team_changed = input('Enter which team was changed: ')
    player_position = input('Enter player position here: ')
    old_player = input('Enter player to switch out: ')
    new_player = input('Enter player to switch in: ')
else:
    pass

# team data
team_dict = {'TL': ['Impact', 'Broxah', 'Jensen', 'Tactical', 'CoreJJ'], 'TSM': ['Broken Blade', 'Spica', 'Bjergsen', 'Doublelift', 'Biofrost'], 
'GG': ['Hauntzer', 'Closer', 'Damonte', 'FBI', 'Huhi'], '100T': ['ssumday', 'Meteos', 'Ryoma', 'Cody Sun', 'Stunt'], 'C9': ['Licorice', 'Blaber', 'Nisqy', 'Zven', 'Vulcan'], 
'CLG': ['Ruin', 'Wiggily', 'Pobelter', 'Stixxay', 'Smoothie'], 'DIG': ['V1PER', 'Akaadian', 'Froggen', 'Johnsun', 'Aphromoo'], 'EG': ['Kumo', 'Svenskeren', 'Jiizuke', 'Bang', 'Zeyzal'], 
'FLY': ['solo', 'Santorin', 'PowerOfEvil', 'WildTurtle', 'IgNar'], 'IMT': ['sOAZ', 'Potluck', 'Eika', 'Altec', 'Gate']}

# adjusted team
adjusted_team = []
team1_adj = 0
team2_adj = 0
try:
    if team_changed == first_team:
        team1_adj += 1
    if team_changed == second_team:
        team2_adj += 1
    else:
        pass
except NameError:
    pass

# operative teams
team1 = {0: [], 1: [], 2: [], 3: [], 4: []}
team2 = {0: [], 1: [], 2: [], 3: [], 4: []}

# adjusted team function
def adjust_team(team, old_player, new_player):
    adjusted_team = team_dict.get(team)
    for i in range(len(adjusted_team)):
        if adjusted_team[i] == old_player:
            adjusted_team[i] = new_player
        else:
            pass
    team_dict[team] = adjusted_team

# strength of sched
def strength_sched(team1, team2):
    team1_op = []
    team2_op = []
    team1_calc = []
    team2_calc = []
    team1_point_total = 0
    team2_point_total = 0
    matches = pd.read_excel('matches.xlsx')
    matches_narrow_team1 = matches.loc[matches['Team'] == first_team]
    matches_narrow_team2 = matches.loc[matches['Team'] == second_team]
    team1_num_matches = len(matches_narrow_team1.index)
    team2_num_matches = len(matches_narrow_team2.index)
    points = pd.read_excel('standings.xlsx')
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
    conversion_str_sch = team1_str_sch/team2_str_sch - 1
    print('Raw strength of schedule for ' + first_team + ': ' + str(conversion_str_sch))
    return conversion_str_sch

# filling player stats
def player_stats(row, team):
    player, position, dmg, gpm = row
    if position == 'TOP':
        team[0].append(player)
        team[0].append(position)
        team[0].append(dmg)
        team[0].append(gpm)
    if position == 'JUNGLE':
        team[1].append(player)
        team[1].append(position)
        team[1].append(dmg)
        team[1].append(gpm)
    if position == 'MID':
        team[2].append(player)
        team[2].append(position)
        team[2].append(dmg)
        team[2].append(gpm)
    if position == 'ADC':
        team[3].append(player)
        team[3].append(position)
        team[3].append(dmg)
        team[3].append(gpm)
    if position == 'SUPPORT':
        team[4].append(player)
        team[4].append(position)
        team[4].append(dmg)
        team[4].append(gpm)
    else:
        pass

# filling altered stats
def alt_player_stats(row):
    player, position, dmg, gpm = row
    for i in range(0, 4):
        if not team1.get(i):
            team1[i].append(player)
            team1[i].append(position)
            team1[i].append(dmg)
            team1[i].append(gpm)
        if not team2.get(i):
            team2[i].append(player)
            team2[i].append(position)
            team2[i].append(dmg)
            team2[i].append(gpm)
        else:
            pass

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
    print(team1_best, team2_best)
    # team1 
    team1_gold1 = team1.get(team1_best)[3]
    team2_gold1 = team2.get(team1_best)[3]
    team1_win_factor = team1_gold1/team2_gold1
    # team2
    team1_gold2 = team1.get(team2_best)[3]
    team2_gold2 = team2.get(team2_best)[3]
    team2_win_factor = team2_gold2/team1_gold2
    # total
    gold_total = team1_win_factor + team2_win_factor
    str_sched = strength_sched(first_team, second_team)
    team1_percentage = round(team1_win_factor/gold_total * 100 + (str_sched * 5), 2)
    team2_percentage = round(team2_win_factor/gold_total * 100 - (str_sched * 5), 2)
    # if adjusted
    if team1_adj > 0:
        position_index = {'TOP': 0, 'JUNGLE': 1, 'MID': 2, 'ADC': 3, 'SUPPORT': 4}
        dmg_total = 0
        for i in range(len(team1)):
            dmg_total += float(team1.get(i)[2])
        disc_dmg = 100 - dmg_total
        print(disc_dmg)
        if disc_dmg > 0:
            if team1_best == position_index.get(player_position):
                team1_percentage = round(team1_percentage - disc_dmg, 2)
                team2_percentage = round(team2_percentage + disc_dmg, 2)
            else:
                pass
        if disc_dmg < 0:
            if team1_best == position_index.get(player_position):
                team1_percentage = round(team1_percentage + disc_dmg, 2)
                team2_percentage = round(team2_percentage - disc_dmg, 2)
            else:
                pass
    if team2_adj > 0:
        position_index = {'TOP': 0, 'JUNGLE': 1, 'MID': 2, 'ADC': 3, 'SUPPORT': 4}
        dmg_total = 0
        for i in range(len(team2)):
            dmg_total += float(team2.get(i)[2])
        disc_dmg = 100 - dmg_total
        print('Damange discrepency with new player added: ' + str(disc_dmg))
        if disc_dmg > 0:
            if team2_best == position_index.get(player_position):
                team2_percentage = round(team2_percentage - disc_dmg, 2)
                team1_percentage = round(team1_percentage + disc_dmg, 2)
            else:
                pass
        if disc_dmg < 0:
            if team2_best == position_index.get(player_position):
                team2_percentage = round(team2_percentage + disc_dmg, 2)
                team1_percentage = round(team1_percentage - disc_dmg, 2)
            else:
                pass
    team1_percentage = str(team1_percentage) + '%'
    team2_percentage = str(team2_percentage) + '%'
    return team1_percentage, team2_percentage

# reading and applying data
if team_changes == 'No':
    stats = pd.read_excel('Stats.xlsx')
    stats['DMG%'] = pd.to_numeric(stats['DMG%'], errors='coerce').fillna(0)
    stats['GPM'] = pd.to_numeric(stats['GPM'], errors='coerce').fillna(0)
    team1_narrowed = stats.loc[stats['Player'].isin(team_dict.get(first_team))]
    team2_narrowed = stats.loc[stats['Player'].isin(team_dict.get(second_team))]
    team1_apply = team1_narrowed[['Player', 'Position', 'DMG%', 'GPM']]
    team2_apply = team2_narrowed[['Player', 'Position', 'DMG%', 'GPM']]
    team1_apply.apply(player_stats, axis=1, team=team1)
    team2_apply.apply(player_stats, axis=1, team=team2)
else:
    adjust_team(team_changed, old_player, new_player)
    stats = pd.read_excel('Stats.xlsx')
    stats['DMG%'] = pd.to_numeric(stats['DMG%'], errors='coerce').fillna(0)
    stats['GPM'] = pd.to_numeric(stats['GPM'], errors='coerce').fillna(0)
    team1_narrowed = stats.loc[stats['Player'].isin(team_dict.get(first_team))]
    team2_narrowed = stats.loc[stats['Player'].isin(team_dict.get(second_team))]
    team1_apply = team1_narrowed[['Player', 'Position', 'DMG%', 'GPM']]
    team2_apply = team2_narrowed[['Player', 'Position', 'DMG%', 'GPM']]
    team1_apply.apply(player_stats, axis=1, team=team1)
    team2_apply.apply(player_stats, axis=1, team=team2)
    stats_all = pd.read_excel('Stats_all.xlsx')
    first_new_player_narrowed = stats_all.loc[stats_all['Player'] == new_player]
    new_player_narrowed = first_new_player_narrowed.loc[stats_all['Position'] == player_position]
    new_player_narrowed['DMG%'] = pd.to_numeric(new_player_narrowed['DMG%'], errors='coerce').fillna(0)
    new_player_narrowed['GPM'] = pd.to_numeric(new_player_narrowed['GPM'], errors='coerce').fillna(0)
    new_player_narrowed_apply = new_player_narrowed[['Player', 'Position', 'DMG%', 'GPM']]
    new_player_narrowed_apply.apply(alt_player_stats, axis=1)

# result
print(first_team + ' and ' + second_team + ' will have a respective chance at winning: ' + str(top_player()))