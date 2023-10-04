---
title: "Checkmarx"
toc_hide: true
---

### File Types
DefectDojo parser can accept `Checkmarx Scan`, `Checkmarx Scan detailed` files as XML, and `Checkmarx OSA` files as JSON.
Data from SAST, SCA and KICS are supported.

#### Checkmarx OSA process
Checkmarx OSA files require some additional steps before they can be parsed into DefectDojo:

- To generate the OSA report using Checkmarx CLI:
`./runCxConsole.sh OsaScan -v -CxServer <...> -CxToken <..> -projectName <...>  -enableOsa -OsaLocationPath <lib_folder> -OsaJson <output_folder>`

- That will generate three files, two of which are needed for defectdojo. Build the file for defectdojo with the jq utility:
`jq -s . CxOSAVulnerabilities.json CxOSALibraries.json`


### Sample Reports
Sample Checkmarx files can be found at https://github.com/DefectDojo/django-DefectDojo/tree/master/unittests/scans/checkmarx.