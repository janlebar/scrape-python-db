import requests
from bs4 import BeautifulSoup
import os

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    raise ValueError("BASE_URL environment variable is not set.")


# Letters to scrape (A-Z)
LETTERS = [chr(i) for i in range(ord('a'), ord('z') + 1)]

# Dictionary to store medicines
all_medicines = {}

# Function to scrape medicines from a given letter page
def scrape_medicines(letter):
    url = f"{BASE_URL}alpha/{letter}.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all medicine names
    medicines = []
    ul_list = soup.find_all("ul", class_="ddc-list-column-2")
    
    for ul in ul_list:
        for li in ul.find_all("li"):
            a_tag = li.find("a")
            if a_tag:
                medicines.append(a_tag.text.strip())

    return medicines

# Loop through each letter and scrape data
for letter in LETTERS:
    print(f"Scraping medicines for letter: {letter.upper()} ...")
    medicines = scrape_medicines(letter)
    all_medicines[letter] = medicines

# Save results to a file
with open("medicines_list.txt", "w", encoding="utf-8") as file:
    for letter, medicines in all_medicines.items():
        file.write(f"\n### Medicines starting with {letter.upper()} ###\n")
        for medicine in medicines:
            file.write(medicine + "\n")

print("\nScraping complete! Medicines saved to medicines_list.txt ")
