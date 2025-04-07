# Main script for the automated content generator
import subprocess
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
OUTPUT_DIR = "." # Output files to the project root
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
    <!-- Google AdSense Verification/Auto Ads Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1226435955298586"
         crossorigin="anonymous"></script>
    <!-- End Google AdSense Code -->
    <!--
        Placeholder for Analytics (e.g., Google Analytics)
        (Get this from your Analytics account)
    -->
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p>Date: {date_str}</p>
        <p><a href="index.html">Home</a> | <a href="archive.html">Archive</a></p>
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

def update_archive(new_page_filename, page_title):
    """Reads archive.html, adds the new link, sorts, and rewrites the file."""
    logging.info(f"Updating archive with: {new_page_filename}")
    archive_file = "archive.html"
    new_link = f'<li><a href="{new_page_filename}">{page_title}</a></li>'
    links = []
    placeholder_text = "<!-- Links will be automatically added here by the script -->"
    list_start_tag = '<ul id="archive-list">'
    list_end_tag = '</ul>'

    try:
        # Read existing archive content
        if os.path.exists(archive_file):
            with open(archive_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract existing links using BeautifulSoup for robustness
            soup = BeautifulSoup(content, 'html.parser')
            archive_list_ul = soup.find('ul', {'id': 'archive-list'})
            if archive_list_ul:
                existing_links = archive_list_ul.find_all('li')
                # Filter out placeholder if present
                links = [str(li) for li in existing_links if "No entries generated yet." not in li.get_text()]
            else:
                 logging.warning(f"Could not find <ul id='archive-list'> in {archive_file}. Starting fresh.")
                 content = "" # Reset content if list not found

        else:
            logging.warning(f"{archive_file} not found. Creating a new one.")
            # Create basic structure if file doesn't exist
            content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archive - Daily Tech History</title>
    <link rel="stylesheet" href="style.css">
    <!-- Google AdSense Verification/Auto Ads Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1226435955298586"
         crossorigin="anonymous"></script>
    <!-- End Google AdSense Code -->
</head>
<body>
    <header>
        <h1>Archive - Daily Tech History</h1>
        <p>Browse past entries.</p>
        <p><a href="index.html">Back to Home</a></p>
    </header>
    <main>
        <h2>Past Entries</h2>
        {list_start_tag}
            {placeholder_text}
        {list_end_tag}
    </main>
    <footer>
        <p>Powered by Automated Content Generator.</p>
        <p><a href="https://github.com/guppyO/tech-history-daily" target="_blank" rel="noopener noreferrer">Project Source</a></p>
    </footer>
</body>
</html>"""

        # Add the new link if it's not already there
        if new_link not in links:
            links.append(new_link)

        # Sort links based on filename (date) - descending (newest first)
        # Extract date from filename like 'YYYY-MM-DD.html'
        def get_date_from_link(link_str):
            try:
                 href = BeautifulSoup(link_str, 'html.parser').find('a')['href']
                 return href.split('.')[0] # Get 'YYYY-MM-DD'
            except:
                 return "0000-00-00" # Fallback for sorting

        links.sort(key=get_date_from_link, reverse=True)

        # Prepare the new list content
        new_list_content = "\n            ".join(links) if links else f"<li>No entries generated yet.</li>"

        # Replace the old list content (or placeholder) with the new sorted list
        start_index = content.find(list_start_tag)
        end_index = content.find(list_end_tag)

        if start_index != -1 and end_index != -1:
            start_index += len(list_start_tag) # Move index past the start tag
            # Ensure newline and indentation consistency
            new_content = content[:start_index] + f"\n            {new_list_content}\n        " + content[end_index:]
        else:
             logging.error(f"Could not find list tags in {archive_file} template/content. Cannot update.")
             return # Avoid writing if structure is broken

        # Write the updated content back to archive.html
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        logging.info(f"Successfully updated {archive_file}")

    except Exception as e:
        logging.exception(f"An error occurred while updating {archive_file}: {e}")

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
            update_archive(filename, data.get('title', 'Unknown Title')) # Call update_archive
            # --- Automatic Deployment using Git ---
            try:
                logging.info("Attempting to deploy changes via Git...")
                # Stage all changes in the current directory (project root)
                subprocess.run(['git', 'add', '.'], check=True, capture_output=True, text=True, cwd='.') # Run from script's dir (content_generator)

                # Check if there are any changes staged
                # Use --quiet to exit with 1 if changes, 0 if not.
                status_check = subprocess.run(['git', 'diff', '--quiet', '--cached'], cwd='.')
                
                if status_check.returncode != 0: # If exit code is non-zero, there are staged changes
                    commit_message = f"Update content for {data.get('date', 'Unknown Date')}"
                    subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True, text=True, cwd='.')
                    logging.info("Changes committed.")
                    
                    # Push the changes
                    logging.info("Pushing changes to origin main...")
                    push_result = subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True, text=True, cwd='.')
                    logging.info("Changes pushed successfully.")
                    logging.debug(f"Git push output: {push_result.stdout}\n{push_result.stderr}")
                else:
                    logging.info("No changes detected in output_html to commit.")
                    
            except subprocess.CalledProcessError as e:
                logging.error(f"Git command failed: {e}")
                logging.error(f"Command: {' '.join(e.cmd)}")
                logging.error(f"Stderr: {e.stderr}")
                logging.error(f"Stdout: {e.stdout}")
            except FileNotFoundError:
                 logging.error("Git command not found. Ensure Git is installed and in the system's PATH.")
            except Exception as e:
                logging.exception("An unexpected error occurred during Git deployment.")
            # --- End Automatic Deployment ---

            # TODO: Add logic here to potentially update an index.html file
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