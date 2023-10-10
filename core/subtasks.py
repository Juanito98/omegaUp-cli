import os
import re


def infer_number_subtask_from_statements(problem_dir: str) -> int:
    # Read the statements
    with open(os.path.join(problem_dir, "statements/es.markdown"), "r") as f:
        lines = f.read()
    # Count the number of subtasks
    reg = re.compile(r"[^\n\w]*[Ss]ubtarea \d+")
    return len(reg.findall(lines))
