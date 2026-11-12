import unittest
from credit_risk import analyze,kmeans
class CreditRiskTests(unittest.TestCase):
 def test_two_clear_clusters(self):
  rows=[{"x":"0","y":"0"},{"x":"0.1","y":"0"},{"x":"10","y":"10"},{"x":"10.1","y":"10"}];r=analyze(rows,["x","y"],2);self.assertEqual(r[0]["segment"],r[1]["segment"]);self.assertNotEqual(r[0]["segment"],r[2]["segment"])
 def test_missing_values_dropped(self):self.assertEqual(len(analyze([{"x":"1"},{"x":"bad"}],["x"],1)),1)
if __name__=="__main__":unittest.main()
