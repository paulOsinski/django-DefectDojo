---
title: "Hashcode"
date: 2021-02-02T20:46:29+01:00
draft: false
type: docs
---

Hashcodes are used in [Finding Deduplication](../deduplication) to identify Duplicate Findings.  Hashcodes are assigned automatically at the time of Finding creation, based on a tool's metadata.

Most tools use the following fields for Hashcode calculation:

* title
* cwe
* line
* file path
* description

**DefectDojo Pro** users can change which fields are used for hashcode calculation: [("Same-Tool Deduplication")](/en/working_with_findings/finding_deduplication/tune_deduplication/).

To see which fields a given tool uses for Deduplication by default, check the tool's entry in the [supported tools](/en/connecting_your_tools/parsers/) list.

For more information, see our guide to [deduplication](/en/working_with_findings/finding_deduplication/about_deduplication/).