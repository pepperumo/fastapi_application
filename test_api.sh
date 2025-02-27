#!/bin/bash

echo "=== Health check ==="
curl -i http://localhost:8000/health
echo ""

echo "=== Get 5 questions (fail if none) ==="
curl -i -u alice:wonderland \
  "http://localhost:8000/questions?use=general&subject=Geography&number_of_questions=5"
echo ""

echo "=== Attempt to create a question with invalid admin password ==="
curl -i -X POST -u bob:builder \
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
  "http://localhost:8000/questions?admin_password=wrongPW"
echo ""

echo "=== Create a question with correct admin password ==="
curl -i -X POST -u bob:builder \
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
echo ""
