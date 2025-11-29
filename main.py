import json
import argparse
from z3 import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run z3 solver with a config file.")
    parser.add_argument("--config", default="config.json", help="Path to the configuration file")
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{args.config}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{args.config}'.")
        exit(1)

    variables = {name: Real(name) for name in config.get("variables", [])}
    solver = Solver()

    for formula_str in config.get("formulas", []):
        try:
            constraint = eval(formula_str, {}, variables)
            solver.add(constraint)
        except Exception as e:
            print(f"Error processing formula '{formula_str}': {e}")
            exit(1)

    if solver.check() == sat:
        model = solver.model()
        print("Solution found:")
        for var_name in variables:
            print(f"{var_name} = {model[variables[var_name]]}")
    else:
        print("No solution exists.")