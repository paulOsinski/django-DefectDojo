import json

from cvss.cvss3 import CVSS3

from dojo.models import Finding


class SnykCodeParser:

    def get_fields(self) -> list[str]:
        """
        Return the list of fields used in the Snyk Code Parser

        Fields:
        - title: Made using the title from Snyk Code scanner.
        - severity: Set to severity from Snyk Code Scanner converted to Defect Dojo format.
        - severity_justification: Made using severity and CVSS score from Snyk Code Parser.
        - description: Made by combining package name, version, vulnerable version(s), and description from Snyk Code Scanner.
        - mitigation: Set to a string and is added on if more context is available.
        - component_name: Set to component_name from Snyk Code Scanner.
        - component_version: Set to version from Snyk Code Scanner.
        - false_p: Set to false.
        - duplicate: Set to false.
        - out_of_scope: Set to false.
        - impact: Set to same value as severity.
        - static_finding: Set to true.
        - dynamic_finding: Set to false.
        - file_path: Set to from value in the Snyk Code scanner output.
        - vuln_id_from_tool: Set to id from Snyk Code scanner.
        - cvssv3: Set to cvssv3 from Snyk Code scanner if available.
        - cwe: Set to the cwe values outputted from Burp Scanner.
        """
        return [
            "title",
            "severity",
            "severity_justification",
            "description",
            "mitigation",
            "component_name",
            "component_version",
            "false_p",
            "duplicate",
            "out_of_scope",
            "impact",
            "static_finding",
            "dynamic_finding",
            "file_path",
            "vuln_id_from_tool",
            "cvssv3",
            "cwe",
        ]

    def get_dedupe_fields(self) -> list[str]:
        """
        Return the list of dedupe fields used in the Snyk Code Parser

        Fields:
        - vuln_id_from_tool: Set to id from Snyk Code scanner.
        - file_path: Set to from value in the Snyk Code scanner output.
        """
        return [
            "vuln_id_from_tool",
            "file_path",
        ]

    def get_scan_types(self):
        return ["Snyk Code Scan"]

    def get_label_for_scan_types(self, scan_type):
        return scan_type  # no custom label for now

    def get_description_for_scan_types(self, scan_type):
        return "Snyk output file (snyk test --json > snyk.json) can be imported in JSON format."

    def get_findings(self, json_output, test):
        reportTree = self.parse_json(json_output)

        if isinstance(reportTree, list):
            temp = []
            for moduleTree in reportTree:
                temp += self.process_tree(moduleTree, test)
            return temp
        return self.process_tree(reportTree, test)

    def process_tree(self, tree, test):
        return list(self.get_items(tree, test)) if tree else []

    def parse_json(self, json_output):
        try:
            data = json_output.read()
            try:
                tree = json.loads(str(data, "utf-8"))
            except Exception:
                tree = json.loads(data)
        except Exception:
            msg = "Invalid format"
            raise ValueError(msg)

        return tree

    def get_items(self, tree, test):
        items = {}
        iterator = 0
        if "vulnerabilities" in tree:
            target_file = tree.get("displayTargetFile", None)
            upgrades = tree.get("remediation", {}).get("upgrade", None)
            vulnerabilityTree = tree["vulnerabilities"]
            for node in vulnerabilityTree:
                item = self.get_item(
                    node, test, target_file=target_file, upgrades=upgrades,
                )
                items[iterator] = item
                iterator += 1
        elif "runs" in tree and tree["runs"][0].get("results"):
            results = tree["runs"][0]["results"]
            for node in results:
                item = self.get_code_item(
                    node, test,
                )
                items[iterator] = item
                iterator += 1
        return list(items.values())

    def get_item(self, vulnerability, test, target_file=None, upgrades=None):
        # vulnerable and unaffected versions can be in string format for a single vulnerable version,
        # or an array for multiple versions depending on the language.
        if isinstance(vulnerability["semver"]["vulnerable"], list):
            vulnerable_versions = ", ".join(
                vulnerability["semver"]["vulnerable"],
            )
        else:
            vulnerable_versions = vulnerability["semver"]["vulnerable"]

        # Following the CVSS Scoring per https://nvd.nist.gov/vuln-metrics/cvss
        if "cvssScore" in vulnerability:
            if vulnerability["cvssScore"] is None:
                severity = vulnerability["severity"].title()
            # If we're dealing with a license finding, there will be no
            # cvssScore
            elif vulnerability["cvssScore"] <= 3.9:
                severity = "Low"
            elif (
                vulnerability["cvssScore"] >= 4.0
                and vulnerability["cvssScore"] <= 6.9
            ):
                severity = "Medium"
            elif (
                vulnerability["cvssScore"] >= 7.0
                and vulnerability["cvssScore"] <= 8.9
            ):
                severity = "High"
            else:
                severity = "Critical"
        else:
            # Re-assign 'severity' directly
            severity = vulnerability["severity"].title()

        # Construct "file_path" removing versions
        vulnPath = ""
        for index, item in enumerate(vulnerability["from"]):
            if index == 0:
                vulnPath += "@".join(item.split("@")[0:-1])
            else:
                vulnPath += " > " + "@".join(item.split("@")[0:-1])

        # create the finding object
        finding = Finding(
            title=vulnerability["from"][0] + ": " + vulnerability["title"],
            test=test,
            severity=severity,
            severity_justification="Issue severity of: **"
            + severity
            + "** from a base "
            + "CVSS score of: **"
            + str(vulnerability.get("cvssScore"))
            + "**",
            description="## Component Details\n - **Vulnerable Package**: "
            + vulnerability["packageName"]
            + "\n- **Current Version**: "
            + str(vulnerability["version"])
            + "\n- **Vulnerable Version(s)**: "
            + vulnerable_versions
            + "\n- **Vulnerable Path**: "
            + " > ".join(vulnerability["from"])
            + "\n"
            + vulnerability["description"],
            mitigation="A fix (if available) will be provided in the description.",
            component_name=vulnerability["packageName"],
            component_version=vulnerability["version"],
            false_p=False,
            duplicate=False,
            out_of_scope=False,
            impact=severity,
            static_finding=True,
            dynamic_finding=False,
            file_path=vulnPath,
            vuln_id_from_tool=vulnerability["id"],
        )
        finding.unsaved_tags = []

        # CVSSv3 vector
        if vulnerability.get("CVSSv3"):
            finding.cvssv3 = CVSS3(vulnerability["CVSSv3"]).clean_vector()

        # manage CVE and CWE with idnitifiers
        cwe_references = ""
        if "identifiers" in vulnerability:
            if "CVE" in vulnerability["identifiers"]:
                vulnerability_ids = vulnerability["identifiers"]["CVE"]
                if vulnerability_ids:
                    finding.unsaved_vulnerability_ids = vulnerability_ids

            if "CWE" in vulnerability["identifiers"]:
                cwes = vulnerability["identifiers"]["CWE"]
                if cwes:
                    # Per the current json format, if several CWEs, take the
                    # first one.
                    finding.cwe = int(cwes[0].split("-")[1])
                    if len(vulnerability["identifiers"]["CWE"]) > 1:
                        cwe_references = ", ".join(cwes)
                else:
                    finding.cwe = 1035

        references = ""
        if "id" in vulnerability:
            references = "**SNYK ID**: https://app.snyk.io/vuln/{}\n\n".format(
                vulnerability["id"],
            )

        if cwe_references:
            references += f"Several CWEs were reported: \n\n{cwe_references}\n"

        # Append vuln references to references section
        for item in vulnerability.get("references", []):
            references += "**" + item["title"] + "**: " + item["url"] + "\n"

        finding.references = references

        finding.description = finding.description.strip()

        # Find remediation string limit indexes
        remediation_index = finding.description.find("## Remediation")
        references_index = finding.description.find("## References")

        # Add the remediation substring to mitigation section
        if (remediation_index != -1) and (references_index != -1):
            finding.mitigation = finding.description[
                remediation_index:references_index
            ]

        # Add Target file if supplied
        if target_file:
            finding.unsaved_tags.append(f"target_file:{target_file}")
            finding.mitigation += f"\nUpgrade Location: {target_file}"

        # Add the upgrade libs list to the mitigation section
        if upgrades:
            for current_pack_version, meta_dict in upgrades.items():
                upgraded_pack = meta_dict["upgradeTo"]
                tertiary_upgrade_list = meta_dict["upgrades"]
                if any(
                    lib.split("@")[0] in finding.mitigation
                    for lib in tertiary_upgrade_list
                ):
                    finding.unsaved_tags.append(
                        f"upgrade_to:{upgraded_pack}",
                    )
                    finding.mitigation += f"\nUpgrade from {current_pack_version} to {upgraded_pack} to fix this issue, as well as updating the following:\n - "
                    finding.mitigation += "\n - ".join(tertiary_upgrade_list)
        return finding

    def get_code_item(self, vulnerability, test):
        ruleId = vulnerability["ruleId"]
        ruleIndex = vulnerability["ruleIndex"]
        message = vulnerability["message"]["text"]
        score = vulnerability["properties"]["priorityScore"]
        locations_uri = vulnerability["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
        locations_uriBaseId = vulnerability["locations"][0]["physicalLocation"]["artifactLocation"]["uriBaseId"]
        locations_startLine = vulnerability["locations"][0]["physicalLocation"]["region"]["startLine"]
        locations_endLine = vulnerability["locations"][0]["physicalLocation"]["region"]["endLine"]
        locations_startColumn = vulnerability["locations"][0]["physicalLocation"]["region"]["startColumn"]
        locations_endColumn = vulnerability["locations"][0]["physicalLocation"]["region"]["endColumn"]
        isAutofixable = vulnerability["properties"]["isAutofixable"]

        if score <= 399:
            severity = "Low"
        elif score <= 699:
            severity = "Medium"
        elif score <= 899:
            severity = "High"
        else:
            severity = "Critical"
        # create the finding object
        return Finding(
            vuln_id_from_tool=ruleId,
            file_path=locations_uri,
            title=ruleId + "_" + locations_uri,
            test=test,
            severity=severity,
            description="**ruleId**: " + str(ruleId) + "\n"
            + "**ruleIndex**: " + str(ruleIndex) + "\n"
            + "**message**: " + str(message) + "\n"
            + "**score**: " + str(score) + "\n"
            + "**uri**: " + locations_uri + "\n"
            + "**uriBaseId**: " + locations_uriBaseId + "\n"
            + "**startLine**: " + str(locations_startLine) + "\n"
            + "**endLine**: " + str(locations_endLine) + "\n"
            + "**startColumn**: " + str(locations_startColumn) + "\n"
            + "**endColumn**: " + str(locations_endColumn) + "\n"
            + "**isAutofixable**: " + str(isAutofixable) + "\n",
            false_p=False,
            duplicate=False,
            out_of_scope=False,
            static_finding=True,
            dynamic_finding=False,
        )
