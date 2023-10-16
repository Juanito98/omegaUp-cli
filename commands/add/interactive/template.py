files = [
    {
        "path": """interactive/Main.cpp""",
        "content": """#include <iostream>

#include "{module_name}.h"

{subtasks}""",
    },
    {
        "path": """interactive/Main.distrib.cpp""",
        "content": """#include <iostream>

#include "{module_name}.h"

int main() {{
  // TODO: Implementar
  return 0;
}}
""",
    },
    {
        "path": """interactive/{module_name}.idl""",
        "content": """interface Main {{
}};

interface {module_name} {{
}};
""",
    },
]


symlinks = [
    {
        "src": "examples",
        "dst": "interactive/examples",
    },
]


subcase_main = """const int NUM_SUB = {num_sub};
int getSubtask(const std::string& caseName) {{
  for (int sub = 1; sub <= NUM_SUB; ++sub) {{
    if (caseName.find("sub" + std::to_string(sub)) != std::string::npos) {{
      return sub;
    }}
  }}
  return -1;
}}

int main(int argc, char* argv[]) {{
  // Obtenemos el nombre del caso
  std::string caseName = argv[1];
  int subtask = getSubtask(caseName);

  // TODO: Implementar

  return 0;
}}
"""


no_subcase_main = """int main() {
  // TODO: Implementar
  return 0;
}"""


settings_json_dict = {
    "validator": {
        "name": "token-caseless",
        "limits": {
            "TimeLimit": 1000
        }
    },
    "interactive": {
        "ModuleName": "{module_name}",
        "ParentLang": "cpp17-gcc"
    },
}
