## About the connector
Qualys Web Application Scanning (WAS) is a robust cloud-based application security product that continuously discovers, detects, and catalogs web applications and APIs.
<p>This document provides information about the Qualys Web Application Scanning(WAS) Connector, which facilitates automated interactions, with a Qualys Web Application Scanning(WAS) server using FortiSOAR&trade; playbooks. Add the Qualys Web Application Scanning(WAS) Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with Qualys Web Application Scanning(WAS).</p>

### Version information

Connector Version: 2.0.0


Authored By: Fortinet

Certified: No
## Installing the connector
<p>Use the <strong>Content Hub</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.</p><p>You can also use the <code>yum</code> command as a root user to install the connector:</p>
<pre>yum install cyops-connector-qualys-web-application-scanner</pre>

## Prerequisites to configuring the connector
- You must have the credentials of Qualys Web Application Scanning(WAS) server to which you will connect and perform automated operations.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the Qualys Web Application Scanning(WAS) server.

## Minimum Permissions Required
- Not applicable

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>Qualys Web Application Scanning(WAS)</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations</strong> tab enter the required configuration details:</p>
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Server URL</td><td>IP address or Hostname of the Qualys Web Application endpoint server to which you will connect and perform the automated operations.
</td>
</tr><tr><td>Username</td><td>Provide username credentials with API access to Qualys Web Application.
</td>
</tr><tr><td>Password</td><td>Provide password credentials with API access to Qualys Web Application.
</td>
</tr><tr><td>Verify SSL</td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set to True.</td></tr>
</tbody></table>

## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations from FortiSOAR&trade; release 4.10.0 and onwards:
<table border=1><thead><tr><th>Function</th><th>Description</th><th>Annotation and Category</th></tr></thead><tbody><tr><td>Get Scan Count</td><td>Returns the total number of scans in the user’s account. Input parameters are optional and are used to filter the number of scans included in the count. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission API Access. The count includes scans in the user's scope.</td><td>scan_count <br/>Investigation</td></tr>
<tr><td>Search Scans</td><td>Returns a list of scans on web applications which are in the user’s scope. Input parameters are optional and act as filters. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission API Access. The output includes scans in the user's scope.</td><td>search_scans <br/>Investigation</td></tr>
<tr><td>Get Scan Details</td><td>Retrieves details for a scan on a web application which is in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes authentication records in the user's scope.</td><td>get_scan_details <br/>Investigation</td></tr>
<tr><td>Launch Scans</td><td>Launches web application scanning. You can scan any number of web applications as a Multi-Scan through API. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access” and “Launch WAS Scan“. The output includes scan targets in the user's scope.</td><td>launch_scans <br/>Investigation</td></tr>
<tr><td>Retrieve Scan Status</td><td>Retrieve the status of a scan on a web application which is in the user’s scope.</td><td>retrieve_scan_status <br/>Investigation</td></tr>
<tr><td>Retrieve Scan Results</td><td>Retrieve the results of a scan on a web application which is in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes scan targets in the user's scope.</td><td>retrieve_scan_results <br/>Investigation</td></tr>
<tr><td>Delete Scan</td><td>Delete an existing scan on a web application which is in the user’s scope. You can delete any scan in your account that is not running. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access” and ”Delete WAS scan” permission. The scan to be deleted must be within the user’s scope.</td><td>delete_scan <br/>Investigation</td></tr>
<tr><td>Count Web Applications</td><td>Returns the total number of web applications in the user’s account. Input parameters are optional and are used to filter the number of web applications included in the count. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The count includes web applications in the user's scope.</td><td>count_webapp <br/>Investigation</td></tr>
<tr><td>Search Web Applications</td><td>Returns a list of web applications which are in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes web applications in the user's scope.</td><td>search_webapp <br/>Investigation</td></tr>
<tr><td>Get Web Application Details</td><td>Returns details for a web application which is in the user’s scope. The web application screenshot, when available, is included in the output in the “screenshot” element as a base64 encoded binary string. This string needs to be converted before a user can decode and view the image file (.jpg). Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes web applications in the user's scope.</td><td>get_webapp_details <br/>Investigation</td></tr>
<tr><td>Create Web Application</td><td>Creates a new web application. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access” and WAS Asset Permission “Create Web Asset”. The output includes web applications in the user's scope. If you want to add postman collection files, you must have the 'ENABLE_POSTMAN_COLLECTION' option enabled for your account. If this option is not enabled, contact Qualys Support to enable this option. When only “name” and “url” are specified:
- Scope defaults to ALL. The scanner will crawl all directories and subdirectories of the starting URL.
- No default option profile is specified. An option profile must be specified for each scan.
- No authentication records are defined. No form or server authentication will be performed.
- No blacklists or whitelists are defined. All directories and sub-directories of the starting URL will be scanned.</td><td>create_web_app <br/>Investigation</td></tr>
<tr><td>Delete Web Applications</td><td>Delete a web application configuration in your account. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access” and WAS Asset Permission “Delete Web Asset”. The web application to be deleted must be within the user’s scope.</td><td>delete_webapp <br/>Investigation</td></tr>
<tr><td>Search Reports</td><td>Returns a list of reports which are in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes reports in the user's scope.</td><td>search_reports <br/>Investigation</td></tr>
<tr><td>Download Report</td><td>Download a report which is in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes reports in the user's scope.</td><td>download_report <br/>Investigation</td></tr>
<tr><td>Search Option Profiles</td><td>Returns a list of option profiles which are in the user’s scope. Action logs are not included in the output. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The Output includes option profiles in the user's scope. Input parameters are optional and act as filters.</td><td>search_option_profiles <br/>Investigation</td></tr>
<tr><td>Search Schedule</td><td>Returns a list of scheduled scans on web applications which are in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes scan targets in the user's scope. Input parameters are optional and act as filters.</td><td>search_schedule <br/>Investigation</td></tr>
<tr><td>Get Schedule Details</td><td>Retrieves details for a scheduled scan on a web application which is in the user’s scope. Permissions required - User must have WAS module enabled. User account must have these permissions: Access Permission “API Access”. The output includes schedules in the user's scope.</td><td>get_schedule_details <br/>Investigation</td></tr>
</tbody></table>

