from pybaseball import playerid_lookup, statcast_pitcher
import pandas as pd

SEASON_START = '2026-03-25'
SEASON_END = '2026-10-01'

BR_TO_PYBASEBALL_TEAM = {
    "BOS": "Red Sox",    "NYY": "Yankees",     "TBR": "Rays",
    "TOR": "Blue Jays",  "BAL": "Orioles",     "CLE": "Guardians",
    "CHW": "White Sox",  "DET": "Tigers",      "KCR": "Royals",
    "MIN": "Twins",      "HOU": "Astros",      "LAA": "Angels",
    "OAK": "Athletics",  "SEA": "Mariners",    "TEX": "Rangers",
    "ATL": "Braves",     "NYM": "Mets",        "PHI": "Phillies",
    "MIA": "Marlins",    "WSN": "Nationals",   "CHC": "Cubs",
    "CIN": "Reds",       "MIL": "Brewers",     "PIT": "Pirates",
    "STL": "Cardinals",  "ARI": "Diamondbacks","COL": "Rockies",
    "LAD": "Dodgers",    "SDP": "Padres",      "SFG": "Giants",
}

def fix_name_encoding(name):
    if not isinstance(name, str):
        return name
    
    name = name.replace('\xa0', ' ')
    
    try:
        name = name.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass  
    
    return name.strip()


df = pd.read_csv("red_sox_2026_schedule.csv")

#Get list of all starting pitchers and closing pitchers if applicable from our csv
losses_df = df[df["W/L"] == "L"].copy()
losing_starting_pitchers   = losses_df["Win"].tolist()
losing_closing_pitchers    = losses_df["Save"].tolist()
losing_opp                 = losses_df["Opp"].tolist()   

wins_df = df[df["W/L"] == "W"].copy()
winning_starting_pitchers  = wins_df["Loss"].tolist()
winning_tm                 = wins_df["Tm"].tolist()      


_velocity_cache = {} 
# Use pybaseball to fetch the average fastball velocity for each pitcher
def get_avg_fastball_velocity(pitcher_name):
    """Return average four-seam (FF) velocity for a pitcher, falling back to
    sinker (SI) if no four-seamers were thrown. Returns None if unavailable."""

    if not isinstance(pitcher_name, str) or pd.isna(pitcher_name):
        return None

    start = SEASON_START
    end = SEASON_END

    key = (pitcher_name.strip(), start, end)
    if key in _velocity_cache:
        return _velocity_cache[key]

    result = None
    parts = pitcher_name.strip().split()
    if len(parts) >= 2:
        try:
            player_info = playerid_lookup(parts[-1], parts[0])
            if not player_info.empty:
                player_id = int(player_info.iloc[0]['key_mlbam'])
                data = statcast_pitcher(start, end, player_id=player_id)
                if not data.empty:
                    for pitch_type in ('FF', 'SI'):
                        subset = data[data['pitch_type'] == pitch_type]
                        if not subset.empty:
                            result = subset['release_speed'].mean()
                            break
        except Exception as e:
            print(f"Lookup failed for {pitcher_name}: {e}")
            return None  # don't cache transient failures

    _velocity_cache[key] = result
    return result

# Create new DataFrame with Wins and Losses starting and closing pitchers and turn it to csv
winning_pitchers_df = pd.DataFrame({
    "Winning Starting Pitchers": pd.Series(winning_starting_pitchers),
    #"Winning Closing Pitchers":  pd.Series(winning_closing_pitchers),
    "Winning Tm":                pd.Series(winning_tm)
})

losing_pitchers_df = pd.DataFrame({
    "Losing Starting Pitchers":  pd.Series(losing_starting_pitchers),
    "Losing Closing Pitchers":   pd.Series(losing_closing_pitchers),
    "Losing Opp":                pd.Series(losing_opp)
})

for col in ["Winning Starting Pitchers"]:
    winning_pitchers_df[col] = winning_pitchers_df[col].apply(fix_name_encoding)
for col in ["Losing Starting Pitchers", "Losing Closing Pitchers"]:
    losing_pitchers_df[col] = losing_pitchers_df[col].apply(fix_name_encoding)

winning_pitchers_df['Winning Starting Pitchers Full'] = winning_pitchers_df['Winning Starting Pitchers']
#winning_pitchers_df['Winning Closing Pitchers Full'] = winning_pitchers_df['Winning Closing Pitchers']
losing_pitchers_df['Losing Starting Pitchers Full'] = losing_pitchers_df['Losing Starting Pitchers']
losing_pitchers_df['Losing Closing Pitchers Full'] = losing_pitchers_df['Losing Closing Pitchers']

winning_pitchers_df['Winning SP Avg FB Velocity'] = winning_pitchers_df['Winning Starting Pitchers Full'].apply(get_avg_fastball_velocity)
#winning_pitchers_df['Winning CP Avg FB Velocity'] = winning_pitchers_df['Winning Closing Pitchers Full'].apply(get_avg_fastball_velocity)
losing_pitchers_df['Losing SP Avg FB Velocity']  = losing_pitchers_df['Losing Starting Pitchers Full'].apply(get_avg_fastball_velocity)
losing_pitchers_df['Losing CP Avg FB Velocity']  = losing_pitchers_df['Losing Closing Pitchers Full'].apply(get_avg_fastball_velocity)


# Add the updated DataFrames with velocity data to the CSV files
winning_pitchers_df.to_csv("winning_pitchers.csv", index=False)
losing_pitchers_df.to_csv("losing_pitchers.csv", index=False)