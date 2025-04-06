# Automated Niche Content Site Generator: "On This Day in Tech History"

## 1. Goal

To create a simple website that automatically updates *every day* with historical technology events corresponding to that date. The website is designed to generate passive income through online advertising networks (like Google AdSense) with minimal ongoing maintenance after the initial setup.

## 2. Core Concept

- A Python script (`main.py`) runs automatically once per day.
- It fetches data about historical events for the current date from a reliable source (currently Wikipedia's "On This Day" pages).
- It filters this data to find tech-related events using keywords.
- It generates a static HTML web page for that day's content, using a basic template and CSS (`output_html/style.css`).
- These generated pages are automatically published/deployed to a live web host.
- Advertising code (e.g., from Google AdSense) is embedded in the pages via the template.
- Over time, search engines (like Google) index these pages, attracting visitors interested in tech history (organic traffic).
- Ad views and clicks from these visitors generate revenue passively.

## 3. Components & Status

- **Data Source:** Wikipedia "On This Day" pages (e.g., `https://en.wikipedia.org/wiki/April_07`). 
  - *Status: Implemented*
- **Content Scraper/Processor (`main.py` - `fetch_data`):** Python code using `requests` and `BeautifulSoup` to get and parse Wikipedia content, filtering for tech keywords. 
  - *Status: Implemented & Tested*
- **HTML Generator (`main.py` - `generate_html`):** Python code to create the structure of the daily web page using the fetched data. Includes placeholders for ads. 
  - *Status: Implemented & Tested*
- **Stylesheet (`output_html/style.css`):** Basic CSS for page appearance. 
  - *Status: Implemented*
- **Output Storage (`output_html` folder):** Where the daily HTML files are saved locally. 
  - *Status: Implemented*
- **Scheduler (`main.py` - `apscheduler`):** Schedules the script to run daily (currently set for 1 AM UTC). 
  - *Status: Implemented in script*
- **Web Hosting:** A platform to make the generated HTML files accessible online (e.g., GitHub Pages, Netlify, Vercel). 
  - *Status: Not Yet Implemented - Requires User Setup*
- **Monetization:** An advertising network account (e.g., Google AdSense) to provide ad code. 
  - *Status: Not Yet Implemented - Requires User Setup & Approval*
- **Deployment Automation:** A mechanism to automatically transfer the generated files from the local `output_html` folder to the live web host daily. 
  - *Status: Not Yet Implemented - Can be added to `main.py` or handled by hosting platform*
- **Execution Environment:** A reliable way to run the `main.py` script daily (e.g., local machine with Task Scheduler/cron, cloud service like PythonAnywhere). 
  - *Status: Not Yet Implemented - Requires User Setup*

## 4. Workflow (Once Fully Set Up)

1.  **Daily @ ~1 AM UTC:** The scheduled task triggers `python main.py`.
2.  `fetch_data()` gets today's Wikipedia page.
3.  `fetch_data()` extracts tech events based on keywords.
4.  `generate_html()` creates the HTML content, embedding ad placeholders.
5.  `save_html()` writes `YYYY-MM-DD.html` to the local `output_html` folder.
6.  *(Future Step)* Deployment logic (e.g., `git add .`, `git commit -m "Update content for YYYY-MM-DD"`, `git push`) uploads the new/updated files in `output_html` to the live web host (e.g., GitHub repository configured for GitHub Pages).
7.  The live website is updated with the latest day's content.
8.  Visitors arrive (hopefully via search engines over time), view pages, see ads, potentially generating revenue.

## 5. Assessment of Current State

- The core engine for fetching data and generating the daily HTML pages is complete and functional.
- The project is well-structured.
- The foundation is solid for adding the hosting, monetization, and automation layers.

## 6. Next Steps (Required for Passive Income)

1.  **Choose & Set Up Hosting:** Select a static hosting provider (GitHub Pages is recommended for a free start). Create a GitHub repository, push the current project code, and configure GitHub Pages in the repository settings (likely serving from the `/output_html` folder or root on the `main` branch).
2.  **Apply for Monetization:** Sign up for Google AdSense (or alternative). Submit your live site URL (from step 1) for review. This may take days or weeks.
3.  **Integrate Ad Code:** Once approved by AdSense, copy the provided JavaScript snippets. Edit `main.py` and paste these snippets into the placeholder comments within the `generate_html` function's template string.
4.  **Implement Deployment:** Add Git commands (or other deployment commands specific to your host) to the end of the `job()` function in `main.py` to automatically push changes after saving the HTML file. Ensure Git is configured correctly on the machine running the script (authentication may be needed for pushes).
5.  **Set Up Reliable Scheduling:** Configure your operating system (Task Scheduler on Windows, `cron` on Linux/macOS) or a cloud service (like PythonAnywhere's free tier) to execute the `python main.py` command within the `content_generator` directory once per day at the desired time.