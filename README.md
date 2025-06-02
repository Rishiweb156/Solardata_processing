# Solar PV Plant Performance Analysis and Visualization

## Objective
The primary objective of this project is to process raw Performance Ratio (PR) and Global Horizontal Irradiance (GHI) data from a solar PV plant and visualize its performance trends.

## Dataset
The dataset consists of daily PR and GHI values, organized into directories based on year-month and parameter.

**Parameters:**
* **PR (Performance Ratio):** Tracks the daily performance of the PV plant. A high value indicates good plant performance.
* **GHI (Global Horizontal Irradiance):** Tracks the total irradiation for a particular day. A high value indicates a sunny day.

## Data Processing
The project processes the raw daily CSV files into a single, consolidated CSV file.

* **Output File:** 'processed_data.csv'
* **Columns:** 'Date', 'GHI', 'PR'

* **Note:** During development, it was observed that the provided local dataset contains **197 rows** for both PR and GHI. The script will accurately process all available 197 rows.

**Key Function:**
* 'preprocess_data(base_data_path="data")' in 'main.py': Handles reading individual CSVs, extracting Date, GHI, and PR values, and merging them into a single pandas DataFrame.

## Data Visualization
A comprehensive Performance Ratio Evolution graph is generated based on the processed data.

**Graph Elements:**
* **Red Line:** Represents the 30-day moving average of PR (Performance Evolution).
* **Scatter Points:** Display daily PR values, color-coded based on GHI (Daily Irradiation):
    * '< 2 kWh/m2': Navy blue
    * '2-4 kWh/m2': Light blue
    * '4-6 kWh/m2': Orange
    * '> 6 kWh/m2': Brown
* **Dark Green Line:** Represents the Target Budget Yield Performance Ratio, starting at 73.9% and reducing by 0.8% annually (as per assessment).
* **Summary Metrics:**
    * **Points above Target Budget PR:** Shows the count and percentage of daily PR points exceeding the Budget PR.
    * **Average PR:** Displays average PR for the last 7, 30, 60, 90, 365 days, and Lifetime.

**Key Function:**
* 'generate_pr_graph(df, start_date=None, end_date=None)' in 'visualization.py': Creates and saves the performance graph.

## Important Notes (from Assessment)
* The data has to be collated into a single file.
* Create a single function to preprocess the data. Make sure your code is organized and readable.
* Create a single function to generate the graph. Make sure your code is organized and readable.
* Please note that the values and the trends might not match the example graph exactly, as the provided data has been slightly altered or might be a subset of the original.

## Bonus Points Addressed
The script has been enhanced to accept start and end date arguments for generating a PR graph based on a specified date range.

* **Usage:** You can uncomment and modify the 'my_start_date' and 'my_end_date' variables in 'main.py' to filter the data for a specific period.
* **Output:** The graph title and filename will dynamically update to reflect the custom date range used.

## How to Run the Code

### 1. Project Setup
* Ensure you have Python 3.x installed.
* Save the 'main.py' and 'visualization.py' files in your project directory.
* Create a 'data' folder in the same directory, Inside the 'data' folder, we will have  'PR' and 'GHI' subfolders.
* Place your daily PR and GHI CSV files (e.g., '2019-07-01.csv', '2019-07-02.csv', etc.) into their respective year-month subdirectories within the 'PR' and 'GHI' folders.
    * **Example structure:** 'your_project_root/data/PR/2019-07/2019-07-01.csv'

### 2. Install Dependencies
Open your terminal or command prompt, navigate to your project directory, and run:
pip install pandas matplotlib numpy

### 3. Run the script 
python main.py

### 4. View Results
A processed_data.csv file will be created in your project directory containing the combined data.
A performance_evolution.png image file will be generated in your project directory, displaying the performance graph.




