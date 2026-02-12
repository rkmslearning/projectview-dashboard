import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import random

# Create data directory if it doesn't exist
Path("data").mkdir(exist_ok=True)

# Sample inventory data with completely different structure
data = {
    "SKU": [
        "INV-1001",
        "INV-1002",
        "INV-1003",
        "INV-1004",
        "INV-1005",
        "INV-1006",
        "INV-1007",
        "INV-1008",
        "INV-1009",
        "INV-1010",
    ],
    "Product Name": [
        "Wireless Mouse",
        "Mechanical Keyboard",
        "USB-C Cable",
        "Laptop Stand",
        "Webcam HD",
        "Bluetooth Headset",
        "External SSD 1TB",
        "Monitor 27 inch",
        "Docking Station",
        "Ergonomic Chair",
    ],
    "Category": [
        "Electronics",
        "Electronics",
        "Accessories",
        "Furniture",
        "Electronics",
        "Electronics",
        "Storage",
        "Electronics",
        "Accessories",
        "Furniture",
    ],
    "Quantity in Stock": [150, 85, 320, 45, 120, 95, 60, 30, 55, 25],
    "Reorder Level": [50, 30, 100, 20, 40, 35, 25, 15, 20, 10],
    "Unit Price": [
        29.99,
        89.99,
        12.99,
        149.99,
        79.99,
        59.99,
        129.99,
        399.99,
        189.99,
        599.99,
    ],
    "Supplier": [
        "TechCorp",
        "KeyMaster Inc",
        "CableWorks",
        "OfficeMax",
        "VisionTech",
        "AudioPro",
        "DataStore",
        "DisplayCo",
        "ConnectHub",
        "ComfortPlus",
    ],
    "Stock Status": [
        "In Stock",
        "In Stock",
        "In Stock",
        "Low Stock",
        "In Stock",
        "In Stock",
        "In Stock",
        "Low Stock",
        "In Stock",
        "Critical",
    ],
    "Last Restocked": [
        "2026-01-15",
        "2026-02-01",
        "2026-01-28",
        "2025-12-10",
        "2026-01-20",
        "2026-02-05",
        "2026-01-25",
        "2025-11-15",
        "2026-02-08",
        "2025-10-20",
    ],
    "Warehouse Location": [
        "A-12",
        "A-15",
        "B-03",
        "C-08",
        "A-18",
        "A-20",
        "B-11",
        "C-15",
        "B-05",
        "D-02",
    ],
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = "data/inventory_data.xlsx"
df.to_excel(output_file, index=False, sheet_name="Inventory")

print(f"✅ Inventory Excel file created: {output_file}")
print(f"📊 Total items: {len(df)}")
print(f'📝 Columns: {", ".join(df.columns)}')
print(f"\n📦 Stock Status Summary:")
print(df["Stock Status"].value_counts())
print(f"\n🏢 Categories:")
print(df["Category"].value_counts())
