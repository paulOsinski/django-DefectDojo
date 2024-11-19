---
title: "New User Checklist"
description: "Get Started With DefectDojo"
draft: "false"
weight: 1
chapter: true
---

Here's a quick reference you can use to ensure successful implementation - from a blank canvas to a fully functional app.

### The Basics

1. Start by [importing a file](../../connecting_your_tools/import_scan_files/import_scan_ui) using the UI.  This is generally the quickest way to see how your data fits into the DefectDojo model. (note: OS users will need to set up a Product Type and Product before they can import data)

2. Now that you have data in DefectDojo, learn more about how to organize it with the [Product Hierarchy Overview](../../working_with_findings/organizing_engagements_tests/product-hierarchy-overview). The Product Hierarchy creates a working inventory of your apps, which helps you divide your data up into logical categories. These categories can be used to apply access control rules, or to segement your reports to the correct team.

3. Try [creating a Report](../../pro_reports/using-the-report-builder/) to summarize the data you've imported.  Reports can be used to quickly share Findings with stakeholders such as Product Owners.

This is the essence of DefectDojo - import security data, organize it, and present it to the folks who need to know. 

All of these features can be automated, and because DefectDojo can handle over 190 tools (at time of writing) you should be all set to create a functional security inventory of your entire organizational output.

### Other guides

- Does your organization use Jira? Learn how to use our [Jira integration](../jira_integration/Connect%20DefectDojo%20to%20Jira.md) to create Jira tickets from the data you ingest.
- Are you expecting to share DefectDojo with many users in your organization? Check out our guides to [user management](../user_management/about-permissions-roles) and set up role-based access control (RBAC).
- Ready to dive into automation? Learn how to use the [DefectDojo API](../connecting_your_tools/import_scan_files/api_pipeline_modelling) to automatically import new data, and build a robust CI / CD pipeline.