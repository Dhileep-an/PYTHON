# project4.py
# Web Scraper for Headlines & Quotes

import json
import time
import requests
from bs4 import BeautifulSoup
from collections import Counter

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "InternCircle-learning-project (student scraper)"}

def scrape_quotes():
    '''Scrapes quotes, authors, and tags across paginated pages safely.'''
    url = BASE_URL + "/"
    quotes_data = []
    
    print(f"Starting scrape from {BASE_URL}...")
    
    while url:
        print(f"Fetching {url}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            break
            
        soup = BeautifulSoup(r.text, "html.parser")
        
        for q in soup.select("div.quote"):
            text = q.select_one("span.text").get_text(strip=True) if q.select_one("span.text") else ""
            author = q.select_one("small.author").get_text(strip=True) if q.select_one("small.author") else ""
            tags = [t.get_text(strip=True) for t in q.select("a.tag")]
            
            quotes_data.append({
                "text": text,
                "author": author,
                "tags": tags
            })
            
        next_btn = soup.select_one("li.next a")
        url = BASE_URL + next_btn["href"] if next_btn else None
        
        # Polite delay
        if url:
            time.sleep(1)
            
    return quotes_data

def summarize_data(quotes):
    '''Calculates most quoted author and most common tag.'''
    if not quotes:
        return None, None
        
    authors = [q['author'] for q in quotes if q['author']]
    all_tags = [tag for q in quotes for tag in q['tags']]
    
    most_common_author = Counter(authors).most_common(1)
    most_common_tag = Counter(all_tags).most_common(1)
    
    top_author = most_common_author[0] if most_common_author else ("None", 0)
    top_tag = most_common_tag[0] if most_common_tag else ("None", 0)
    
    return top_author, top_tag

def save_data(quotes):
    '''Saves scraped data to JSON and TXT formats.'''
    # Save to JSON
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
        
    # Save to standard text file
    with open("quotes.txt", "w", encoding="utf-8") as f:
        for i, q in enumerate(quotes, 1):
            f.write(f"Quote {i}\n")
            f.write(f"Text: {q['text']}\n")
            f.write(f"Author: {q['author']}\n")
            f.write(f"Tags: {', '.join(q['tags'])}\n")
            f.write("-" * 40 + "\n")
            
def main():
    quotes = scrape_quotes()
    if not quotes:
        print("No quotes found.")
        return
        
    save_data(quotes)
    print(f"\nSuccessfully saved {len(quotes)} quotes to quotes.json and quotes.txt")
    
    top_author, top_tag = summarize_data(quotes)
    print("\n--- Scraping Summary ---")
    print(f"Total Quotes: {len(quotes)}")
    print(f"Most Quoted Author: {top_author[0]} ({top_author[1]} quotes)")
    print(f"Most Common Tag: {top_tag[0]} ({top_tag[1]} uses)")

if __name__ == '__main__':
    main()
