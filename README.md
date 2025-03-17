# Global Data Trend Analysis App

## Overview
The Global Data Trend Analysis App is a Streamlit-based web application designed to analyze global trends across various Key Performance Indicators (KPIs). It utilizes pre-calculated Chow Test results to identify trending and downgrading patterns in different sectors and subsectors over the past 3, 5, or 10 years.

## Features
- **Interactive filtering**: Users can select sector, subsector, indicator, and trend type.
- **Breakpoint selection**: Choose between 3, 5, or 10 years for trend analysis.
- **Top N countries ranking**: View the top trending or downgrading countries based on Chow Test results.
- **Data visualization**: Displays a table of results and a line chart for selected countries over time.

## Project Structure
```
|-- .gitignore
|-- app.py                   # Streamlit application
|-- data_analysis.ipynb      # Jupyter Notebook for data analysis and Chow Test calculations
|-- data.csv                 # Original dataset
|-- results.csv              # Pre-calculated Chow Test results
|-- README.md                # Project documentation
|-- requirements.txt         # Python dependencies
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

## Usage
Run the Streamlit app using the following command:
```sh
streamlit run app.py
```
The application will launch in the default web browser.

## Data Processing
- The `data_analysis.ipynb` file processes the original dataset (`data.csv`) and applies the Chow Test.
- The results are stored in `results.csv` and used by the Streamlit application.

## Requirements
Ensure that the required Python packages are installed by using `requirements.txt`.

## License
This project is licensed under the MIT License.

