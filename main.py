import os
import pandas as pd
from visualization import generate_pr_graph
from datetime import datetime

def preprocess_data(base_data_path="data"):
    """
    Generates a single CSV file containing all the data from both the PR and GHI folders.
    The new CSV file will contain 3 columns: Date, GHI, PR.
    """
    all_pr_data = []
    all_ghi_data = []

    pr_path = os.path.join(base_data_path, "PR")
    ghi_path = os.path.join(base_data_path, "GHI")
    pr_files_found = 0

    # Process PR data
    if os.path.exists(pr_path):
        for root, _, files in os.walk(pr_path):
            for file in files:
                if file.endswith(".csv"):
                    pr_files_found += 1
                    file_path = os.path.join(root, file)
                    try:
                        date_str = os.path.basename(file).replace(".csv", "")
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                        df_temp = pd.read_csv(file_path, parse_dates=['Date'])
                        
                        if 'PR' in df_temp.columns:
                            numeric_pr_value = float(df_temp['PR'].iloc[0]) 
                            all_pr_data.append({"Date": date_obj, "PR": numeric_pr_value})
                        else:
                            print(f"Warning: 'PR' column not found in {file_path}. Skipping this file.")

                    except Exception as e:
                        print(f"Error processing PR file {file_path}: {e}")
    else:
        print(f"Error: PR directory not found at {pr_path}")
    print(f"Found {pr_files_found} PR CSV files.")

    # Create a DataFrame for PR data
    pr_df = pd.DataFrame(all_pr_data).sort_values(by="Date").drop_duplicates(subset=['Date'])
    pr_df.set_index("Date", inplace=True)

    ghi_files_found = 0
    # Process GHI data
    if os.path.exists(ghi_path):
        for root, _, files in os.walk(ghi_path):
            for file in files:
                if file.endswith(".csv"):
                    ghi_files_found += 1
                    file_path = os.path.join(root, file)
                    try:
                        date_str = os.path.basename(file).replace(".csv", "")
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        df_temp = pd.read_csv(file_path, parse_dates=['Date'])

                        if 'GHI' in df_temp.columns:
                            numeric_ghi_value = float(df_temp['GHI'].iloc[0]) 
                            all_ghi_data.append({"Date": date_obj, "GHI": numeric_ghi_value})
                        else:
                            print(f"Warning: 'GHI' column not found in {file_path}. Skipping this file.")

                    except Exception as e:
                        print(f"Error processing GHI file {file_path}: {e}")
    else:
        print(f"Error: GHI directory not found at {ghi_path}")
    print(f"Found {ghi_files_found} GHI CSV files.")

    # Creating a DataFrame for GHI data
    ghi_df = pd.DataFrame(all_ghi_data).sort_values(by="Date").drop_duplicates(subset=['Date'])
    ghi_df.set_index("Date", inplace=True)

    # Merging PR and GHI dataframes on Date
    # We can use 'outer' merge to include dates present in either GHI or PR 
    processed_df = pd.merge(pr_df, ghi_df, left_index=True, right_index=True, how="outer")
    processed_df.reset_index(inplace=True)
    processed_df.rename(columns={"index": "Date"}, inplace=True)
    processed_df = processed_df[['Date', 'GHI', 'PR']]

    # Now we will Drop rows where either GHI or PR is NaN (if a date exists for one but not the other)
    processed_df.dropna(subset=['GHI', 'PR'], inplace=True)
    print(f"Finished preprocessing. Final DataFrame has {len(processed_df)} rows. Files found: {pr_files_found} PR and {ghi_files_found} GHI.")
    return processed_df

if __name__ == "__main__":
    base_data_path = "data" 

    processed_df = preprocess_data(base_data_path=base_data_path)
    output_csv_path = "processed_data.csv"
    processed_df.to_csv(output_csv_path, index=False)
    print(f"Processed data saved to {output_csv_path}")

    # Default date range from the given assessment example graph [cite: 19, 39]
    default_start_date = "2019-07-01"
    default_end_date = "2022-03-24"

    # --- Bonus Points: Accept start and end date arguments --- 
    # We can uncomment and modify these lines to test different date ranges
    # my_start_date = "2020-01-01"
    # my_end_date = "2021-01-01"
    # generate_pr_graph(processed_df, start_date=my_start_date, end_date=my_end_date)
    # print(f"Graph generated for custom date range: performance_evolution_{my_start_date}_to_{my_end_date}.png")

    generate_pr_graph(processed_df, start_date=default_start_date, end_date=default_end_date)
    print("Graph generated: performance_evolution.png")