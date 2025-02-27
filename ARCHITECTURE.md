# MCQ API Architecture

## Overview
We built a simple MCQ (Multiple-Choice Question) API in Python using the FastAPI framework. The API allows:
- Basic user authentication (via HTTP Basic Auth) to access questions.
- Admin-level creation of questions using a special admin password ("4dM1n").

## Data Storage
- For simplicity, we store MCQs in a Python list named 'mcq_data'. 
- Each MCQ is represented by a Pydantic model 'Question', which enforces schema validation.

## Endpoints
1. **GET /health**: Returns a basic JSON indicating the API is operational.
2. **GET /questions**: 
   - Requires a valid username:password from the 'users_db'.
   - Takes URL query parameters for 'use' (type of MCQ), 'subject' (category), and 'number_of_questions' (5, 10, or 20, etc.).
   - Randomly shuffles questions matching those filters and returns a subset.
3. **POST /questions**:
   - Also requires Basic Auth credentials plus an admin_password query parameter.
   - Only the correct admin password '4dM1n' allows creation of a new MCQ record.
   - Appends the new question to the in-memory 'mcq_data'.

## Authentication
- We utilize FastAPI's HTTPBasic for user authentication.
- The function 'get_current_username' checks the 'users_db' dictionary to confirm valid credentials.
- Admin functionality is unlocked if the query parameter 'admin_password' matches the known admin password '4dM1n'.

## Error Handling
- If credentials are invalid, the API returns 401 status with a descriptive error.
- If the requested number of questions is invalid (like <= 0), the API returns 400.
- If no questions match filters, the API returns 404.
- If an admin password is incorrect, the API returns 403.

## Security Notice
- In a real-world scenario, we would not store plaintext passwords in a dictionary. We would use hashed/salted passwords in a secure database, and we would require TLS for communication. For this exercise, the focus is on basic FastAPI usage and demonstration.

## Future Extensions
- You could add a real database (SQL or NoSQL) for persistent storage of questions.
- Extend the user model to handle roles (e.g., admin vs. normal user).
- Add more robust logging, monitoring, and stricter error handling.

