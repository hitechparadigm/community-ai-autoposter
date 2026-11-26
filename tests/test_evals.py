"""Tests of the evaluation set's checks (no Claude calls): python -m unittest discover -s tests"""
import json
import os
import re
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autoposter import evals  # noqa: E402

with open(os.path.join(evals.EVAL_DIR, "cases.json"), encoding="utf-8") as _f:
    CASES = json.load(_f)["cases"]
CASE = next(c for c in CASES if c["id"] == "min-wage-mb")
GOOD = {"title": "💵 Манітоба підвищить мінімальну зарплату до 16,50 долара",
        "body": ("З 1 жовтня мінімальна зарплата в Манітобі зросте на 65 центів, до 16,50 долара за годину. "
                 "Це стосується близько 40 000 працівників, переважно в торгівлі та закладах харчування, "
                 "повідомив міністр праці провінції Деніел Моро (Daniel Moreau).\n\n"
                 "Підвищення прив'язане до інфляції. Бізнес-об'єднання Manitoba Chambers of Commerce погоджується, "
                 "але просить надалі попереджати роботодавців раніше. Нова ставка діє для всіх годин, "
                 "відпрацьованих від 1 жовтня, зокрема для студентів і тих, хто працює неповний день."),
        "problems": []}


class Checks(unittest.TestCase):
    def test_cases_are_well_formed(self):
        ids = [c["id"] for c in CASES]
        self.assertEqual(len(ids), len(set(ids)))
        for c in CASES:
            self.assertIn(c["mode"], ("news", "tips"))
            for key in ("title", "summary", "article", "source", "region"):
                self.assertTrue(c[key], f"{c['id']}: {key}")
            for alternatives in c["expect"]["facts"]:
                for a in alternatives:
                    re.compile(evals.normalize(a))

    def test_good_post_passes(self):
        res = evals.score(CASE, GOOD)
        self.assertTrue(all(ok for ok, _ in res.values()), res)

    def test_each_kind_of_error_is_caught(self):
        bad = {**GOOD, "body": GOOD["body"].replace("16,50", "16,00").replace("(Daniel Moreau)", "")
               .replace("Manitoba Chambers of Commerce", "Палати торгівлі Манітоби")
               .replace("Підвищення", "Підвищення являється")}
        res = evals.score(CASE, bad)
        for check in ("people", "names_kept", "language"):
            self.assertFalse(res[check][0], check)
        self.assertIn("1 жовтня", evals.score(CASE, {**GOOD, "body": GOOD["body"].replace("1 жовтня", "осені")
                                                       .replace("від осені", "від осені")})["facts"][1])

    def test_numbers_and_names_match_in_any_form(self):
        self.assertEqual(evals.normalize("40 000 і 16.50 та 2 300 000"), "40000 і 16,50 та 2300000")
        pattern = evals.name_pattern("Канадська королівська кінна поліція (RCMP)")
        self.assertTrue(re.search(pattern, evals.normalize("заява Канадської королівської кінної поліції")))
        pattern = evals.name_pattern("міністерство імміграції, біженців і громадянства Канади (IRCC); далі коротко")
        self.assertTrue(re.search(pattern, evals.normalize("Міністерство імміграції, біженців та громадянства Канади")))

    def test_glossary_names_are_required(self):
        case = next(c for c in CASES if c["id"] == "rcmp-deepfake")
        post = {"title": "Поліція попереджає", "body": "Поліція Ванкувера попереджає про шахраїв.", "problems": []}
        ok, detail = evals.score(case, post)["glossary"]
        self.assertFalse(ok)
        self.assertIn("Канадська королівська кінна поліція", detail)

    def test_run_writes_scorecard(self):
        fake_post = {**GOOD, "emoji": "💵", "photo_query": ""}
        with tempfile.TemporaryDirectory() as d, \
                mock.patch.object(evals, "EVAL_DIR", d), \
                mock.patch.object(evals, "write_news", return_value=fake_post), \
                mock.patch.object(evals, "judge", return_value={"accuracy": 5, "language": 5, "usefulness": 4,
                                                                "notes": ""}), \
                mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": ""}):
            with open(os.path.join(d, "cases.json"), "w", encoding="utf-8") as f:
                json.dump({"cases": [CASE]}, f)
            evals.cmd_eval()
            with open(os.path.join(d, "results", "latest.md"), encoding="utf-8") as f:
                md = f.read()
            self.assertIn("1/1 passed every check", md)
            self.assertTrue(os.path.exists(os.path.join(d, "results", "history.csv")))


if __name__ == "__main__":
    unittest.main()
