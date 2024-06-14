"""
ascension_scraper
================

A Python module to scrape achievement names from `db.ascension.gg` with multi-threading.

This module provides a multi-threaded scraper to retrieve achievement names from `db.ascension.gg` and save them to a CSV file.

Functions
---------

* `get_achievement_name(achievement_id)`: Get the achievement name from `db.ascension.gg`.
* `worker(task_queue, results)`: Worker thread function to retrieve achievement names.
* `scrape_and_save_achievements(start_id, end_id)`: Scrape achievement names from `db.ascension.gg` and save to CSV.
"""
import threading
import time
import csv
import queue
import pandas as pd
from bs4 import BeautifulSoup
import requests

achievement_results: queue.Queue = queue.Queue()
achievement_queue: queue.Queue = queue.Queue()
csv_lock: threading.Lock = threading.Lock()

class SaverThread(threading.Thread):
    """
    A thread to save the achievements to a CSV file.
    """

    def __init__(self, results_queue: queue.Queue, filename: str, save_every: int = 30):
        super().__init__()
        self.results_queue = results_queue
        self.filename = filename
        self.save_every = save_every
        self.daemon = True

    def run(self):
        while True:
            time.sleep(self.save_every)
            self.save_achievements_to_csv()

    def save_achievements_to_csv(self):
        with csv_lock:
            achievements = []
            while not self.results_queue.empty():
                achievements.append(self.results_queue.get())
            if achievements:
                with open(self.filename, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(achievements)

saver_thread = SaverThread(achievement_results, 'scraped_achievements.csv', save_every=15)
saver_thread.start()

def get_achievement_name(achievement_id: int) -> str:
    """
    Get the achievement name from `db.ascension.gg`.

    Args:
        achievement_id (int): The ID of the achievement.

    Returns:
        str: Name of the achievement, "achievement does not exist" if ID invalid, or "maintenance".
    """
    base_url = "https://db.ascension.gg/?achievement="
    url = f"{base_url}{achievement_id}"
    response = requests.get(url, timeout=30)
    time.sleep(1)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('h1')
        if title_element:
            title_text = title_element.text.strip()
            if f"Achievement #{achievement_id}" in title_text:
                return "Achievement ID not found in database"
            else:
                return title_text
        return None
    elif response.status_code == 503:
        soup = BeautifulSoup(response.text, 'html.parser')
        maintenance_message = soup.find('h1')
        if maintenance_message and "Ascension DB under maintenance" in maintenance_message.text:
            print("Maintenance detected. Waiting for 30 minutes before retrying...")
            return "maintenance"
        time.sleep(1800)  # wait for 30 minutes
    else:
        print(f"Failed to get achievement #{achievement_id}: Status code {response.status_code}")
        return None

def worker(task_queue: queue.Queue, results: queue.Queue):
    """
    Worker thread function to retrieve achievement names.

    Args:
        task_queue (queue.Queue): The queue of achievement IDs to process.
        results (queue.Queue): The queue to store the results.
    """
    while True:
        try:
            achievement_id = task_queue.get()
            if achievement_id is None:
                break
            name = get_achievement_name(achievement_id)
            if name == "maintenance":
                task_queue.put(achievement_id)  # retry the request later
            elif name:
                print(f"Found achievement: ID = {achievement_id}, Name = {name}")
                results.put((achievement_id, name))
            task_queue.task_done()
        except queue.Empty:
            print("Queue is empty")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error processing queue: {e}")
            break

def scrape_and_save_achievements(start_id: int, end_id: int):
    """
    Scrape achievement names from `db.ascension.gg` and save to a CSV file.

    Args:
        start_id (int): The starting achievement ID.
        end_id (int): The ending achievement ID.
    """
    threads = []
    for _ in range(4):
        t = threading.Thread(target=worker, args=(achievement_queue, achievement_results))
        t.start()
        threads.append(t)

    for achievement_id in range(start_id, end_id + 1):
        achievement_queue.put(achievement_id)

    achievement_queue.join()

    for _ in range(4):
        achievement_queue.put(None)
    for t in threads:
        t.join()

    achievements = []
    while not achievement_results.empty():
        achievements.append(achievement_results.get())

    achievements.sort(key=lambda x: x[0])

    df = pd.DataFrame(achievements, columns=['ID', 'Name'])
    try:
        df.to_csv('scraped_achievements.csv', index=False)
        print("Achievements saved to scraped_achievements.csv")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permissions error: {e}")
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV: {e}")
    except IOError as e:
        print(f"Error writing CSV: {e}")
    else:
        print(f"No achievement found for ID = {achievement_id}")

START_ID = 1
END_ID = 400000

scrape_and_save_achievements(START_ID, END_ID)
