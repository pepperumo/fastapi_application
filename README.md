

## Project Structure

- **`main.py`** — The FastAPI application code.
- **`requirements.txt`** — Python dependencies.
- **`test_api.sh`** — A shell script with `curl` commands for testing.
- **`ARCHITECTURE.md`** — High-level explanation of the project.
- **`README.md`** — Project instructions and documentation (this file).

---

## Installation & Setup

1. **Clone** or **Download** this repository.

2. **Create and activate** a virtual environment (recommended):
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
   *(On Windows: `env\Scripts\activate`)*

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Verify Python version**:
   ```bash
   python --version
   ```
   Make sure it’s Python 3.9 or above.

---

## Running the Application

Use **Uvicorn** to start the server:

```bash
uvicorn main:app --reload
```

By default, it will listen on [http://127.0.0.1:8000](http://127.0.0.1:8000).  

### Interactive Docs

FastAPI automatically provides a Swagger UI at:
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Testing with `test_api.sh`

We’ve provided a simple script that calls the endpoints using `curl`.  

1. **Make the file executable** (only needed once):
   ```bash
   chmod +x test_api.sh
   ```
2. **Run**:
   ```bash
   ./test_api.sh
   ```
3. **Observe** the responses. You should see:
   - A successful health check (HTTP `200`).
   - Successful question retrieval.
   - A `403 Forbidden` when using a wrong admin password.
   - A `200` success when using the correct admin password (`4dM1n`).

---

## Usage & Endpoints

1. **Basic Auth**  
   - In-memory user database in `main.py`:  
     ```python
     users_db = {
         "alice": "wonderland",
         "bob": "builder",
         "clementine": "mandarine"
     }
     ```
   - You must supply valid credentials (e.g., `alice:wonderland`) to access protected endpoints.

2. **Health Check**  
   - **`GET /health`**  
   - Returns `{"status":"OK","message":"The API is functional."}` if the server is running.

3. **Get Questions**  
   - **`GET /questions`**  
   - Parameters:
     - `use` (e.g., `general`, `school`)
     - `subject` (e.g., `Geography`, `Math`, etc.)
     - `number_of_questions` (integer, typically `5`, `10`, or `20`)
   - Requires Basic Auth (username:password).  
   - Returns a JSON list of MCQs that match your filters, randomly ordered.

4. **Create a Question**  
   - **`POST /questions`**  
   - Payload body follows the `Question` Pydantic model:
     ```json
     {
       "question": "Your question here?",
       "subject": "SomeSubject",
       "correct": ["A"],
       "use": "TestUse",
       "answerA": "Answer A",
       "answerB": "Answer B",
       "answerC": "Answer C",
       "answerD": "Answer D"
     }
     ```
   - **Admin Password**: Add `?admin_password=4dM1n` to your request URL.  
   - Also requires Basic Auth from one of the `users_db` entries.

Example `curl` request:
```bash
curl -X POST -u alice:wonderland \
  -H "Content-Type: application/json" \
  -d '{
    "question": "A new question?",
    "subject": "TestSubject",
    "correct": ["A"],
    "use": "TestUse",
    "answerA": "Answer A",
    "answerB": "Answer B",
    "answerC": "Answer C",
    "answerD": "Answer D"
  }' \
  "http://localhost:8000/questions?admin_password=4dM1n"
```

---

## Contributing

1. Fork the project & create a feature branch.
2. Submit a Pull Request describing your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

```

---

### How to use this `README.md`
- Simply **copy and paste** the Markdown text above into a `README.md` file in your repository.
- Adjust the details (ports, Python version, dependencies, etc.) as appropriate to your project.
