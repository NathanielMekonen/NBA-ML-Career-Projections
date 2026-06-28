import pandas as pd

source_file_path = '/Users/natemekonen/Desktop/Data_Projects/nba_ml_career_projections/data/processed'
dest_file_path = '/Users/natemekonen/Desktop/Data_Projects/nba_ml_career_projections/data/final'

# Load in csv files
per_game_df = pd.read_csv(f'{source_file_path}/per_game_stats.csv', index_col=0)
advanced_df = pd.read_csv(f'{source_file_path}/advanced_stats.csv', index_col=0)
per_poss_df = pd.read_csv(f'{source_file_path}/per_poss_stats.csv', index_col=0)
logos_df = pd.read_csv(f'{source_file_path}/team_logos.csv', index_col=0)

print('Transforming the data..')

# Merge the dataframes
per_game_advanced_df = per_game_df.merge(advanced_df, how='inner', on=['Player', 'Season'], suffixes=('_g', '_a'))

merged_df = per_game_advanced_df.merge(per_poss_df, how='inner', on=['Player', 'Season'], suffixes=('', '_p'))

# Drop unnecessary columns
columns_to_drop = ['Awards_g', 'Is_Allstar_g', 'Rk_a', 'Team_a', 'Pos_a', 'G_a', 'GS_a', 'Awards_a', 'Is_Allstar_a', 'Rk', 'Age', 'Team', 'Pos', 'G', 'GS', 'MP']

merged_df = merged_df.drop(columns=columns_to_drop)

# Get season number for each row
merged_df = merged_df.sort_values(by=['Player', 'Season'])

merged_df['Season_Num'] = merged_df.groupby('Player').cumcount() + 1

# Show players who were allstars after year 2
merged_df["AS_After_2"] = (
    merged_df["Is_Allstar"]
    .where(merged_df["Season_Num"] > 2, 0)
    .groupby(merged_df["Player"])
    .transform("max")
    .astype(int)
)

# Filter for player's first two seasons
merged_df = merged_df[merged_df['Season_Num'] <= 2]

# Fit first two seasons stats on one row
year_one_df = merged_df[merged_df['Season_Num'] == 1]

year_two_df = merged_df[merged_df['Season_Num'] == 2]

final_df = year_one_df.merge(year_two_df, how='left', on='Player', suffixes=['_y1', '_y2'])

# Drop unnecessary columns and rename column
columns_to_drop = ['Awards_y1', 'Is_Allstar_y1', 'Season_Num_y1', 'AS_After_2_y1', 'Rk_g_y2', 'Age_g_y2', 'Team_g_y2', 'Pos_g_y2', 'Awards_y2', 'Is_Allstar_y2', 'Season_Num_y2']

final_df = final_df.drop(columns=columns_to_drop)

final_df = final_df.rename(columns={'AS_After_2_y2' : 'AS_After_Year_Two'})

# Extract rookies and sophomores
headshot_df = pd.read_csv(f'{source_file_path}/rookie_sophomore_headshots.csv', index_col=0)

rookie_soph_df = final_df[final_df['Player'].isin(headshot_df['Player'])]

final_rookie_soph_df = rookie_soph_df.merge(headshot_df, how='inner', on='Player')

final_rookie_df = final_rookie_soph_df[final_rookie_soph_df['G_g_y2'].isna()].iloc[:, ~final_rookie_soph_df.columns.str.endswith("_y2")]

final_soph_df = final_rookie_soph_df[final_rookie_soph_df['G_g_y2'].notna()]

# Merge team logos to tables
final_soph_df = final_soph_df.merge(logos_df, how='left', left_on='Team_g_y1', right_on='team_abbr')

final_rookie_df = final_rookie_df.merge(logos_df, how='left', left_on='Team_g_y1', right_on='team_abbr')

# Filter df for non rookie/sophomores
final_df = final_df[~final_df['Player'].isin(headshot_df['Player'])]

final_soph_stats_total = final_df[final_df['G_g_y2'].notna()]

final_rookie_stats_total = final_soph_stats_total.iloc[:, ~final_soph_stats_total.columns.str.endswith("_y2")]

# Save csv
final_rookie_stats_total.to_csv(f'{dest_file_path}/final_rookie_stats_TOTAL.csv')
final_soph_stats_total.to_csv(f'{dest_file_path}/final_soph_stats_TOTAL.csv')
final_rookie_df.to_csv(f'{dest_file_path}/final_rookie_stats.csv')
final_soph_df.to_csv(f'{dest_file_path}/final_soph_stats.csv')

print('Transformations complete.')
