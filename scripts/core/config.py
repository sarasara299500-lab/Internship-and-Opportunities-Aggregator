"""
Central configuration for the Opportunity Bot.
--------------------------------------------------
All tunable knobs live here so there is a single source of truth. Every value
can be overridden via environment variables (useful for GitHub Actions secrets
and for other users who want to reuse the bot without editing code).
"""

import os

# ============================================================
# USER PROFILE  (the LLM uses this to judge relevance)
# ============================================================
# Override with the USER_PROFILE env var to reuse the bot for someone else.
USER_PROFILE = os.environ.get("USER_PROFILE", """
- B.Tech Computer Science student in India, GRADUATING IN 2028
  (currently entering 5th semester / 3rd year).
- Nationality: Indian. Based in Bhopal, Madhya Pradesh, India. College: LNCT Bhopal.
- Interests: AI/ML, Software Development, Data Structures & Algorithms, Web Development.
- Skills: Python, C++, Java, SQL, HTML, CSS, JavaScript.
- Looking for: Software Engineering / AI-ML / Data internships (Summer 2027 or
  off-cycle / remote), hackathons, coding competitions, tech scholarships,
  and research / technology fellowships.

- ELIGIBILITY RULES (very important — used to reject irrelevant listings):
  * KEEP only opportunities that are open to Indian students / international
    applicants, OR located in India, OR fully remote / online / virtual /
    global / "open to all".
  * REJECT opportunities restricted to another country's citizens or residents,
    or that are onsite in a foreign country (e.g. US-only, UK-only, Canada-only,
    Nigeria-only, EU-only onsite roles). Being Indian, I cannot take these.
  * REJECT full-time "new grad" / entry-level roles that need graduation in
    2025 / 2026 / 2027 or an already-completed degree — I graduate in 2028.
  * REJECT roles requiring a Master's / PhD or years of work experience.

- NOT interested in: MBA / management, sales / marketing / HR, business /
  case-study / strategy competitions, journalism, content writing,
  finance / consulting, medical, law, agriculture, arts / humanities-only.
""").strip()

# ============================================================
# GROQ LLM SETTINGS
# ============================================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()

# Update here if the model gets deprecated (see https://console.groq.com/docs/models)
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

# Minimum LLM relevance score (0-10) for an opportunity to be sent. Higher = stricter.
MIN_RELEVANCE_SCORE = int(os.environ.get("MIN_RELEVANCE_SCORE", "6"))

# How many opportunities to score per LLM request (keeps prompts small & cheap).
LLM_BATCH_SIZE = int(os.environ.get("LLM_BATCH_SIZE", "15"))

# ============================================================
# CATEGORIES
# ============================================================
# Categories that are always relevant to the user — these skip the LLM entirely
# to conserve the free-tier quota. ONLY coding hackathons are blanket-approved;
# competitions / scholarships / fellowships are relevance-checked because many
# are non-tech (management case comps, climate/journalism fellowships, etc.).
AUTO_APPROVE_CATEGORIES = {"HACKATHON"}

# ============================================================
# DEDUP / SEEN STORE
# ============================================================
# Absolute path to the dedup store (repo_root/data/seen.json). Computed from this
# file's location so it is correct regardless of the current working directory.
SEEN_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "seen.json")
)

# Prune seen entries older than this many seconds (30 days).
SEEN_MAX_AGE = 30 * 86400
