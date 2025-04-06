# Main script for the automated content generator
import os
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Basic Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
OUTPUT_DIR = "output_html"
# Example: Define a source URL or API endpoint
# SOURCE_URL = os.getenv("SOURCE_URL") 

# --- Functions ---

def fetch_data():
    """Fetches 'On This Day in Tech History' data from Wikipedia."""
    logging.info("Fetching 'On This Day in Tech History' data...")
    now = datetime.now()
    month_day = now.strftime("%B_%d") # Format like January_01
    year = now.strftime("%Y")
    wiki_url = f"https://en.wikipedia.org/wiki/{month_day}"
    headers = {'User-Agent': 'AutomatedContentGenerator/1.0 (https://example.com/bot; contact@example.com)'} # Be a good citizen

    try:
        response = requests.get(wiki_url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the H2 heading directly by its ID
        events_h2 = soup.find('h2', {'id': 'Events'})
        if not events_h2:
            # Fallback: Find H2 containing a span with id 'Events' (less common structure)
            events_heading_span = soup.find('span', {'id': 'Events'})
            if events_heading_span:
                 events_h2 = events_heading_span.find_parent('h2')
            
        if not events_h2:
             logging.warning(f"Could not find H2 heading with ID 'Events' or containing span with ID 'Events' on {wiki_url}")
             return None
        
        logging.info(f"Found 'Events' heading: <{events_h2.name} id='{events_h2.get('id')}'>")

        # Find the next <ul> tag after the H2 heading, searching siblings and descendants
        events_list = events_h2.find_next('ul')

        if not events_list:
            logging.warning(f"Could not find any 'ul' tag following the 'Events' H2 on {wiki_url}")
            return None

        tech_events = []
        tech_keywords = ["computer", "internet", "software", "semiconductor", "microprocessor", "apple", "microsoft", "google", "ibm", "intel", "nasa", "space", "digital", "network", "web", "programming", "code", "algorithm", "robot", "phone", "mobile"]

        list_items = events_list.find_all('li', recursive=False) # Get only direct children li
        for item in list_items:
            text = item.get_text().lower()
            # Check if any tech keyword is in the list item text
            if any(keyword in text for keyword in tech_keywords):
                 # Basic cleanup: remove citation needed tags etc.
                for tag in item.find_all(['sup', 'span'], {'class': ['reference', 'noprint']}):
                    tag.decompose()
                tech_events.append(item.get_text(strip=True))

        if not tech_events:
            logging.info(f"No specific tech events found for {month_day} on Wikipedia.")
            body_content = "No specific tech events found for today."
        else:
            # Format as an HTML list
            body_content = "<ul>\n" + "\n".join(f"  <li>{event}</li>" for event in tech_events) + "\n</ul>"

        data = {
            "title": f"On This Day in Tech History: {now.strftime('%B %d, %Y')}",
            "body": body_content,
            "date": now.strftime("%Y-%m-%d")
        }
        logging.info(f"Successfully fetched and processed tech events for {month_day}.")
        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Wikipedia page {wiki_url}: {e}")
        return None
    except Exception as e:
        logging.exception(f"An unexpected error occurred during data fetching for {month_day}: {e}")
        return None

def generate_html(data):
    """Generates HTML content from the fetched data."""
    logging.info("Generating HTML...")
    title = data.get('title', 'Generated Content')
    body = data.get('body', '<p>No content available for today.</p>')
    date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Basic HTML structure with placeholders
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Tech history events for {date_str}. Discover what happened in technology on this day.">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
    <!--
        Placeholder for Google AdSense Auto Ads script
        (Get this from your AdSense account)
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_PUB_ID"
                crossorigin="anonymous"></script>
    -->
    <!--
        Placeholder for Analytics (e.g., Google Analytics)
        (Get this from your Analytics account)
    -->
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p>Date: {date_str}</p>
        <!-- Optional: Link back to an index page -->
        <!-- <p><a href="index.html">Back to Archive</a></p> -->
    </header>

    <main>
        <!-- Placeholder for Ad Unit 1 (Optional) -->
        <!--
        <div class="ad-placeholder">
            Ad Unit 1 (e.g., Display Ad) - Place AdSense code here
        </div>
        -->

        <h2>Events:</h2>
        {body}

        <!-- Placeholder for Ad Unit 2 (Optional) -->
        <!--
        <div class="ad-placeholder">
            Ad Unit 2 (e.g., Display Ad) - Place AdSense code here
        </div>
        -->
    </main>

    <footer>
        <p>Content sourced from Wikipedia under CC BY-SA license. Generated automatically.</p>
        <!-- Optional: Link to specific Wikipedia page? -->
        <p><a href="https://github.com/your-repo-link-here" target="_blank" rel="noopener noreferrer">Project Source (Optional)</a></p>
    </footer>

</body>
</html>
"""
    logging.info("HTML generated successfully.")
    return html_content

def save_html(html_content, filename):
    """Saves the generated HTML to a file."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logging.info(f"Created output directory: {OUTPUT_DIR}")
        
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"HTML saved successfully to {filepath}")
    except IOError as e:
        logging.error(f"Error saving HTML to {filepath}: {e}")

def job():
    """The main job executed by the scheduler."""
    logging.info("Starting content generation job...")
    try:
        data = fetch_data()
        if data:
            html = generate_html(data)
            # Use date for filename to avoid overwriting and create archives
            filename = f"{data.get('date', datetime.now().strftime('%Y-%m-%d'))}.html" 
            save_html(html, filename)
            # TODO: Add logic here to potentially update an index.html file
            # TODO: Add logic here for deployment (e.g., git commit/push, sync command)
        else:
            logging.warning("No data fetched, skipping HTML generation.")
    except Exception as e:
        logging.exception("An error occurred during the job execution.")
    logging.info("Content generation job finished.")

# --- Scheduler Setup ---
scheduler = BlockingScheduler(timezone="UTC") # Use UTC or your preferred timezone

# Schedule the job to run daily at a specific time (e.g., 01:00 UTC)
scheduler.add_job(job, 'cron', hour=1, minute=0) 

# --- Main Execution ---
if __name__ == "__main__":
    logging.info("Starting the scheduler...")
    # Optional: Run the job once immediately on startup before scheduling
    # logging.info("Running initial job before starting scheduler...")
    # job()
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")