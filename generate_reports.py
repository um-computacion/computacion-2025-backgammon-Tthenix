import os
def read_file(filepath):
    if not os.path.exists(filepath):
        return f"Error: Report file not found at {filepath}"
    with open(filepath, "r") as f:
        return f.read()
coverage_report = read_file("coverage_report.txt")
pylint_report = read_file("pylint_report.txt")
reports_content = f"""# Automated Reports
## Coverage Report
```text
{coverage_report}
```
## Pylint Report
```text
{pylint_report}
```
"""
with open("REPORTS.md", "w") as f:
    f.write(reports_content)
