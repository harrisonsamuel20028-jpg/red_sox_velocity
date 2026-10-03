import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from pybaseball import playerid_lookup, statcast_pitcher
import unicodedata
from matplotlib import pyplot as plt


#Create visualizations for Average Velocity for the outcome of the games from the csv data.
winning_pitchers_df = pd.read_csv("winning_pitchers.csv")
losing_pitchers_df = pd.read_csv("losing_pitchers.csv")


# Winning Starting Pitchers Average Fastball Velocity
plt.figure(figsize=(10, 6))
plt.hist(winning_pitchers_df['Winning SP Avg FB Velocity'].dropna(), bins=20, alpha=0.7, color='blue')
plt.title('Winning Starting Pitchers Average Fastball Velocity')
plt.xlabel('Velocity (mph)')
plt.ylabel('Frequency')
plt.savefig('winning_sp_avg_fb_velocity.png')
plt.close()

# Losing Starting Pitchers Average Fastball Velocity
plt.figure(figsize=(10, 6))
plt.hist(losing_pitchers_df['Losing SP Avg FB Velocity'].dropna(), bins=20, alpha=0.7, color='red')
plt.title('Losing Starting Pitchers Average Fastball Velocity')
plt.xlabel('Velocity (mph)')
plt.ylabel('Frequency')
plt.savefig('losing_sp_avg_fb_velocity.png')
plt.close()


# Losing Closing Pitchers Average Fastball Velocity
plt.figure(figsize=(10, 6))
plt.hist(losing_pitchers_df['Losing CP Avg FB Velocity'].dropna(), bins=20, alpha=0.7, color='red')
plt.title('Losing Closing Pitchers Average Fastball Velocity')
plt.xlabel('Velocity (mph)')
plt.ylabel('Frequency')
plt.savefig('losing_cp_avg_fb_velocity.png')
plt.close()
