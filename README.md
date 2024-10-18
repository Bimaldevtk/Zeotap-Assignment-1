# Rule Engine API

This is a simple Rule Engine API built with FastAPI. It allows users to create, combine, evaluate, and modify rules using a simple rule syntax.

## Features

- Create rules and get the corresponding Abstract Syntax Tree (AST).
- Combine multiple rules into a single AST.
- Evaluate rules against provided data.
- Modify existing rules.
- Validation of attributes to ensure only allowed attributes are used in rules.

## Requirements

- Python 3.7 or higher
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/repo-name.git
   cd repo-name
Create a virtual environment (optional but recommended):

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:

bash

    pip install fastapi uvicorn

Running the Application

Start the FastAPI server using Uvicorn:

bash

uvicorn main:app --reload

The API will be accessible at http://127.0.0.1:8000.
API Endpoints
1. Create Rule

    Endpoint: POST /create_rule/

    Request Body:

    json

{
  "rule_string": "age > 30 and department == 'Sales'"
}

Response:

json

    {
      "AST": "Your AST representation"
    }

2. Combine Rules

    Endpoint: POST /combine_rules/

    Request Body:

    json

[
  "age > 30",
  "department == 'Sales'"
]

Response:

json

    {
      "CombinedAST": "Your Combined AST representation"
    }

3. Evaluate Rule

    Endpoint: POST /evaluate_rule/

    Request Body:

    json

{
  "rule_string": "age > 30 and department == 'Sales'",
  "data": {
    "age": 35,
    "department": "Sales"
  }
}

Response:

json

    {
      "result": true
    }

4. Modify Rule

    Endpoint: PUT /modify_rule/

    Request Body:

    json

{
  "original_rule": "age > 30",
  "modified_rule": "age >= 30"
}

Response:

json

{
  "message": "Rule modified successfully",
  "AST": "Your modified AST representation"
}
