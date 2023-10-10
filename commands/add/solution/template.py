files = [
    {
        "path": """solutions/{case_name}""",
        "content": """{case_template}""",
    },
]

official_solution_files = [
    {
        "path": """.gitignore""",
        "content": """**/*.out
!tests/invalid-cases/*.out
""",
    },
]

cpp_template = """#include <iostream>

int main() {
    // TODO: Implement solution
    return 0;
}
"""
