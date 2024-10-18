from fastapi import FastAPI, HTTPException, Body
from typing import List, Dict
import ast
import operator

app = FastAPI()

# In-memory storage for rules
rules_db = {}

# Helper function to parse a rule string into AST nodes
def parse_rule(rule_str: str):
    try:
        tree = ast.parse(rule_str, mode='eval')
        return tree
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Invalid rule syntax")

# A safer way to evaluate simple expressions using Python's operator module
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.And: operator.and_,
    ast.Or: operator.or_,
    ast.Gt: operator.gt,
    ast.Lt: operator.lt,
    ast.GtE: operator.ge,
    ast.LtE: operator.le,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}

# Function to evaluate an AST expression node safely
def safe_eval(node, data):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body, data)
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left, data)
        right = safe_eval(node.right, data)
        return SAFE_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(safe_eval(value, data) for value in node.values)
        elif isinstance(node.op, ast.Or):
            return any(safe_eval(value, data) for value in node.values)
    elif isinstance(node, ast.Compare):
        left = safe_eval(node.left, data)
        right = safe_eval(node.comparators[0], data)
        return SAFE_OPERATORS[type(node.ops[0])](left, right)
    elif isinstance(node, ast.Name):
        return data[node.id]
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        raise ValueError("Unsupported expression")

# API 1: Create Rule (returns an AST node)
@app.post("/create_rule/")
def create_rule(rule: Dict[str, str] = Body(...)):  # Use Body to accept JSON
    rule_string = rule.get("rule_string")  # Get the rule_string from the body
    if not rule_string:
        raise HTTPException(status_code=400, detail="rule_string is required")
    rule_ast = parse_rule(rule_string)
    return {"AST": ast.dump(rule_ast)}

# API 2: Combine multiple rules into a single AST
@app.post("/combine_rules/")
def combine_rules(rule_strings: List[str] = Body(...)):  # Use Body to accept JSON
    combined_ast = None
    for rule in rule_strings:
        rule_ast = parse_rule(rule)
        if combined_ast is None:
            combined_ast = rule_ast
        else:
            combined_ast = ast.BoolOp(op=ast.Or(), values=[combined_ast.body, rule_ast.body])
    return {"CombinedAST": ast.dump(combined_ast)}

# API 3: Evaluate Rule
@app.post("/evaluate_rule/")
def evaluate_rule(ast_json: Dict = Body(...)):
    try:
        rule_string = ast_json["rule_string"]
        data = ast_json["data"]
        rule_ast = parse_rule(rule_string)
        result = safe_eval(rule_ast, data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Optional: Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Rule Engine API"}
