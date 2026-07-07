"""
Unit tests for the Opportunity Bot's pure functions (filtering, dedup,
seen-store migration, category detection). These are the pieces most likely to
regress when sources change, and they run without any network access.

Run from the repo root:   python3 -m unittest discover -s scripts/tests -v
"""

import os
import sys
import json
import time
import tempfile
import unittest

# Make the `core` and `scrapers` packages importable regardless of cwd.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.utils import (  # noqa: E402
    is_junk, is_blocked, normalize_key, make_hash, keyword_relevance,
    load_seen, save_seen,
)
from core import config, utils  # noqa: E402
from scrapers.scholarships import detect_category  # noqa: E402


class TestIsJunk(unittest.TestCase):
    def test_flags_result_and_admit_card(self):
        self.assertTrue(is_junk("SSC CGL Answer Key 2025 released"))
        self.assertTrue(is_junk("Railway Group D Admit Card download"))
        self.assertTrue(is_junk("UPSC Result declared"))

    def test_keeps_real_openings(self):
        self.assertFalse(is_junk("ISRO Scientist Engineer Recruitment 2025"))
        self.assertFalse(is_junk("Google Summer of Code applications open"))


class TestIsBlocked(unittest.TestCase):
    def test_blocks_unwanted_roles(self):
        self.assertTrue(is_blocked("Digital Marketing Internship"))
        self.assertTrue(is_blocked("Sales Executive"))
        self.assertTrue(is_blocked("HR Intern"))
        self.assertTrue(is_blocked("Content Writing Internship"))

    def test_short_words_matched_as_whole_words_only(self):
        # "sales" must not fire on "Salesforce"; "ops" must not fire on "DevOps".
        self.assertFalse(is_blocked("Salesforce Developer Intern"))
        self.assertFalse(is_blocked("DevOps Engineer Internship"))

    def test_allows_tech_roles(self):
        self.assertFalse(is_blocked("Machine Learning Intern"))
        self.assertFalse(is_blocked("Backend Software Developer"))


class TestNormalizeKey(unittest.TestCase):
    def test_collapses_near_duplicates(self):
        a = normalize_key("Software Engineer Intern at Google")
        b = normalize_key("software engineer INTERNSHIP for Google!!!")
        self.assertEqual(a, b)

    def test_distinct_titles_differ(self):
        self.assertNotEqual(
            normalize_key("Data Scientist"), normalize_key("Web Developer")
        )


class TestKeywordRelevance(unittest.TestCase):
    def test_auto_approve_categories_always_relevant(self):
        for cat in config.AUTO_APPROVE_CATEGORIES:
            self.assertTrue(
                keyword_relevance({"title": "anything", "description": "", "category": cat})
            )

    def test_tech_internship_relevant(self):
        opp = {"title": "Python Developer Intern", "description": "", "category": "INTERNSHIP"}
        self.assertTrue(keyword_relevance(opp))

    def test_nontech_internship_not_relevant(self):
        opp = {"title": "Fashion Designer Trainee", "description": "", "category": "INTERNSHIP"}
        self.assertFalse(keyword_relevance(opp))


class TestDetectCategory(unittest.TestCase):
    def test_detects_each_type(self):
        self.assertEqual(detect_category("Chevening Fellowship", []), "FELLOWSHIP")
        self.assertEqual(detect_category("Fully funded Scholarship", []), "SCHOLARSHIP")
        self.assertEqual(detect_category("Summer Internship 2026", []), "INTERNSHIP")
        self.assertEqual(detect_category("Global AI Hackathon", []), "HACKATHON")
        self.assertEqual(detect_category("Coding Contest", []), "COMPETITION")
        self.assertEqual(detect_category("Random newsletter update", []), "OPPORTUNITY")

    def test_uses_rss_category_tags(self):
        self.assertEqual(detect_category("Great news", ["Hackathon"]), "HACKATHON")


class TestSeenStore(unittest.TestCase):
    def setUp(self):
        # Redirect the seen store to a temp file for isolation.
        self._tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self._tmp.close()
        self._orig = utils.SEEN_FILE
        utils.SEEN_FILE = self._tmp.name

    def tearDown(self):
        utils.SEEN_FILE = self._orig
        os.unlink(self._tmp.name)

    def test_missing_file_returns_empty_dict(self):
        os.unlink(self._tmp.name)
        self.assertEqual(load_seen(), {})
        # recreate so tearDown's unlink succeeds
        open(self._tmp.name, "w").close()

    def test_migrates_old_list_format_to_dict(self):
        with open(self._tmp.name, "w") as f:
            json.dump(["hash1", "hash2"], f)
        migrated = load_seen()
        self.assertIsInstance(migrated, dict)
        self.assertEqual(set(migrated.keys()), {"hash1", "hash2"})

    def test_save_prunes_old_entries(self):
        now = int(time.time())
        data = {
            "fresh": now,
            "stale": now - config.SEEN_MAX_AGE - 10,  # older than max age
        }
        save_seen(data)
        reloaded = load_seen()
        self.assertIn("fresh", reloaded)
        self.assertNotIn("stale", reloaded)

    def test_hash_is_stable(self):
        self.assertEqual(make_hash("abc"), make_hash("abc"))
        self.assertNotEqual(make_hash("abc"), make_hash("abd"))


if __name__ == "__main__":
    unittest.main()
