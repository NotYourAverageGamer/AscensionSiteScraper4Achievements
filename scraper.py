"""
This script scrapes achievements from the Ascension database and saves them to a CSV file.
"""
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_achievement_name(achievement_id):
    """
    Retrieve the achievement name by its ID from the Ascension database.

    Parameters:
    - achievement_id (int): The ID of the achievement to retrieve.

    Returns:
    - str or None: The name of the achievement if found, otherwise None.
    """
    base_url = "https://db.ascension.gg/?achievement="
    url = f"{base_url}{achievement_id}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('h1')  # Look for any <h1> tag
        if title_element:
            achievement_name = title_element.text.strip()
            return achievement_name
    else:
        print(f"Failed to get achievement {achievement_id}: Status code {response.status_code}")
    return None

def scrape_and_save_achievements(start_id, end_id):
    """
    Scrape achievement names within a given range and save them to a CSV file.

    Parameters:
    - START_ID (int): The starting ID of the achievement range to scrape.
    - END_ID (int): The ending ID of the achievement range to scrape.
    """
    # Dictionary to store achievement IDs and names
    achievements = {}

    for achievement_id in range(start_id, end_id + 1):
        name = get_achievement_name(achievement_id)
        if name:
            achievements[achievement_id] = name
            print(f"Found achievement: ID = {achievement_id}, Name = {name}")
            # Convert to DataFrame for easy manipulation and saving
            df = pd.DataFrame(list(achievements.items()), columns=['ID', 'Name'])

            # Save to a CSV file
            try:
                df.to_csv('achievements.csv', index=False)
                print("Achievement saved to achievements.csv")
            except FileNotFoundError as e:
                print(f"File not found error: {e}")
            except PermissionError as e:
                print(f"Permission error: {e}")
            except IOError as e:
                print(f"IO error: {e}")
        else:
            print(f"No achievement found for ID = {achievement_id}")
        # Sleep to avoid overloading the server
        time.sleep(1)

# Specify the range of achievement IDs to scrape
START_ID = 1
END_ID = 25000

# Call the function to scrape and save achievements
scrape_and_save_achievements(START_ID, END_ID)
