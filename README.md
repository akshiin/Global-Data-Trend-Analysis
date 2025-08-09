# Global Data Trend Analysis App

## Overview
The **Global Data Trend Analysis App** is a Streamlit-based web application designed to analyze global trends across various **Key Performance Indicators (KPIs)**. It utilizes **the Chow Test** to detect structural breaks and identify trending and downgrading patterns across multiple sectors and subsectors over different timeframes (**3, 5, or 10 years**).

For the most interpretable and easy-to-understand results, users can select:

- **Sector** → *Economy*  
- **Subsector** → *Productivity and Labour Market*  
- **Indicator** → *Gross Domestic Product (Billion US Dollars)*  

This setup provides a clear and meaningful starting point for exploring the data.

**Example view:**  
<img width="1512" height="865" alt="image" src="https://github.com/user-attachments/assets/ea057e34-28f8-4767-a6f6-c4e9eff20f33" />

Users can also **upload their own datasets**, and the system will compute trend analysis in real-time. The results are now stored in a **PostgreSQL database** for better performance and scalability. Additionally, a **caching system** has been implemented to speed up query execution and optimize resource usage.

## Key Features
- **Interactive Filtering**: Users can select sector, subsector, indicator, and trend type.
- **Structural Break Detection**: Detects breakpoints over 3, 5, or 10 years using the Chow Test.
- **Top N Country Ranking**: View the top trending or declining countries.
- **Data Visualization**: Line charts and tables displaying results dynamically.
- **User Data Upload**: Users can upload their own datasets, and the system will analyze the trend and store results in a **PostgreSQL** database.
- **Caching System**: Reduces redundant computations and improves query performance.
- **PostgreSQL Integration**: Provides scalability and efficient data handling.

## Project Structure
```
|-- .gitignore
|-- .gitattributes             # Git LFS configuration file
|-- .streamlit/                # Configuration folder for Streamlit (e.g., custom settings)
|-- app.py                     # Streamlit application
|-- data_analysis.ipynb        # Jupyter Notebook for data analysis and Chow Test calculations
|-- docker-compose.yml         # Docker configuration for running the app and PostgreSQL database
|-- pages/
|   |-- page_1.py              # Trend analysis dashboard
|   |-- page_2.py              # Upload your data section
|-- utils.py                   # Contains external helper functions
|-- LICENSE                    # MIT License
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
4. Set up PostgreSQL Database:

Ensure PostgreSQL is Installed:
   ```sh
   sudo apt update && sudo apt install postgresql postgresql-contrib
   ```

Set up the database:
   ```sh
    psql -U your_user -d your_database -f schema.sql
   ```

## Usage
Run the Streamlit app using the following command:
```sh
streamlit run app.py
```
The application will launch in the default web browser.

### User Data Upload Process

- Navigate to the "Upload Your Data" section in the app.
- Download the provided CSV template.
- Fill in the required data and upload the file.
- The system processes the data, runs Chow Test analysis, and stores the results in the PostgreSQL database.

### Data Processing

- The data_analysis.ipynb notebook processes raw datasets and applies the Chow Test for trend detection.
- The results are stored in PostgreSQL instead of local files for better scalability and multi-user access.
- Caching System reduces processing time by preventing redundant calculations.

### PostgreSQL & Caching Benefits

- PostgreSQL:
   - Handles large datasets efficiently.
   - Supports concurrent users.
   - Improves data integrity and query speed.
- Streamlit Caching:
   - Speeds up repeated calculations.
   - Optimizes resource usage.
   - Enhances user experience with faster response times.
 
### **Pages**:
- **Trend Analysis Dashboard** (`page_1.py`): Provides an overview of the trend analysis results.
- **Upload Your Data** (`page_2.py`): Allows users to upload their dataset, which will be processed using the Chow Test.

## Requirements
Ensure that the required Python packages are installed by using `requirements.txt`.

## License
This project is licensed under the MIT License.

## Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/reference/index.html)
- [PostgreSQL Documentation](https://www.psycopg.org/docs/)
