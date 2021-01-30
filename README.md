# LCS
The following scripts are tools used to predict the outcome of League of Legends matches. The newest version of the match predictor uses a TensorFlow neural net 

money_ball.py is built from Oracle's Elixir's dataset: https://oracleselixir-downloadable-match-data.s3-us-west-2.amazonaws.com/2020_LoL_esports_match_data_from_OraclesElixir_20200908.csv

money_ball.py
- current iteration of the LCS prediction bot, uses machine learning

lcs_win.py
- old version of the LCS prediction bot, no longer in use

worlds_calibration.py
- analyzes the data from previous Worlds to find weights to apply to predict this Worlds

groups_calc.py
- calculates the chances of teams making it out of groups

leaguepedia.py
- creates a database of recent games pulled from leaguepedia
