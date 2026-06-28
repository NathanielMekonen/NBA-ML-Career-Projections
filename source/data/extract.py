from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
import time
from nba_api.stats.static import players

base_url = 'https://www.basketball-reference.com/leagues'
headshot_url = 'https://cdn.nba.com/headshots/nba/latest/1040x760'
logos_url = 'https://www.nba.com/teams'
headers = {'User-Agent': 'Mozilla/5.0'}
file_path = '/Users/natemekonen/Desktop/Data_Projects/nba_ml_career_projections/data/raw'
table_id_mapping = {
    'per_game': 'per_game_stats',
    'advanced': 'advanced',
    'per_poss': 'per_poss'
}

def nba_scrape(seasons, stat_type):
    """Scrape Basketball Reference player stats."""

    for season in seasons:
        print(f'Scraping {season} season {stat_type} stats..')

        url = f'{base_url}/NBA_{season}_{stat_type}.html'

        page = requests.get(url, headers=headers)
        page.encoding = 'utf-8'

        soup = BeautifulSoup(page.text, 'html.parser')

        # Find stats table
        table_id = table_id_mapping[stat_type]
        table = soup.find('table', id=table_id)

        if table is None:
            print(f'Could not find {stat_type} stats table for {season} season')
            continue
        
        # Extract column headers
        header_row = table.find('thead').find('tr').find_all('th')

        columns = [column['aria-label'] for column in header_row]

        # Extract rows
        rows = []

        body_rows = table.find('tbody').find_all('tr')

        for row in body_rows:

            player_data = row.find_all(['th','td'])

            row_values = [player.get_text(strip=True) for player in player_data]
            
            rows.append(row_values)
        
        # Create DataFrame
        season_df = pd.DataFrame(rows, columns=columns)

        # Save csv
        season_df.to_csv(file_path + f'/{stat_type}/{season}_season_{stat_type}_stats.csv')

        print(f'Saved to {season}_season_{stat_type}_stats.csv')

        time.sleep(random.uniform(4, 7))


def get_headshot(player):
    """Use NBA-API to obtain player headshots"""

    player_list = players.find_players_by_full_name(str(player))

    if not player_list:
        return None

    player_id = player_list[0]['id']

    image_url = f'{headshot_url}/{player_id}.png'

    return image_url


def headshot_map(df):
    """Map headshots to players"""

    players = df['Player']

    headshot_map = {}

    for player in players:
        headshot_map[player] = get_headshot(player)

    return headshot_map


def nba_rookies_scrape(seasons):
    """Scrape Basketball Reference for rookies and sophomores."""

    for season in seasons:
            
        url = f'{base_url}/NBA_{season}_rookies.html'

        page = requests.get(url, headers=headers)
        page.encoding = 'utf-8'

        soup = BeautifulSoup(page.text, 'html.parser')

        # Find stats table
        table = soup.find('table', id='rookies')

        if table is None:
            print(f'Could not find rookie stats table for {season} season')
            continue

        # Extract column headers
        header_row = table.find('thead').find_all('tr')[1].find_all('th')

        columns = [column['aria-label'] for column in header_row]

        # Extract rows
        rows = []

        body_rows = table.find('tbody').find_all('tr')

        for row in body_rows:

            player_data = row.find_all(['th','td'])

            row_values = [player.get_text(strip=True) for player in player_data]
            
            rows.append(row_values)

        # Create rookies DataFrame
        rookies_df = pd.DataFrame(rows, columns=columns)

        # Save csv
        rookies_df.to_csv(file_path + f'/rookie_sophomore/{season}_season_rookie_stats.csv')

        # Get rookie headshots
        headshot_mapping = headshot_map(rookies_df)

        rookies_df['Images'] = rookies_df['Player'].map(headshot_mapping)

        headshot_df = rookies_df[['Player', 'Images']]

        # Save csv
        headshot_df.to_csv(file_path + f'/rookie_sophomore/{season}_headshots.csv')

        print(f'Saved all rookie stats and headshots')

        time.sleep(random.uniform(4, 7))


def get_logos():
    """Scrape NBA.com for team logos."""

    url = logos_url

    page = requests.get(url, headers=headers)
    page.encoding = 'utf-8'

    soup = BeautifulSoup(page.text, 'html.parser')

    # Find images table
    images = soup.find_all("img")

    teams_logos = []

    # Get team name and logos for each team
    for img in soup.find_all("img"):
        src = img.get("src")
        alt = img.get("alt")

        if src and "cdn.nba.com/logos/nba" in src:

            team_name = alt.replace(" Logo", "") if alt else "Unknown"

            teams_logos.append({
                "team": team_name,
                "logo": src
            })

    # Create dataframe of teams and logos
    logos_df = pd.DataFrame(teams_logos)

    logos_df = logos_df.drop_duplicates()

    # Save csv
    logos_df.to_csv(file_path + f'/rookie_sophomore/team_logos.csv')



def main():
    season_list = list(range(1990, 2027))
    nba_scrape(season_list, 'per_game')
    nba_scrape(season_list, 'advanced')
    nba_scrape(season_list, 'per_poss')

    rookie_seasons = [2025, 2026]
    nba_rookies_scrape(rookie_seasons)

    get_logos()


if __name__ == '__main__':
    main()