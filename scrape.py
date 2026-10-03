from bs4 import BeautifulSoup
import requests
import csv

ENDPOINT_URL = "https://www.baseball-reference.com/teams/BOS/2026-schedule-scores.shtml"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest", 
    "Referer": "https://www.baseball-reference.com/teams/BOS/2026-schedule-scores.shtml"
}

response = requests.get(ENDPOINT_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
headers_row = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

rows_data = []
for tr in table.find("tbody").find_all("tr"):
    if "thead" in tr.get("class", []):
        continue
    cells = tr.find_all(["td", "th"])
    # Get full name of winning_pitcher, losing_pitcher, and saving_pitcher via 'title="' attribute in <a> tag if available
    for c in cells:
        # Headers "Win", "Loss", "Save" contain pitcher names with full names in the 'title' attribute of the <a> tag
        if c.find("a") and c.find("a").has_attr("title"):
            c.string = c.find("a")["title"]
            #Append the full name to the corresponding cell in rows_data
    row_data = [c.get_text(strip=True) for c in cells]
    rows_data.append(row_data)
            
with open("red_sox_2026_schedule.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers_row)
    writer.writerows(rows_data)

print(f"Saved {len(rows_data)} games")
