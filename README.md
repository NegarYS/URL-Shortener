# 📘 README - Midterm Final Checklist
 
 --- 
 
## 1. API Test Coverage Table 

 
| # | API Endpoint / Feature | Implemented & Tested By (Student Name) | 
|---|------------------------|-----------------------------------------| 
| 1 | Create Short Link - POST /links | Negar | 
| 2 | Redirect to Original URL - GET /{code} | Negar | 
| 3 | Get All Shortened Links - GET /links | Tina | 
| 4 | Delete Short Link - DELETE /links/{code} | Tina | 
 --- 
 
## 2. Code Generation Method (Section 6.4) 
 
Check the method you used to generate the short code: 
- [x] **1. Random Generation**
- [ ] **2. ID → Base62 Conversion**
- [ ] **3. Hash-based Generation**


 
(Only select the one you actually implemented.) 
 --- 
 
## 3. Bonus User Story: TTL (Expiration Time) for Shortened Links) 
 
If you implemented the bonus user story, mark the box and complete the 
required details. 
 - [x] TTL Feature Implemented 
 
If checked, fill in the following information: 
 - ENV variable or config key used:  
 APP_TTL_HOURS=24 
 
You must also ensure this key exists in .env.example with a sample value. 
 
 - Location of TTL Logic (File + Function):  
 
Specify the exact location where TTL expiration is checked and expired 
links are detected/removed. 

File: `app/repositories/link_repository.py`
Function: `is_expired(short_code: str) -> bool `
Description: `Checks if a link's expires_at timestamp has passed.`

Expired Link Deletion
File: `app/repositories/link_repository.py`
Function: `delete_expired_links() -> int`
Description: `Deletes all links where expires_at < current_time.`

Scheduled Cleanup
File: `app/scheduler.py`
Function: `TTLScheduler._run_cleanup()`
Description: `Automatically calls delete_expired_links() every hour when TTL is enabled.`

TTL Configuration
File: `app/config.py`
Variable: `APP_TTL_HOURS`
Description: `Sets TTL duration in hours (0 = disabled).`

Main Flow:
`TTLScheduler (hourly) → cleanup_expired_links() → LinkRepository.delete_expired_links()`


 - How TTL cleanup is triggered:  

Full file path of the command
app/commands/cleanup.py

Command name / execution method
Command: cleanup_expired_links()
Execution: python -m app.commands.cleanup (manually) or called by scheduler automatically

Scheduler details
File: app/scheduler.py
Scheduler: TTLScheduler runs every hour when TTL is enabled
Logic: Compares expires_at field with current time and deletes expired links
 
## 4. Postman Collection (Required) 
 
A Postman Collection has been created and includes all four API routes: 
 - POST /links - GET /{code} - GET /links - DELETE /links/{code} 
 
### Screenshots (included in GitHub) 
 
For each route, two screenshots have been added: 
 - Successful response (2xx)  - Error-handled response (4xx) 
 
Screenshots are located in: 
 
          
   /postman 
    
 
 
 
### Naming Example: 
 
 
postman/ 
post-links-201-success.png 
post-links-400-invalid-url.png 
get-code-302-redirect.png 
get-code-404-bad-request.png 
get-links-200-success.png 
delete-code-200-success.png 
delete-code-404-not-found.png 
15 
 
Filenames must clearly show: - Route  - HTTP status  - Success or error  --- 

✔️
 Make sure this README is fully completed before submission.

