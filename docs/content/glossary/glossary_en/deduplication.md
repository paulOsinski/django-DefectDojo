---
title: "Deduplication"
date: 2021-02-02T20:46:29+01:00
draft: false
type: docs
---

DefectDojo can automatically identify and label duplicate Findings.  If implemented correctly, Deduplication can make AppSec processes significantly more efficient:

* Identical Findings from different reports can be automatically linked, with duplicate instances of the Finding being set to [Inactive] and removed from metrics or alerts
* **DefectDojo Pro** allows you to identify 'cross-tool' duplicates, meaning that Findings can be caught as duplicates even if they're reported by a different tool
* Duplicates can also be handled through **Reimport** methods, which automatically filter out and discard duplicate Findings

## How Duplicates Are Identified
DefectDojo assigns a unique Hashcode to each Finding, based on data fields from the Finding.  This may include fields like

* a Finding's Title
* CWE
* a Component Name

Each supported [Tool](/en/connecting_your_tools/parsers/) uses different fields for Deduplication based on the context that the tool is meant to report on.  **DefectDojo Pro** users can change the fields used for Deduplication in-app.

For more information, see our guides to [deduplication](/en/working_with_findings/finding_deduplication/about_deduplication/) and [deduplication tuning](/en/working_with_findings/finding_deduplication/tune_deduplication/)