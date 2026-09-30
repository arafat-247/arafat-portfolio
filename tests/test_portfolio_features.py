import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import build_portfolio_features as features


class PortfolioFeatureTests(unittest.TestCase):
    def test_education_assignment(self):
        item={"title":"Teacher shortages strain government primary schools","excerpt":"","category":"Education"}
        enriched=features.enrich([item])[0]
        self.assertEqual(enriched["beat"],"education")

    def test_series_assignment(self):
        item={"title":"Public university admission woes deepen","excerpt":"","category":"Education"}
        enriched=features.enrich([item])[0]
        self.assertIn("universities-campus-governance",enriched["series"])

    def test_collections_are_bylined_only(self):
        definition=features.BEATS[0]
        items=[
            {"beat":"education","credit_type":"byline"},
            {"beat":"education","credit_type":"contribution"},
        ]
        self.assertEqual(len(features.rows_for(definition,items,"beat")),1)


if __name__=="__main__":
    unittest.main()
