# Global Data Trend Analysis App

## Overview
The Global Data Trend Analysis App is a Streamlit-based web application designed to analyze global trends across various Key Performance Indicators (KPIs). It utilizes pre-calculated Chow Test results to identify trending and downgrading patterns in different sectors and subsectors over the past 3, 5, or 10 years. Users can also upload their own data, and the system will calculate the trend using the Chow Test and store the results in an SQLite3 database.

## Features
- **Interactive filtering**: Users can select sector, subsector, indicator, and trend type.
- **Breakpoint selection**: Choose between 3, 5, or 10 years for trend analysis.
- **Top N countries ranking**: View the top trending or downgrading countries based on Chow Test results.
- **Data visualization**: Displays a table of results and a line chart for selected countries over time.
- **User data upload**: Users can upload their own dataset for trend analysis using the Chow Test. The results are automatically stored in an SQLite3 database.

## Project Structure
```
|-- .gitignore
|-- .gitattributes             # Git LFS configuration file
|-- .streamlit/                # Configuration folder for Streamlit (e.g., custom settings)
|-- app.py                     # Streamlit application
|-- data_analysis.ipynb        # Jupyter Notebook for data analysis and Chow Test calculations
|-- data.csv                   # Original dataset
|-- results.csv                # Pre-calculated Chow Test results
|-- pages/
|   |-- page_1.py              # Trend analysis dashboard
|   |-- page_2.py              # Upload your data section
|-- utils.py                   # Contains external helper functions
|-- calculated_data.db         # SQLite3 database containing calculated trend data
|-- data.db                    # SQLite3 database containing original uploaded data
|-- README.md                  # Project documentation
|-- requirements.txt           # Python dependencies
```

## Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Handling Large Files
Since GitHub has a 100MB file limit, handling large files like `results.csv`, `calculated_data.db`, and `data.db` requires using Git Large File Storage (LFS):

### **Using Git LFS (Recommended)**

If your files are large, use Git Large File Storage (LFS) to track and manage them:

   1. **Install Git LFS**:
      ```sh
      git lfs install
      ```

   2. **Track the large files**:
      Use the following command to track the files:
      ```sh
      git lfs track "results.csv"
      git lfs track "calculated_data.db"
      git lfs track "data.db"
      ```

   3. **Add the `.gitattributes` file**:
      The above command will automatically add the `.gitattributes` file, which is responsible for Git LFS configuration.

   4. **Commit and push**:
      After tracking the files, commit the changes and push them to the repository:
      ```sh
      git add .gitattributes results.csv calculated_data.db data.db
      git commit -m "Track large files with Git LFS"
      git push origin main
      ```

## Usage
Run the Streamlit app using the following command:
```sh
streamlit run app.py
```
The application will launch in the default web browser.

### **User Data Upload**:
Users can upload their own dataset through the app interface. The system will calculate the trend using the Chow Test and store the results in the `calculated_data.db` SQLite3 database.

### **Pages**:
- **Trend Analysis Dashboard** (`page_1.py`): Provides an overview of the trend analysis results.
- **Upload Your Data** (`page_2.py`): Allows users to upload their dataset, which will be processed using the Chow Test.

## Data Processing
- The `data_analysis.ipynb` file processes the original dataset (`data.csv`) and applies the Chow Test.
- The results are stored in `results.csv` (for pre-calculated data) and in the SQLite3 database (`calculated_data.db`) when new data is uploaded via the application. The original uploaded data is stored in `data.db`.

## Requirements
Ensure that the required Python packages are installed by using `requirements.txt`.

## License
This project is licensed under the MIT License.

## Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/reference/index.html)
- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)

