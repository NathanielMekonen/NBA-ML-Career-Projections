import pandas as pd

source_file_path = '/Users/natemekonen/Desktop/Data_Projects/nba_ml_career_projections/data/raw'
dest_file_path = '/Users/natemekonen/Desktop/Data_Projects/nba_ml_career_projections/data/processed'

def clean_and_concatenate(seasons, stat_type):
    """Clean and concatenate player stats tables"""

    print(f'Cleaning {stat_type} stats data..')

    all_dfs = []

    for season in seasons:
        df = pd.read_csv(f'{source_file_path}/{stat_type}/{season}_season_{stat_type}_stats.csv', index_col=0)

        # Data transformations
        df = df[df['Player'] != 'League Average']

        df.drop_duplicates(subset=['Rk', 'Player'], inplace=True)

        df['Is_Allstar'] = df['Awards'].str.contains('AS', na=False).astype(int)

        df['Season'] = str(season)

        df['Awards'] = df['Awards'].fillna('None')

        if stat_type == 'per_game' or stat_type == 'per_poss':
            df[['FG%', '3P%', '2P%', 'eFG%', 'FT%']] = df[['FG%', '3P%', '2P%', 'eFG%', 'FT%']].fillna(0)
        
        if stat_type == 'advanced':
            df[['TS%', '3PAr', 'FTr', 'TOV%']] = df[['TS%', '3PAr', 'FTr', 'TOV%']].fillna(0)
        
        # Add dataframe to list of dataframes
        all_dfs.append(df)

    print(f'Concatenating {stat_type} stats data..')

    # Concatenate dataframes
    final_df = pd.concat(all_dfs, ignore_index=True)

    # Save csv
    final_df.to_csv(f'{dest_file_path}/{stat_type}_stats.csv')

    print(f'{stat_type} stats data has been cleaned and concatenated.')


def concatenate_rookie_headshots(seasons):
    """Concatenate rookie headshot tables"""

    print(f'Concatenating rookie headshots..')
    
    all_dfs = []

    for season in seasons:
        df = pd.read_csv(f'{source_file_path}/rookie_sophomore/{season}_headshots.csv', index_col=0)

        # Data transformations
        df = df.dropna(subset=["Images"])

        df = df[(df["Player"] != "Totals") & (df["Player"] != "Player")]

        all_dfs.append(df)

    # Concatenate dataframes
    final_df = pd.concat(all_dfs, ignore_index=True)

    # Save csv
    final_df.to_csv(f'{dest_file_path}/rookie_sophomore_headshots.csv')

    print(f'Headshots have been concatenated.')


def map_shortened_team_names():
    """Add shortened team names to logos table"""

    df = pd.read_csv(f'{source_file_path}/rookie_sophomore/team_logos.csv', index_col=0)

    team_abbrev = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "LA Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
    }

    # Add abbreviation column
    df["team_abbr"] = df["team"].map(team_abbrev)

    # Save csv
    df.to_csv(f'{dest_file_path}/team_logos.csv')


def main():
    seasons = list(range(1990, 2027))
    clean_and_concatenate(seasons, 'per_game')
    clean_and_concatenate(seasons, 'advanced')
    clean_and_concatenate(seasons, 'per_poss')

    rookie_seasons = [2025, 2026]
    concatenate_rookie_headshots(rookie_seasons)

    map_shortened_team_names()


if __name__ == '__main__':
    main()