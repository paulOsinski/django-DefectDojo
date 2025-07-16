---
title: "Finding Template"
date: 2021-02-02T20:46:29+01:00
draft: false
type: docs
---

Finding Templates can be used to quickly adjust metadata for Findings.

A Finding Template can have any of the following:

* a Title
* a CWE
* one or more Vulnerability IDs
* a CVSSV3 Vector String
* a [Severity]
* a Description, Mitigation, Impact and/or References field
* Finding Tags

When applying a Finding Template to an existing Finding, you can decide whether you want to **Keep**, **Replace** or **Combine** the data from the original Finding with the data from the Finding Template.  Each field can have its own decision made on how to handle the data from the Finding and the Finding Template.

## See Also: Rules Engine

**DefectDojo Pro** includes **Rules Engine**, an automation method which allows you to automatically transform Findings when they match a given logical trigger condition.  For example, you could automatically assign all Findings that have a certain Tag to a Group, add a Note to those Findings, or take many other actions beyond what a Finding Template can do.

See [Rules Engine](/en/customize_dojo/rules_engine/) documentation for more info.
