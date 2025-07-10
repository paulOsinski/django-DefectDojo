---
title: "Finding"
date: 2021-02-02T20:46:29+01:00
draft: false
type: docs
---

A Finding in DefectDojo represents a security vulnerability.  Findings can be entered manually, but are generally added to DefectDojo by importing scan reports from security tools.

## Finding Attributes
Findings always have the following attributes:

* A [Status], determining whether the Finding is Active or Inactive, along with further sub-statuses sorting why
* A [Severity Value]
* A [Risk Value] (pro only)
* A [Priority] Score (pro only)
* An [SLA], governed by the containing Product

## How Findings are Organized
Findings are stored in:
* An associated [Test], which is the main place a report is summarized in DefectDojo
* An associated [Product Type], [Product], and [Engagement], three [Product Hierarchy] elements which categorize the [Test]