### operation: Get Scan Count
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan ID</td><td>Specify the scan ID.
</td></tr><tr><td>Scan Name</td><td>Specify the scan name.
</td></tr><tr><td>Web App Name</td><td>Specify the name of the web application being scanned.
</td></tr><tr><td>Web App ID</td><td>Specify the ID of the web application being scanned.
</td></tr><tr><td>Web App Tag ID</td><td>Specify the tag ID assigned to web application being scanned.
</td></tr><tr><td>Reference</td><td>Specify the scan reference ID.
</td></tr><tr><td>Launch Date</td><td>Specify the date and time to return all the scan which was launched after specified date and time in UTC date/time format (YYYY-MM-DDTHH:MM:SSZ)
</td></tr><tr><td>Type</td><td>Specify the scan type. You can choose from the following options: VULNERABILITY or DISCOVERY.
</td></tr><tr><td>Mode</td><td>Specify the mode of the scan. You can choose from the following options: ONDEMAND, SCHEDULED or API.
</td></tr><tr><td>Status</td><td>Specify the status of the scan. You can choose from the following options: SUBMITTED, RUNNING, FINISHED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, ERROR or CANCELED.
</td></tr><tr><td>Authentication Status</td><td>Specify the status of the authentication record. You can choose from the following options: NONE, NOT_USED, SUCCESSFUL, FAILED or PARTIAL.
</td></tr><tr><td>Result Status</td><td>Specify the status of the scan. You can choose from the following options: NOT_USED, NO_HOST_ALIVE, NO_WEB_SERVICE, PROCESSING, SCAN_RESULTS_INVALID, TIME_LIMIT_REACHED, SERVICE_ERROR, SCAN_INTERNAL_ERROR, SUCCESSFUL, TO_BE_PROCESSED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, SUBMITTED, RUNNING, FINISHED, CANCELED, CANCELING ERROR, DELETED.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "responseCode": "",
        "count": ""
    }
}</pre>
### operation: Search Scans
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan ID</td><td>Specify the scan ID.
</td></tr><tr><td>Scan Name</td><td>Specify the scan name.
</td></tr><tr><td>Web App Name</td><td>Specify the name of the web application being scanned.
</td></tr><tr><td>Web App id</td><td>Specify the ID of the web application being scanned.
</td></tr><tr><td>Web App Tag ID</td><td>Specify the tag ID assigned to web application being scanned.
</td></tr><tr><td>Reference</td><td>Specify the scan reference ID.
</td></tr><tr><td>Launch Date</td><td>Specify the date and time to return all the scan which was launched after specified date and time in UTC date/time format (YYYY-MM-DDTHH:MM:SSZ)
</td></tr><tr><td>Type</td><td>Specify the scan type. You can choose from the following options: VULNERABILITY or DISCOVERY.
</td></tr><tr><td>Mode</td><td>Specify the mode of the scan. You can choose from the following options: ONDEMAND, SCHEDULED or API.
</td></tr><tr><td>Status</td><td>Specify the status of the scan. You can choose from the following options: SUBMITTED, RUNNING, FINISHED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, ERROR or CANCELED.
</td></tr><tr><td>Authentication Status</td><td>Specify the status of the authentication record. You can choose from the following options: NONE, NOT_USED, SUCCESSFUL, FAILED or PARTIAL.
</td></tr><tr><td>Result Status</td><td>Specify the status of the scan. You can choose from the following options: NOT_USED, NO_HOST_ALIVE, NO_WEB_SERVICE, PROCESSING, SCAN_RESULTS_INVALID, TIME_LIMIT_REACHED, SERVICE_ERROR, SCAN_INTERNAL_ERROR, SUCCESSFUL, TO_BE_PROCESSED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, SUBMITTED, RUNNING, FINISHED, CANCELED, CANCELING ERROR, DELETED.
</td></tr><tr><td>Limit</td><td>Specify the total number of items to return. The default is 100. You can specify a value from 1 to 1,000.
</td></tr><tr><td>Offset</td><td>Specify the first item to return by index. The default is 1.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WasScan": {
                    "target": {
                        "webApp": {
                            "name": "",
                            "url": "",
                            "id": ""
                        },
                        "cancelOption": "",
                        "scannerAppliance": {
                            "type": ""
                        }
                    },
                    "launchedBy": {
                        "id": "",
                        "lastName": "",
                        "firstName": "",
                        "username": ""
                    },
                    "reference": "",
                    "multi": "",
                    "mode": "",
                    "id": "",
                    "profile": {
                        "id": "",
                        "name": ""
                    },
                    "status": "",
                    "launchedDate": "",
                    "type": "",
                    "name": "",
                    "summary": {
                        "resultsStatus": "",
                        "authStatus": ""
                    }
                }
            }
        ],
        "hasMoreRecords": "",
        "count": "",
        "responseCode": ""
    }
}</pre>
### operation: Get Scan Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan ID</td><td>Specify the scan ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WasScan": {
                    "target": {
                        "webApp": {
                            "name": "",
                            "url": "",
                            "id": ""
                        },
                        "cancelOption": "",
                        "scannerAppliance": {
                            "type": ""
                        }
                    },
                    "launchedBy": {
                        "id": "",
                        "lastName": "",
                        "firstName": "",
                        "username": ""
                    },
                    "sendMail": "",
                    "reference": "",
                    "multi": "",
                    "mode": "",
                    "id": "",
                    "profile": {
                        "id": "",
                        "name": ""
                    },
                    "status": "",
                    "launchedDate": "",
                    "type": "",
                    "enableWAFAuth": "",
                    "scanDuration": "",
                    "options": {
                        "count": "",
                        "list": [
                            {
                                "WasScanOption": {
                                    "value": "",
                                    "name": ""
                                }
                            }
                        ]
                    },
                    "name": "",
                    "summary": {
                        "nbRequests": "",
                        "resultsStatus": "",
                        "authStatus": "",
                        "linksCrawled": "",
                        "crawlDuration": "",
                        "os": "",
                        "testDuration": ""
                    }
                }
            }
        ],
        "count": "",
        "responseCode": ""
    }
}</pre>
### operation: Launch Scans
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan Name</td><td>Specify the scan name.
</td></tr><tr><td>Scan Type</td><td>Specify the scan type. You can choose from the following options: VULNERABILITY or DISCOVERY.
</td></tr><tr><td>Web App ID</td><td>Specify the ID of the web application to include it in the scan
</td></tr><tr><td>Target Web App Auth Record</td><td>Set this to true to use the default web application's authentication record for the scan.
</td></tr><tr><td>Target Scanner Appliance Type</td><td>Specify the type of scanner appliance used for the scan. You can choose from the following options: EXTERNAL or INTERNAL or scannerTags
</td></tr><tr><td>Scan Profile ID</td><td>Specify the name of the option profile that includes scan settings. This parameter is required unless the target has a default option profile.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WasScan": {
                    "id": ""
                }
            }
        ],
        "responseCode": "",
        "count": ""
    }
}</pre>
### operation: Retrieve Scan Status
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan ID</td><td>Specify the scan ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WasScan": {
                    "id": "",
                    "status": "",
                    "summary": {
                        "authStatus": "",
                        "resultsStatus": ""
                    }
                }
            }
        ],
        "responseCode": "",
        "count": ""
    }
}</pre>
### operation: Retrieve Scan Results
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan ID</td><td>Specify the scan ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WasScan": {
                    "sendMail": "",
                    "reference": "",
                    "endScanDate": "",
                    "sensitiveContents": {
                        "count": ""
                    },
                    "multi": "",
                    "stats": {
                        "byGroup": {
                            "count": ""
                        },
                        "byOwasp": {
                            "count": ""
                        },
                        "global": {
                            "nbVulnsLevel4": "",
                            "nbIgsLevel2": "",
                            "nbVulnsLevel2": "",
                            "nbScsLevel4": "",
                            "nbVulnsLevel1": "",
                            "nbVulnsLevel3": "",
                            "nbIgsTotal": "",
                            "nbIgsLevel4": "",
                            "nbScsLevel3": "",
                            "nbIgsLevel1": "",
                            "nbVulnsLevel5": "",
                            "nbScsLevel2": "",
                            "nbScsTotal": "",
                            "nbScsLevel5": "",
                            "nbIgsLevel5": "",
                            "nbScsLevel1": "",
                            "nbIgsLevel3": "",
                            "nbVulnsTotal": ""
                        },
                        "byWasc": {
                            "count": ""
                        }
                    },
                    "target": {
                        "cancelOption": "",
                        "webApp": {
                            "url": "",
                            "name": "",
                            "id": ""
                        },
                        "scannerAppliance": {
                            "type": ""
                        }
                    },
                    "igs": {
                        "count": "",
                        "list": [
                            {
                                "WasScanIg": {
                                    "qid": "",
                                    "data": {
                                        "base64": "",
                                        "value": ""
                                    },
                                    "title": ""
                                }
                            }
                        ]
                    },
                    "vulns": {
                        "count": ""
                    },
                    "id": "",
                    "launchedDate": "",
                    "enableWAFAuth": "",
                    "name": "",
                    "options": {
                        "count": "",
                        "list": [
                            {
                                "WasScanOption": {
                                    "value": "",
                                    "name": ""
                                }
                            }
                        ]
                    },
                    "status": "",
                    "scanDuration": "",
                    "launchedBy": {
                        "firstName": "",
                        "id": "",
                        "lastName": "",
                        "username": ""
                    },
                    "type": "",
                    "mode": "",
                    "summary": {
                        "nbRequests": "",
                        "linksCrawled": "",
                        "authStatus": "",
                        "crawlDuration": "",
                        "resultsStatus": "",
                        "os": "",
                        "testDuration": ""
                    },
                    "profile": {
                        "name": "",
                        "id": ""
                    }
                }
            }
        ],
        "responseCode": "",
        "count": ""
    }
}</pre>
### operation: Delete Scan
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Scan ID</td><td>Specify the scan ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WasScan": {
                    "id": ""
                }
            }
        ],
        "responseCode": "",
        "count": ""
    }
}</pre>
### operation: Count Web Applications
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>ID</td><td>Specify the Web application ID.
</td></tr><tr><td>Name</td><td>Specify the Web application name.
</td></tr><tr><td>URL</td><td>Specify the URL of web application.
</td></tr><tr><td>Tags ID</td><td>Specify the tag ID assigned to web application.
</td></tr><tr><td>Tags Name</td><td>Specify the tag name assigned to web application.
</td></tr><tr><td>Created Date</td><td>Specify the date and time to return all the web application which was created in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Updated Date</td><td>Specify the date and time to return all the web application which was last updated in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Scheduled</td><td>Set this to true to indicate that a scan is scheduled for web application.
</td></tr><tr><td>Scanned</td><td>Set this to true to indicate that the web application has been scanned.
</td></tr><tr><td>Last Scan Status</td><td>Specify the status of the last scan. You can choose from the following options: SUBMITTED, RUNNING, FINISHED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, ERROR or CANCELED
</td></tr><tr><td>Last Scan Date</td><td>Specify the date and time to return all the web application which was last scanned in WAS after specified date and time in UTC date/time format.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "count": "",
        "responseCode": ""
    }
}</pre>
### operation: Search Web Applications
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>ID</td><td>Specify the Web application ID.
</td></tr><tr><td>Name</td><td>Specify the Web application name.
</td></tr><tr><td>URL</td><td>Specify the URL of web application.
</td></tr><tr><td>Tags ID</td><td>Specify the tag ID assigned to web application.
</td></tr><tr><td>Tags Name</td><td>Specify the tag name assigned to web application.
</td></tr><tr><td>Created Date</td><td>Specify the date and time to return all the web application which was created in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Updated Date</td><td>Specify the date and time to return all the web application which was last updated in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Scheduled</td><td>Set this to true to indicate that a scan is scheduled for web application.
</td></tr><tr><td>Scanned</td><td>Set this to true to indicate that the web application has been scanned.
</td></tr><tr><td>Last Scan Status</td><td>Specify the status of the last scan. You can choose from the following options: SUBMITTED, RUNNING, FINISHED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, ERROR or CANCELED
</td></tr><tr><td>Last Scan Date</td><td>Specify the date and time to return all the web application which was last scanned in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Limit</td><td>Specify the total number of items to return. The default is 100. You can specify a value from 1 to 1,000.
</td></tr><tr><td>Offset</td><td>Specify the first item to return by index. The default is 1.
</td></tr><tr><td>Verbose</td><td>Set this to true to indicate whether the list of tags associated with the web application should be listed or not.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WebApp": {
                    "createdDate": "",
                    "name": "",
                    "updatedDate": "",
                    "tags": {
                        "count": ""
                    },
                    "url": "",
                    "owner": {
                        "id": ""
                    },
                    "id": ""
                }
            }
        ],
        "hasMoreRecords": "",
        "count": "",
        "responseCode": ""
    }
}</pre>
### operation: Get Web Application Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>App ID</td><td>Specify the Web application ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WebApp": {
                    "config": {},
                    "isScheduled": "",
                    "url": "",
                    "createdDate": "",
                    "createdBy": {
                        "firstName": "",
                        "id": "",
                        "lastName": "",
                        "username": ""
                    },
                    "updatedDate": "",
                    "defaultScanner": {
                        "type": ""
                    },
                    "owner": {
                        "firstName": "",
                        "id": "",
                        "lastName": "",
                        "username": ""
                    },
                    "postDataBlacklist": {
                        "count": ""
                    },
                    "dnsOverrides": {
                        "count": ""
                    },
                    "authRecords": {
                        "count": ""
                    },
                    "malwareMonitoring": "",
                    "urlBlacklist": {
                        "count": ""
                    },
                    "scope": "",
                    "name": "",
                    "useSitemap": "",
                    "malwareNotification": "",
                    "logoutRegexList": {
                        "count": ""
                    },
                    "id": "",
                    "useRobots": "",
                    "comments": {
                        "count": ""
                    },
                    "urlWhitelist": {
                        "count": ""
                    },
                    "crawlingScripts": {
                        "count": ""
                    },
                    "scannerLocked": "",
                    "tags": {
                        "count": ""
                    },
                    "updatedBy": {
                        "firstName": "",
                        "id": "",
                        "lastName": "",
                        "username": ""
                    },
                    "attributes": {
                        "count": ""
                    }
                }
            }
        ],
        "responseCode": "",
        "count": ""
    }
}</pre>
### operation: Create Web Application
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Web App Name</td><td>Specify the name of the web application.
</td></tr><tr><td>Web App URL</td><td>Specify the URL of the web application.
</td></tr><tr><td>Web App Auth Record ID</td><td>Specify the web app auth record ID of the web application.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WebApp": {
                    "createdDate": "",
                    "isScheduled": "",
                    "name": "",
                    "updatedDate": "",
                    "urlWhitelist": {
                        "count": ""
                    },
                    "tags": {
                        "count": ""
                    },
                    "crawlingScripts": {
                        "count": ""
                    },
                    "postDataBlacklist": {
                        "count": ""
                    },
                    "comments": {
                        "count": ""
                    },
                    "config": {},
                    "updatedBy": {
                        "id": "",
                        "lastName": "",
                        "firstName": "",
                        "username": ""
                    },
                    "malwareMonitoring": "",
                    "logoutRegexList": {
                        "count": ""
                    },
                    "url": "",
                    "attributes": {
                        "count": ""
                    },
                    "createdBy": {
                        "id": "",
                        "lastName": "",
                        "firstName": "",
                        "username": ""
                    },
                    "owner": {
                        "id": "",
                        "lastName": "",
                        "firstName": "",
                        "username": ""
                    },
                    "scope": "",
                    "useSitemap": "",
                    "malwareNotification": "",
                    "defaultScanner": {
                        "type": ""
                    },
                    "id": "",
                    "useRobots": "",
                    "authRecords": {
                        "count": "",
                        "list": [
                            {
                                "WebAppAuthRecord": {
                                    "id": "",
                                    "name": ""
                                }
                            }
                        ]
                    },
                    "dnsOverrides": {
                        "count": ""
                    },
                    "scannerLocked": "",
                    "urlBlacklist": {
                        "count": ""
                    }
                }
            }
        ],
        "count": "",
        "responseCode": ""
    }
}</pre>
### operation: Delete Web Applications
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>App ID</td><td>Specify the Web application ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "ServiceResponse": {
        "data": [
            {
                "WebApp": {
                    "id": ""
                }
            }
        ],
        "count": "",
        "responseCode": ""
    }
}</pre>
### operation: Search Reports
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>ID</td><td>Specify the report ID.
</td></tr><tr><td>Name</td><td>Specify the report name.
</td></tr><tr><td>Tags ID</td><td>Specify the ID of the tag associated with the report.
</td></tr><tr><td>Tags Name</td><td>Specify the name of the tag associated with the report.
</td></tr><tr><td>Creation Date</td><td>Specify the date and time to return all the report which was created after specified date and time in UTC date/time format.
</td></tr><tr><td>Type</td><td>Specify the report type. You can choose from the following options: WAS_SCAN_REPORT, WAS_WEBAPP_REPORT, WAS_SCORECARD_REPORT, WAS_CATALOG_REPORT or DATALIST_REPORT
</td></tr><tr><td>Format</td><td>Specify the format of the report. You can choose from the following options: HTML_ZIPPED, HTML_BASE64, PDF, PDF_ENCRYPTED, POWERPOINT, CSV, CSV_V2, XML or WORD
</td></tr><tr><td>Status</td><td>Specify the status of the report. You can choose from the following options: RUNNING, ERROR or COMPLETE
</td></tr><tr><td>Limit</td><td>Specify the total number of items to return. The default is 100. You can specify a value from 1 to 1,000.
</td></tr><tr><td>Offset</td><td>Specify the first item to return by index. The default is 1.
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Download Report
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Report ID</td><td>Specify the Report ID.
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Search Option Profiles
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>ID</td><td>Specify the option profile ID.
</td></tr><tr><td>Name</td><td>Specify the option profile name.
</td></tr><tr><td>Tags ID</td><td>Specify the ID of the tag associated with the option profile.
</td></tr><tr><td>Tags Name</td><td>Specify the name of the tag associated with the option profile.
</td></tr><tr><td>Created Date</td><td>Specify the date and time to return all the option profile which was created in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Updated Date</td><td>Specify the date and time to return all the option profile which was last updated in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Used By Web Apps</td><td>Web applications used/not used by the option profile.
</td></tr><tr><td>Used By Schedules</td><td>Scan schedules used/not used by the option profile.
</td></tr><tr><td>Owner ID</td><td>Specify the ID of the owner who created the option profile
</td></tr><tr><td>Owner Name</td><td>Specify the full name of the user who created the option profile.
</td></tr><tr><td>Owner Username</td><td>Specify the username of the owner who created the option profile.
</td></tr><tr><td>Limit</td><td>Specify the total number of items to return. The default is 100. You can specify a value from 1 to 1,000.
</td></tr><tr><td>Offset</td><td>Specify the first item to return by index. The default is 1.
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Search Schedule
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>ID</td><td>Specify the schedule ID.
</td></tr><tr><td>Name</td><td>Specify the user-defined schedule name.
</td></tr><tr><td>Owner ID</td><td>Specify the ID associated with the owner who created the schedule.
</td></tr><tr><td>Created Date</td><td>Specify the date and time to return all the schedule which was created in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Updated Date</td><td>Specify the date and time to return all the schedule which was last updated in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Active</td><td>Set this to true to indicate whether the schedule is active.
</td></tr><tr><td>Type</td><td>Specify the scheduled scan type. You can choose from the following options: VULNERABILITY or DISCOVERY.
</td></tr><tr><td>Web App Name</td><td>Specify the name of the web application being scanned.
</td></tr><tr><td>Web App ID</td><td>Specify the ID of the web application being scanned.
</td></tr><tr><td>Web App Tag ID</td><td>Specify the ID of the tag applied to the web application being scanned.
</td></tr><tr><td>Last Scan Status</td><td>Specify the status of the last scan. You can choose from the following options: SUBMITTED, RUNNING, FINISHED, TIME_LIMIT_EXCEEDED, SCAN_NOT_LAUNCHED, SCANNER_NOT_AVAILABLE, ERROR or CANCELED
</td></tr><tr><td>Last Scan Launch Date</td><td>Specify the date and time to return all the web application which was last scanned in WAS after specified date and time in UTC date/time format.
</td></tr><tr><td>Multi</td><td>Set this to true to indicate the scheduled scan is multiple scan.
</td></tr><tr><td>Limit</td><td>Specify the total number of items to return. The default is 100. You can specify a value from 1 to 1,000.
</td></tr><tr><td>Offset</td><td>Specify the first item to return by index. The default is 1.
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Get Schedule Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Schedule ID</td><td>Specify the schedule ID.
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
## Included playbooks
The `Sample - qualys-web-application-scanner - 2.0.0` playbook collection comes bundled with the Qualys Web Application Scanning(WAS) connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR&trade; after importing the Qualys Web Application Scanning(WAS) connector.

- Count Web Applications
- Create Web Application
- Delete Scan
- Delete Web Applications
- Download Report
- Get Scan Count
- Get Scan Details
- Get Schedule Details
- Get Web Application Details
- Launch Scans
- Retrieve Scan Results
- Retrieve Scan Status
- Search Option Profiles
- Search Reports
- Search Scans
- Search Schedule
- Search Web Applications

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection since the sample playbook collection gets deleted during connector upgrade and delete.
