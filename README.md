# Automated Niche Content Site Generator: "On This Day in Tech History"

## 1. Goal

To create a simple website that automatically updates *every day* with historical technology events corresponding to that date. The website is designed to generate passive income through online advertising networks (like Google AdSense) with minimal ongoing maintenance after the initial setup.

## 2. Core Concept

- A Python script (`main.py`) runs automatically once per day.
- It fetches data about historical events for the current date from a reliable source (currently Wikipedia's "On This Day" pages).
- It filters this data to find tech-related events using keywords.
- It generates a static HTML web page for that day's content, using a basic template and CSS (`style.css`).
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
- **Stylesheet (`style.css`):** Basic CSS for page appearance, located in project root.
  - *Status: Implemented*
- **Output Storage:** Daily HTML files (`YYYY-MM-DD.html`) and `index.html` are saved directly in the project root.
  - *Status: Implemented*
- **Scheduler (`main.py` - `apscheduler`):** Schedules the script to run daily (currently set for 1 AM UTC). 
  - *Status: Implemented in script*
- **Web Hosting:** GitHub Pages using custom domain `dailytechhistory.com`. Configured to serve from repository root (`/`).
  - *Status: Implemented*
- **Monetization:** Google AdSense. Verification code added to `index.html` and daily template. Site ownership verified. Site submitted for review.
  - *Status: Pending AdSense Review*
- **Deployment Automation:** Git commands (`add`, `commit`, `push`) integrated into `main.py` to push generated files and structural changes from the project root to GitHub repository.
  - *Status: Implemented*
- **Execution Environment:** Currently relies on `main.py` running continuously (e.g., in VS Code terminal). Long-term solution requires system scheduling (Task Scheduler/cron).
  - *Status: Temporary solution active; Robust solution pending User Setup*

## 4. Workflow (Once Fully Set Up)

1.  **Daily @ ~1 AM UTC:** The scheduled task triggers `python main.py`.
2.  `fetch_data()` gets today's Wikipedia page.
3.  `fetch_data()` extracts tech events based on keywords.
4.  `generate_html()` creates the HTML content, embedding ad placeholders.
5.  `save_html()` writes `YYYY-MM-DD.html` to the project root directory.
6.  Deployment logic runs `git add .`, `git commit -m "Update content..."`, `git push` to update the GitHub repository.
7.  The live website is updated with the latest day's content.
8.  Visitors arrive (hopefully via search engines over time), view pages, see ads, potentially generating revenue.

## 5. Assessment of Current State

- The core engine for fetching data, generating daily HTML pages (including AdSense code), and deploying them automatically to GitHub Pages via the custom domain `dailytechhistory.com` is functional.
- Site ownership is verified with AdSense, and the site is under review.
- Basic `index.html` created for verification and as a landing page.

## 6. Next Steps

### Immediate Priorities
1.  **Await AdSense Review:** Monitor email for AdSense approval/rejection/feedback.
2.  **Set Up Reliable Scheduling:** Configure Windows Task Scheduler (or preferred method) to run `python main.py` daily in the `content_generator` directory. This is crucial for unattended operation.
3.  **(Optional) Add `ads.txt`:** Once AdSense provides the details (likely post-approval), create and deploy the `ads.txt` file.

### Phase 2: User Experience Improvements (Addressing Feedback)
1.  **Navigation - Archive Page:**
    *   Create `archive.html`.
    *   Modify `main.py` to read existing links, add the new daily link, sort, and rewrite `archive.html` during the daily job.
    *   Add links to `archive.html` from `index.html` and the daily page template in `generate_html`.
2.  **Visual Styling:**
    *   Enhance `style.css` with improved layout, fonts (e.g., web-safe or Google Fonts), color scheme, and spacing.
    *   Consider adding a simple logo or refining the header/footer.
3.  **(Optional) Content Enhancements:**
    *   Modify `fetch_data` and `generate_html` to include source links for events.
    *   Review/expand `tech_keywords` list.