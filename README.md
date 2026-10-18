# Web-Scraper-for-jobs
A Python scraping toolkit designed to monitor, retrieve, classify, and export Forward Deployed Engineer (FDE / FDSE), Forward Deployment AI Engineer, and Solutions Engineering job openings in India, specifically filtered for freshers and early-career candidates (0–2 years experience).
Key Features

1. **Multi-Source Scraping**:
   - **LinkedIn Public Jobs (Guest Search)**: Direct real-time aggregation across Indian tech hubs (Bengaluru, Hyderabad, Pune, Mumbai, Delhi NCR, Noida, Chennai, etc.) without requiring authentication or cookies.
   - **Direct ATS Career Portals (Greenhouse & Lever)**: Queries career endpoints of top tech companies known for Forward Deployment (e.g. *DevRev, HighRadius, TrueFoundry, Prodigal, Scale AI, Palantir*).
   - **Remote Job Boards**: Queries public APIs (Jobicy) for global/remote deployment roles open to candidates in India.

2. **Intelligent Fresher & Experience Classification**:
   - **Senior Role Elimination**: Detects and filters out senior, lead, principal, staff, architect, and managerial designations (`5+ years`, `7+ years`).
   - **Fresher Verification**: Matches entry-level indicators (`0-1 yr`, `0-2 yrs`, `fresher`, `intern`, `graduate`, `campus hire`, `associate`).
   - **Role Relevance Filtering**: Ensures only genuine Forward Deployment, Solutions Engineering, and AI Deployment openings are retained.

3. **Anti-Bot & Rate-Limit Resilience**:
   - Polite randomized jitter delays (1.2s – 2.5s).
   - User-Agent pool rotation across modern Chrome, Firefox, Safari, and Edge desktop agents.
   - Automatic exponential backoff and retry when HTTP `429 Too Many Requests` is encountered.

4. **Multi-Format Export**:
   - **`fde_jobs_latest.csv`**: Clean spreadsheet format ready for Google Sheets or Excel.
   - **`fde_jobs_latest.json`**: Complete structured JSON with all attributes and raw snippets.
   - **`fde_jobs_latest.md`**: Beautiful Markdown digest with company breakdown, location stats, and one-click apply links.
