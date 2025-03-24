import csv

def parse_vars_no_units(vars_str):
    """
    Parses a string like: "v0:10, a:2, t:5"
    into a dictionary: {"v0": 10.0, "a": 2.0, "t": 5.0}
    """
    # Example input: "v0:10, a:2, t:5"
    # We'll split by commas, then split each chunk by ':'
    results = {}
    if not vars_str.strip():
        return results  # empty or blank

    chunks = vars_str.split(',')
    for chunk in chunks:
        chunk = chunk.strip()        # e.g. "v0:10"
        if not chunk:
            continue
        pair = chunk.split(':', 1)   # split once at ':'
        if len(pair) < 2:
            continue
        key = pair[0].strip()       # "v0"
        val_str = pair[1].strip()   # "10"
        try:
            val_float = float(val_str)
        except ValueError:
            # Not a float; skip or handle differently
            continue
        results[key] = val_float
    return results

def main(csv_path):
    with open(csv_path, mode='r', encoding='utf-8') as f:
        # The CSV has these headers:
        # Level US;Level FR;Question;Variables;Variables (no units);Formula;Test Answer;Numeric answer;Units 1;Solve function
        # We'll parse with delimiter=';'
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            question_text = row["Question"]
            function_code = row["Solve function"]
            variables_no_units = row["Variables (no units)"]

            print(f"\n=== Solving question: {question_text} ===")

            # 1) Execute the solve function code
            local_env = {}
            global_env = {}
            # Wrap the exec in try/except to handle code issues
            try:
                # function_code is something like:
                # "def solve(v0;a;t): dist=v0*t+0.5*a*(t**2);return f'{dist} m'"
                exec(function_code, global_env, local_env)
            except Exception as e:
                print("Error executing function code:", e)
                continue
            
            # 2) Retrieve the newly defined solve(...) from local_env
            solve_func = local_env.get("solve", None)
            if solve_func is None:
                print("No solve() function found in this row.")
                continue

            # 3) Parse the numeric variables from "Variables (no units)" column
            parsed_vars = parse_vars_no_units(variables_no_units)
            
            # 4) Call solve(...) with the parsed variables
            #    We'll pass them as keyword arguments. If the param names match, this works.
            try:
                result = solve_func(**parsed_vars)
                print("Result =>", result)
            except TypeError as e:
                print("Error calling solve() with parsed variables:", e)
            except Exception as e:
                print("Unexpected error in solve():", e)

if __name__ == "__main__":
    # Example usage:
    # python auto_solve.py path/to/your_csv.csv
    import sys
    if len(sys.argv) < 2:
        print("Usage: python auto_solve.py <csv_file_path>")
    else:
        csv_path = sys.argv[1]
        main(csv_path)
