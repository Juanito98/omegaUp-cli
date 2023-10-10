files = [
    {
        "path": "tests/{validator}",
        "content": """import re
import sys
import unittest
from omegaup.validator import validatortest


class Test(unittest.TestCase):
    def test(self):
        with open("data.in", "r") as handle:
            original_input = handle.read()

        lines = original_input.split("\\n")
        self.assertEqual(lines[-1], "", "unexpected trailing characters")
        lines.pop()

        # TODO: Validate input
        reg = re.compile(r'')

        caseName = sys.argv[1]
        {subtasks}


if __name__ == '__main__':
    validatortest.main()
""",
    },
    {
        "path": "tests/invalid-cases/sin-salto-de-linea.in",
        "content": """0""",
    },
    {
        "path": "tests/invalid-cases/sin-salto-de-linea.out",
        "content": "",
    },
    {
        "path": "tests/invalid-cases/sin-salto-de-linea.expected-failure",
        "content": "unexpected trailing characters",
    },
]
