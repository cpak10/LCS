# LCS
The following scripts are tools used to predict the outcome of League of Legends matches. The newest version of the match predictor uses a TensorFlow neural net and fed public match data from Oracle's Elixir (link below). Based on previous match data for the two teams slotted to play, the NN is able to predict to a certain percentage point the likelihood a certain team has at winning an upcoming match.

An older version of the match predictor exists in this repository. The old version did not use a neural net. Instead, the older version tracked certain key metrics for each team using the same match data from Oracle's Elixir. It then used an algorithm to calculate the percentage chance each team had at winning against each other.

Oracle's Elixir Link: https://oracleselixir-downloadable-match-data.s3-us-west-2.amazonaws.com/2020_LoL_esports_match_data_from_OraclesElixir_20200908.csv

Match Predictor - money_ball.py
- This is the current version of the match predictor. It utilizes the TensorFlow neural net.

Older Match Predictor - lcs_win.py
- This is the old version of the match predictor. It is no longer in use.

Worlds: Worlds Calibrator - worlds_calibration.py
- This script was used to calculate weights in order to accurately predict matches on the international scene.

Worlds: Groups Calculator - groups_calc.py
- This script calculated the chances a certain team has at making it out of its group at Worlds.

Database Updater - leaguepedia.py
- If Oracle's Elixir does not have the most recent games data, this script parses the data on Leaguepedia and adds it to the database.
