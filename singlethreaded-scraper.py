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

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_element = soup.find('h1')  # Look for any <h1> tag
            if title_element:
                achievement_name = title_element.text.strip()
                return achievement_name
        elif response.status_code == 503:
            soup = BeautifulSoup(response.text, 'html.parser')
            maintenance_message = soup.find('h1')
            if maintenance_message and "Ascension DB under maintenance" in maintenance_message.text:
                print("Maintenance detected. Waiting for 30 minutes before retrying...")
                return "maintenance"
        else:
            print(f"Failed to get achievement {achievement_id}: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception for achievement {achievement_id}: {e}")

    return None

def scrape_and_save_achievements(start_id, end_id):
    """
    Scrape achievement names within a given range and save them to a CSV file.

    Parameters:
    - start_id (int): The starting ID of the achievement range to scrape.
    - end_id (int): The ending ID of the achievement range to scrape.
    """
    # Dictionary to store achievement IDs and names
    achievements = {}

    for achievement_id in range(start_id, end_id + 1):
        name = get_achievement_name(achievement_id)
        if name == "maintenance":
            time.sleep(15 * 60)
            continue  # Retry the same achievement_id after the wait
        elif name:
            achievements[achievement_id] = name
            print(f"Found achievement: ID = {achievement_id}, Name = {name}")
        else:
            print(f"No achievement found for ID = {achievement_id}")

        # Convert to DataFrame for easy manipulation and saving
        df = pd.DataFrame(list(achievements.items()), columns=['ID', 'Name'])

        # Save to a CSV file
        try:
            df.to_csv('achievements.csv', index=False)
            print("Achievements saved to achievements.csv")
        except FileNotFoundError as e:
            print(f"File not found error: {e}")
        except PermissionError as e:
            print(f"Permission error: {e}")
        except IOError as e:
            print(f"IO error: {e}")

        # Sleep to avoid overloading the server
        time.sleep(1)

# Specify the range of achievement IDs to scrape
START_ID = 1
END_ID = 400000

# Call the function to scrape and save achievements
scrape_and_save_achievements(START_ID, END_ID)
