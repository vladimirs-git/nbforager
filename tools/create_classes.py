"""Create classes."""

text = """
        self.data_files = self.core.data_files
        self.data_sources = self.core.data_sources
        self.jobs = self.core.jobs
"""

class_names = []
for line in text.splitlines():
    line = line.strip()
    if not line:
        continue
    line = line.split()[0]
    line = line.split(".")[-1]
    class_name = "".join([f"{s.capitalize()}" for s in line.split("_")]) + "F"
    class_names.append(class_name)
    class_line = f"self.{line} = self.{class_name}(self)"
    print(class_line)
    x = 1

print("\n\n\n")

for line in class_names:
    line = line.strip()
    if not line:
        continue
    class_ = f"    class {line}(Forager):\n        \"\"\"{line}.\"\"\"\n\n"
    print(class_)
