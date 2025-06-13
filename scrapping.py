import requests
from bs4 import BeautifulSoup
import time

def scrape_website(url):
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Get the webpage content
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Create BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    url = "https://www.timesnownews.com/world/asia/myanmar-thailand-earthquake-today-bangkok-trembles-as-quake-leaves-1-dead-over-40-trapped-under-debris-article-119643091"
    text_content = scrape_website(url)
    
    if text_content:
        # Save to file
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(text_content)
        print("Content has been saved to 'scraped_content.txt'")
