# AscensionSiteScraper4Achievements

`Ascension Site Scraper for Achievements` or `A.S.S. 4 Achievements` is a Python script designed to scrape achievement names and IDs from the Ascension database website (db.ascension.gg). It fetches this information and saves it into a CSV file for easy access and manipulation.

## ✨ Features

- **Automated Scraping**: The script automates the process of fetching achievement names and IDs, eliminating the need for manual data collection.
- **Dynamic ID Retrieval**: Utilizes dynamic scraping techniques to fetch achievement IDs from the Ascension website, ensuring accuracy and adaptability to changes in the website structure.
- **Flexible Output**: Data is saved into a CSV file, allowing for easy integration into other tools and analysis platforms.

## 🧑‍💻 Usage

1. **Installation**: Clone the repository or download the script (`scraper.py`) to your local machine.

2. **Dependencies**: Ensure you have Python installed on your system along with the required libraries (`requests`, `beautifulsoup4`, and `pandas`). You can install these dependencies using pip:

   ```
   pip install requests beautifulsoup4 pandas
   ```

3. **Execution**: Run the script in your Python environment. This varies from device to device so i cannot provide instructions at this time. The achievements will be scraped and saved to a CSV file named `achievements.csv` in the directory where the script is executed.

## 🛠️ Configuration

- **Range of IDs**: By default, the script fetches achievement names and IDs for a predefined range (1-35000). You can adjust this range by modifying the `START_ID` and `END_ID` variables in the script.
