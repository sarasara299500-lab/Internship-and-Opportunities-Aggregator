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
- 3rd year B.Tech CSE student (entering 5th semester)
- College: LNCT Bhopal, Madhya Pradesh
- Interests: AI/ML, Software Development, Data Structures & Algorithms, Web Development
- Skills: Python, C++, Java, SQL, HTML, CSS, JavaScript
- Looking for: Software Engineering internships, AI/ML internships, hackathons,
  scholarships, fellowships, research opportunities, coding competitions
- NOT interested in: MBA, law, medical, agriculture, arts/humanities-only roles,
  sales/marketing/HR internships, content writing roles
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
# to conserve the free-tier quota.
AUTO_APPROVE_CATEGORIES = {"HACKATHON", "COMPETITION", "SCHOLARSHIP", "FELLOWSHIP"}

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
