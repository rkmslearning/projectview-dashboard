# Project Status Dashboard 📊

A Streamlit-based web application for managing and visualizing project status data from Excel files.

## Features

✅ **Excel File Upload** - Upload .xlsx or .xls files  
✅ **Interactive Data Editor** - Add, edit, and delete records  
✅ **Management Dashboard** - Real-time visualizations and KPIs  
✅ **Data Persistence** - Local CSV storage (SharePoint integration coming soon)  
✅ **Search & Filter** - Find and filter data easily  
✅ **Export Data** - Download filtered data as Excel

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage Guide

### 📤 Upload Data
1. Click "Upload Data" in the sidebar
2. Choose your Excel file
3. Preview the data
4. Click "Save to Database" or "Append to Existing Data"

### ✏️ Edit Data
1. Navigate to "Edit Data"
2. Modify cells directly in the table
3. Add or delete rows as needed
4. Click "Save Changes"

### 📈 Dashboard
- View key metrics and KPIs
- Analyze status distribution
- Track trends over time
- Filter and export data

### 📋 View All Data
- See complete dataset
- Search across all fields
- Select specific columns
- View summary statistics

## Data Storage

Data is stored locally in the `data/` directory as CSV files. This makes it easy to:
- Backup your data
- Version control changes
- Migrate to SharePoint later

## Future Enhancements

- [ ] SharePoint integration for cloud storage
- [ ] User authentication
- [ ] Email notifications
- [ ] Custom report generation
- [ ] Multi-user collaboration

## Troubleshooting

**App won't start?**
- Make sure all dependencies are installed
- Check Python version (3.8+ required)

**Can't upload file?**
- Verify file format (.xlsx or .xls)
- Check file isn't password protected
- Ensure file size is reasonable (<100MB)

## Support

For issues or questions, please check the Streamlit documentation at https://docs.streamlit.io
