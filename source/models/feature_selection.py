import pandas as pd

file_path = '/Users/natemekonen/Desktop/Data_Projects/nba_ml_career_projections/data/final'

columns_to_rename = {
    'Age_g_y1' : 'Age',
    'Pos_g_y1' : 'Position',
    'Season_y1' : 'Rookie_Season',
    'G_g_y1' : 'Games_Played_y1',
    'GS_g_y1' : 'Games_Started_y1',
    'MP_a_y1' : 'Total_Minutes_y1',
    'PTS_p_y1' : 'PTS_per100_y1',
    'TRB_p_y1' : 'TRB_per100_y1', 
    'AST_p_y1' : 'AST_per100_y1',
    'G_g_y2' : 'Games_Played_y2',
    'GS_g_y2' : 'Games_Started_y2',
    'MP_a_y2' : 'Total_Minutes_y2',
    'PTS_p_y2' : 'PTS_per100_y2', 
    'TRB_p_y2' : 'TRB_per100_y2', 
    'AST_p_y2' : 'AST_per100_y2'
}

soph_features = ['Player', 'Age_g_y1', 'Pos_g_y1', 'Season_y1', 'G_g_y1', 'GS_g_y1', 'MP_a_y1', 'PTS_y1', 'TRB_y1', 'AST_y1', 'STL_y1', 'BLK_y1', 'TOV_y1',
                'PER_y1', 'TS%_y1', 'USG%_y1', 'WS_y1', 'WS/48_y1', 'BPM_y1', 'VORP_y1', 'PTS_p_y1', 'TRB_p_y1', 'AST_p_y1',     
                'G_g_y2', 'GS_g_y2', 'MP_a_y2', 'PTS_y2', 'TRB_y2', 'AST_y2', 'STL_y2', 'BLK_y2', 'TOV_y2', 
                'PER_y2', 'TS%_y2', 'USG%_y2', 'WS_y2', 'WS/48_y2', 'BPM_y2', 'VORP_y2', 'PTS_p_y2', 'TRB_p_y2', 'AST_p_y2', 'AS_After_Year_Two']

rookie_features = ['Player', 'Age_g_y1', 'Pos_g_y1', 'Season_y1', 'G_g_y1', 'GS_g_y1', 'MP_a_y1', 'PTS_y1', 'TRB_y1', 'AST_y1', 'STL_y1', 'BLK_y1', 'TOV_y1',
                'PER_y1', 'TS%_y1', 'USG%_y1', 'WS_y1', 'WS/48_y1', 'BPM_y1', 'VORP_y1', 'PTS_p_y1', 'TRB_p_y1', 'AST_p_y1', 'AS_After_Year_Two']


# Helper Functions
def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns and encode categorical variables"""

    df = df.rename(columns=columns_to_rename)

    df = pd.get_dummies(df, columns=["Position"])

    return df


def load_features(filename: str, feature_columns: list[str]) -> pd.DataFrame:
    """Load and preprocess feature dataset."""

    df = pd.read_csv(file_path + '/' + filename)

    df = df.loc[:, df.columns.intersection(feature_columns)]

    return preprocess_features(df)


# Loading features functions
def load_rookie_features():
    return load_features("final_rookie_stats_TOTAL.csv", rookie_features)


def load_soph_features():
    return load_features("final_soph_stats_TOTAL.csv", soph_features)


def load_rookie_prediction_features():
    return load_features("final_rookie_stats.csv", rookie_features)


def load_soph_prediction_features():
    return load_features("final_soph_stats.csv", soph_features)