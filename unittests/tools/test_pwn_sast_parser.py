from dojo.models import Test
from dojo.tools.pwn_sast.parser import PWNSASTParser
from unittests.dojo_test_case import DojoTestCase


class TestPWNSASTParser(DojoTestCase):

    def test_parse_no_findings(self):
        with open("unittests/scans/pwn_sast/no_findings.json") as testfile:
            parser = PWNSASTParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(0, len(findings))

    def test_parse_one_finding(self):
        with open("unittests/scans/pwn_sast/one_finding.json") as testfile:
            parser = PWNSASTParser()
            findings = parser.get_findings(testfile, Test())
            self.assertIsInstance(findings, list)
            self.assertEqual(1, len(findings))

    def test_parse_many_finding(self):
        with open("unittests/scans/pwn_sast/many_findings.json") as testfile:
            parser = PWNSASTParser()
            findings = parser.get_findings(testfile, Test())
            self.assertIsInstance(findings, list)
            self.assertEqual(3, len(findings))

    def test_one_dup_finding(self):
        with open("unittests/scans/pwn_sast/one_dup_finding.json") as testfile:
            parser = PWNSASTParser()
            findings = parser.get_findings(testfile, Test())
            self.assertIsInstance(findings, list)
            self.assertEqual(1, len(findings))

    def test_title_is_not_none(self):
        with open("unittests/scans/pwn_sast/one_finding.json") as testfile:
            parser = PWNSASTParser()
            findings = parser.get_findings(testfile, Test())
            self.assertIsInstance(findings, list)
            for finding in findings:
                self.assertIsNotNone(finding.title)
                self.assertIsNotNone(finding.unique_id_from_tool)
