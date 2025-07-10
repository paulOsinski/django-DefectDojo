---
title: "Finding Group"
date: 2021-02-02T20:46:29+01:00
draft: false
type: docs
---

Finding Groups are, by definition, a manual grouping of Findings.  Finding Groups can be created through the Bulk Edit menu.  However, Finding Groups can only be created with Findings that are in the same Test.

## Finding Group Metadata
Finding Groups aggregate metadata from all grouped Findings:

* A Finding Group's Severity is the highest Severity value for Findings in the Group
* A Finding Group's Status is set to Active if any associated Findings are Active, otherwise it will be set to Mitigated
* A Finding Group's [SLA] is set to the lowest SLA value for a given Finding

![image](images/finding_group.png)

## Finding Group Actions
Finding Groups can be handled in the following ways:

* They can be pushed to Jira, combining many Findings into a single Jira Issue

## Working With Finding Groups
Finding Groups can be created in 2 ways:

* From a list of existing Findings, through the [Bulk Edit](/en/working_with_findings/organizing_engagements_tests/tagging_objects/) Menu
* Automatically from the [Import Scan](/en/connecting_your_tools/import_scan_files/import_scan_ui/) form, when an automatic "Group By" option is chosen and the "Create Finding Groups For All Findings" option is selected
* Objects can be automatically sorted into groups by **Component Name**, **Component Name and Version**, **File Path**, or **Finding Title**

## Other Ways To Sort Findings
If you're looking for a method to organize your Findings in DefectDojo, consider also:

* Using the [Product Hierarchy](/en/working_with_findings/organizing_engagements_tests/product_hierarchy/), sorting your Findings by their Test, Engagement, Product or Product Type
* Using [Tags](/en/working_with_findings/organizing_engagements_tests/tagging_objects/)