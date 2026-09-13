import unittest

from scripts.enrich_entity import enrich_person, replace_jsonld


class EntityEnrichmentTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "site_url": "https://arafatrahaman.com",
            "site_name": "Arafat Rahaman",
            "organisation": "The Daily Star",
            "location": "Dhaka, Bangladesh",
            "description": "Journalist at The Daily Star.",
            "portrait": "assets/identity/asset0.webp",
            "areas": ["Education", "Governance"],
            "career": [{"role": "Staff Reporter"}],
            "education": [{"institution": "University of Rajshahi"}],
            "membership": {"name": "Investigative Reporters & Editors"},
            "recognition": [{"year": "2025", "title": "AccessFest Fellowship", "organisation": "Investigative Reporters & Editors"}],
            "social": {
                "daily_star": "https://www.thedailystar.net/author/arafat-rahaman",
                "muck_rack": "https://muckrack.com/arafat-rahaman",
                "linkedin": "https://bd.linkedin.com/in/arafat-rahaman",
            },
        }

    def test_person_has_stable_entity_id_and_identity_links(self):
        person = enrich_person({}, self.config)
        self.assertEqual(person["@id"], "https://arafatrahaman.com/about/#person")
        self.assertEqual(person["jobTitle"], "Staff Reporter")
        self.assertEqual(person["worksFor"]["name"], "The Daily Star")
        self.assertEqual(person["worksFor"]["@id"], "https://www.thedailystar.net/")
        self.assertNotIn("@type", person["worksFor"])
        self.assertIn("https://www.thedailystar.net/author/arafat-rahaman", person["sameAs"])
        self.assertEqual(person["alumniOf"]["url"], "https://www.ru.ac.bd/")
        self.assertEqual(person["memberOf"]["url"], "https://www.ire.org/")
        self.assertNotIn("@type", person["memberOf"])
        self.assertIn("AccessFest Fellowship", person["award"][0])

    def test_profile_page_keeps_person_as_main_entity(self):
        source = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@type":"Person"}}</script>'
        result = replace_jsonld(source, self.config, profile=True)
        self.assertIn('"@type":"ProfilePage"', result)
        self.assertIn('"@id":"https://arafatrahaman.com/about/#person"', result)
        self.assertIn('"mainEntityOfPage":{"@id":"https://arafatrahaman.com/about/"}', result)
        self.assertNotIn('"@type":"Organization"', result)


if __name__ == "__main__":
    unittest.main()
