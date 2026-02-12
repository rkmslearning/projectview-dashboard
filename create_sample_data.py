import pandas as pd
from pathlib import Path

# Create data directory if it doesn't exist
Path("data").mkdir(exist_ok=True)

# Sample project data
data = {
    "Project ID": [
        "PRJ-001",
        "PRJ-002",
        "PRJ-003",
        "PRJ-004",
        "PRJ-005",
        "PRJ-006",
        "PRJ-007",
        "PRJ-008",
    ],
    "Project Name": [
        "Website Redesign",
        "Mobile App Development",
        "Database Migration",
        "Cloud Infrastructure",
        "CRM Integration",
        "Security Audit",
        "API Development",
        "Data Analytics Platform",
    ],
    "Status": [
        "In Progress",
        "Completed",
        "In Progress",
        "Pending",
        "In Progress",
        "Completed",
        "Pending",
        "In Progress",
    ],
    "Owner": [
        "John Smith",
        "Sarah Johnson",
        "Mike Chen",
        "Emily Davis",
        "Robert Wilson",
        "Lisa Anderson",
        "David Lee",
        "Jennifer Brown",
    ],
    "Start Date": [
        "2026-01-15",
        "2025-11-01",
        "2026-01-20",
        "2026-02-01",
        "2025-12-15",
        "2025-10-01",
        "2026-02-10",
        "2026-01-05",
    ],
    "End Date": [
        "2026-03-15",
        "2026-01-31",
        "2026-04-30",
        "2026-05-30",
        "2026-03-30",
        "2026-01-15",
        "2026-06-30",
        "2026-05-15",
    ],
    "Progress (%)": [65, 100, 45, 0, 80, 100, 10, 55],
    "Budget ($)": [150000, 200000, 180000, 250000, 120000, 80000, 160000, 300000],
    "Priority": ["High", "Medium", "High", "Low", "High", "Medium", "Medium", "High"],
    "Team Size": [5, 8, 6, 10, 4, 3, 7, 9],
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = "data/project_data.xlsx"
df.to_excel(output_file, index=False, sheet_name="Projects")

print(f"✅ Excel file created: {output_file}")
print(f"📊 Total records: {len(df)}")
print(f'📝 Columns: {", ".join(df.columns)}')
