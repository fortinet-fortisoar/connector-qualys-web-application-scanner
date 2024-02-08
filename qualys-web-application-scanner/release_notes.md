#### What's Improved

- Fixed the 'JSON payload sent in the requests'.
- Updated the following action names:
    - Retrieve Scan Results > Get Scan Results
    - Retrieve Scan Status > Get Scan Status
    - Count Web Applications > Get Web Applications Count
- Added the following actions and playbooks: 
    - Search Reports
    - Download Report
    - Search Schedule 
    - Get Schedule Details
    - Search Option Profiles
    - Search Tags
    - Create Tag
    - Update Tag
    - Delete Tag
    - Search Users
- In action "Get Scan Count":
  - The type of input parameter "Scan ID", "Web App ID", "Web App Tag ID" is changed to text from integer.
  - The type of input parameter "Type", "Mode", "Status", "Authentication Status", "Result Status" is changed to multiselect from select.
  - The options "CANCELING", "ERROR", "CANCELED_WITH_RESULTS" are added and "CANCELING ERROR" is removed from the input parameter "Result Status".

- In action "Search Scans":
  - Renamed the input parameter "Web App Rag ID" to "Web App Tag ID".
  - The type of input parameter "Scan ID", "Web App ID", "Web App Tag ID" is changed to text from integer.
  - The type of input parameter "Type", "Mode", "Status", "Authentication Status", "Result Status" is changed to multiselect from select.
  - The options "CANCELING", "ERROR", "CANCELED_WITH_RESULTS" are added and "CANCELING ERROR" is removed from the input parameter "Result Status".
  - Input parameters "Limit" and "Offset" are added.

- In action "Launch Scans":
  - The type of input parameter "Scan Type", "Target Scanner Appliance Type" is changed to multiselect from select.

- In action "Get Web Applications Count":
  - The type of input parameter "ID", is changed to text from integer.
  - Input parameters "Tags ID", "Tags Name", "Created Date", "Updated Date", "Last Scan Status", "Last Scan Date" are added.

- In action "Search Web Applications":
  - Renamed the input parameter "Scan ID" to "ID", "Scan Name" to "Name".
  - The type of input parameter "ID", "Tags ID", "Tags Name" is changed to text from integer.
  - Input parameters "Scheduled", "Scanned", "Last Scan Status", "Last Scan Date", "Limit", "Offset", "Verbose" are added.

- In action "Get Web Application Details":
  - Renamed the input parameter "Scan ID" to "App ID".

- In action "Delete Web Applications":
  - Updated output schema.