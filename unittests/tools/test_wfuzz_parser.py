from dojo.models import Test
from dojo.tools.wfuzz.parser import WFuzzParser
from unittests.dojo_test_case import DojoTestCase


class TestWFuzzParser(DojoTestCase):

    def test_parse_no_findings(self):
        with open("unittests/scans/wfuzz/no_findings.json") as testfile:
            parser = WFuzzParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(0, len(findings))

    def test_parse_one_finding(self):
        with open("unittests/scans/wfuzz/one_finding.json") as testfile:
            parser = WFuzzParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(1, len(findings))

    def test_parse_many_finding(self):
        with open("unittests/scans/wfuzz/many_findings.json") as testfile:
            parser = WFuzzParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(4, len(findings))

    def test_one_dup_finding(self):
        with open("unittests/scans/wfuzz/one_dup_finding.json") as testfile:
            parser = WFuzzParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(4, len(findings))

    def test_issue_7863(self):
        with open("unittests/scans/wfuzz/issue_7863.json") as testfile:
            parser = WFuzzParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(1, len(findings))
            self.assertEqual("Medium", findings[0].severity)

    def test_one_finding_responsecode_missing(self):
        with open("unittests/scans/wfuzz/one_finding_responsecode_missing.json") as testfile:
            parser = WFuzzParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(1, len(findings))
