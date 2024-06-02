import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get achievement name by ID
def get_achievement_name(achievement_id):
    base_url = "https://db.ascension.gg/?achievement="
    url = f"{base_url}{achievement_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('h1')  # Look for any <h1> tag
        if title_element:
            achievement_name = title_element.text.strip()
            return achievement_name
    else:
        print(f"Failed to retrieve achievement {achievement_id}: Status code {response.status_code}")
    return None

# Specify the range of achievement IDs to scrape
START_ID = 1  # Starting ID
END_ID = 24597  # Ending ID

# Dictionary to store achievement IDs and names
achievements = {}

for achievement_id in range(START_ID, END_ID + 1):
    name = get_achievement_name(achievement_id)
    if name:
        achievements[achievement_id] = name
        print(f"Found achievement: ID = {achievement_id}, Name = {name}")
    else:
        print(f"No achievement found for ID = {achievement_id}")
    # Sleep to avoid overloading the server
    time.sleep(1)

# Convert to DataFrame for easy manipulation and saving
df = pd.DataFrame(list(achievements.items()), columns=['ID', 'Name'])

# Save to a CSV file
try:
    df.to_csv('achievements.csv', index=False)
    print("Achievements saved to achievements.csv")
except Exception as e:
    print(f"Error saving to CSV: {e}")
