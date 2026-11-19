"""Regressions from the 19 November 2026 export review."""
import unittest

import backend.config as config
from backend.core.experience import experience_requirements
from backend.core.location import is_india_or_unknown, parse_country
from backend.fetchers.successfactors import _detail_priority


class InlineExperienceLabelTests(unittest.TestCase):
    def required(self, text, title=""):
        return experience_requirements(text, title)[0]

    def test_label_with_non_breaking_space(self):
        text = "Designation : Analyst \n Level : L1 \n Experience :\xa0 1-3 Years \n Job Role : Looking for"
        self.assertEqual(self.required(text), 1)
        self.assertEqual(self.required("Designation : Apprentice\n Experience :\xa0 0 Years \n Job Role :"), 0)

    def test_inline_range_after_label(self):
        self.assertEqual(self.required("Position Title: Deputy Manager Experience: 2-5 years Qualification: B.E/ B.Tech"), 2)
        self.assertEqual(self.required("Education: BE : Mechanical Job Related Experience: 12-18 Years Business Understanding: x"), 12)
        self.assertEqual(self.required("Team.\n Suggested experience: 8-12 years in application development. \n Key Responsibilities \n Take part"), 8)

    def test_inline_value_is_not_overread(self):
        self.assertIsNone(self.required("Experience: 40 years in business and growing"))
        self.assertIsNone(self.required("Preferred experience: 5 years of SQL"))


class NonIndiaCountryTests(unittest.TestCase):
    def test_countries_seen_in_the_export_are_not_unknown(self):
        for text, country in [("Argentina - Buenos Aires, Argentina", "Argentina"),
                              ("Three IFC, Yeongdeungpo-gu, 150-945 Seoul, Korea, Republic of", "South Korea")]:
            self.assertEqual(parse_country(text), country)
            self.assertFalse(is_india_or_unknown(text))

    def test_india_and_unknown_still_pass(self):
        self.assertTrue(is_india_or_unknown("Bangalore"))
        self.assertTrue(is_india_or_unknown("Pune, Maharashtra, India"))


class DetailFetchOrderTests(unittest.TestCase):
    def test_target_and_entry_titles_are_fetched_first(self):
        titles = ["Senior Administrator", "Support Specialist", "Data Analyst", "Campus-Beginner", "Sr Analyst"]
        order = sorted(titles, key=_detail_priority)
        self.assertEqual(order[:2], ["Data Analyst", "Campus-Beginner"])
        self.assertEqual(order[-2:], ["Senior Administrator", "Sr Analyst"])


class RemovedSourceTests(unittest.TestCase):
    def test_exl_is_documented_as_removed(self):
        self.assertIn("exl", config.DISABLED_CAREER_SOURCES)
        self.assertNotIn("exl", [row.get("company") for row in config.ORACLE])
        self.assertNotIn("EXL", config.DISPLAY_NAMES.values())


if __name__ == "__main__":
    unittest.main()
