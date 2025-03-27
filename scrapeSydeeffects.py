
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import os

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    raise ValueError("BASE_URL environment variable is not set.")


def scrape_side_effects(medicine_name):
    formatted_name = medicine_name.lower().replace(" ", "-")
    url = f"{BASE_URL}/sfx/{formatted_name}-side-effects.html"
    
    headers = {"User": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    print(f"\nFetching data for: {medicine_name} -> {url}")  # Debug log
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {medicine_name}, status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the starting point: <h2 id="professional-info">For healthcare professionals</h2>
    professional_info = soup.find("h2", id="professional-info")
    if not professional_info:
        print(f"No professional side effects section found for {medicine_name}, skipping...")
        return ""
    
    side_effects_dict = {}

    # Iterate through elements after professional_info until the next h2 appears
    next_element = professional_info.find_next_sibling()
    while next_element and next_element.name != "h2":  # Stop at next <h2>
        if next_element.name == "h3":  # Side effect category
            category = next_element.text.strip()
            print(f"Processing category: {category}")  # Debug log
            
            # Find the first <ul> after this <h3>
            ul = next_element.find_next_sibling("ul")
            if ul:
                side_effects_list = []
                for li in ul.find_all("li"):
                    strong = li.find("strong")  # Find the <strong> (e.g., "Common", "Rare")
                    if strong:
                        effect_type = strong.text.strip()  # e.g., "Common", "Rare", etc.
                        symptoms_text = li.get_text(separator=" ").replace(effect_type, "").strip()  # Extract text without category
                        
                        # Store results formatted as "Common (x% to y%): symptoms"
                        side_effects_list.append(f"{effect_type}: {symptoms_text}")
                        print(f"Extracted: {category} -> {effect_type}: {symptoms_text}")  # Debug log

                if side_effects_list:
                    side_effects_dict[category] = " | ".join(side_effects_list)

        next_element = next_element.find_next_sibling()  # Move to the next element

    print(f"Side effects dict for {medicine_name}: {side_effects_dict}")  # Debug log
    
    side_effects_list = []
    for category, effects in side_effects_dict.items():
        side_effects_list.append(f"{category}: {effects}")
    
    final_result = " || ".join(side_effects_list)
    print(f"Final side effects for {medicine_name}: {final_result}")  # Debug log
    
    return final_result

def read_medicine_names(file_path):
    medicines_by_letter = {}
    current_letter = None
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("### Medicines starting with "):
                current_letter = line.split("### Medicines starting with ")[1][0]
                medicines_by_letter[current_letter] = []
            elif current_letter and line:
                medicines_by_letter[current_letter].append(line)
    
    return medicines_by_letter

def main():
    input_file = "medicines_name.txt"
    medicines_by_letter = read_medicine_names(input_file)
    
    for letter, medicines in medicines_by_letter.items():
        scraped_data = []
        
        for medicine in medicines:
            side_effects = scrape_side_effects(medicine)
            if side_effects:
                scraped_data.append([medicine, side_effects])
            
            time.sleep(5)  # Pause for 5 seconds to prevent IP blocking
        
        if scraped_data:
            output_file = f"medicine_side_effects_{letter}.csv"
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Medicine", "SideEffects"])
                writer.writerows(scraped_data)
            
            print(f"Scraping complete for letter {letter}. Data saved to {output_file}")

if __name__ == "__main__":
    main()
