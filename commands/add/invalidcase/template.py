files = [
    {
        "path": """tests/invalid-cases/{case_name}.in""",
        "content": """{invalid_case}""",
    },
    {
        "path": """tests/invalid-cases/{case_name}.out""",
        "content": "",
    },
    {
        "path": """tests/invalid-cases/{case_name}.expected-failure""",
        "content": "{expected_failure}",
    },
]
