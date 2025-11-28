from z3 import *

def to_z3(node, variables):
    if isinstance(node, str):
        return variables[node]
    
    if isinstance(node, (int, float)):
        return node
    
    op, left, right = node
    left_z3 = to_z3(left, variables)
    right_z3 = to_z3(right, variables)

    if op == '+':
        return left_z3 + right_z3
    elif op == '-':
        return left_z3 - right_z3
    elif op == '*':
        return left_z3 * right_z3
    elif op == '/':
        return left_z3 / right_z3
    
    raise ValueError(f"Unknown operation: {op}")


# Example usage
# (x * 3) + (10 - y/2) = 20
tree = ('+', ('*', 'x', 3), ('-', 10, ('/', 'y', 2)))

variables = {
    'x': Real('x'),
    'y': Real('y')
}

expr = to_z3(tree, variables)

solver = Solver()
solver.add(expr == 20)
solver.add(variables['x'] >= 0)
solver.add(variables['y'] >= 0)

if solver.check() == sat:
    model = solver.model()
    print("Solution found:")
    for var in variables:
        print(f"{var} = {model[variables[var]]}")
else:
    print("No solution exists.")