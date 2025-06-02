import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def generate_pr_graph(df, start_date=None, end_date=None):
    """
    Generates the Performance Ratio Evolution graph.
    - Red line: 30-d moving average of PR (Performance Evolution). [cite: 12, 32]
    - Scatter points: PR value of the day, color-coded by GHI. [cite: 12, 16, 32, 36]
    - Dark green line: Budget line, starting from 73.9 and reducing by 0.8% annually. [cite: 13, 14, 15, 33, 34, 35]
    - Displays average PR for last 7, 30, 60, 90, 365 days and lifetime. [cite: 17, 37]
    - Displays points above Target Budget PR. [cite: 17, 37]
    - Accepts optional start_date and end_date to filter the data (Bonus Points). [cite: 20, 40]
    """
    # Ensure 'Date' is datetime and sort the DataFrame
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)

    # Filter data based on start and end dates if provided (Bonus Points) [cite: 20, 40]
    if start_date:
        df = df[df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['Date'] <= pd.to_datetime(end_date)]

    if df.empty:
        print("No data to display for the given date range.")
        return

    df['PR_moving_avg'] = df['PR'].rolling(window=30, min_periods=1).mean()

    budget_start_value = 73.9
    annual_reduction_rate = 0.008 # 0.8%

    df['Budget_PR'] = np.nan # To  Initialize budget column

    min_date_data = df['Date'].min()
    max_date_data = df['Date'].max()
    current_year_start = pd.to_datetime(f"{min_date_data.year}-07-01") if min_date_data.month > 6 else pd.to_datetime(f"{min_date_data.year-1}-07-01")

    current_budget = budget_start_value
    # Loop slightly beyond max_date to cover all years in the data
    while current_year_start <= max_date_data + pd.DateOffset(years=1):
        next_year_start = current_year_start + pd.DateOffset(years=1)
        year_mask = (df['Date'] >= current_year_start) & (df['Date'] < next_year_start)
        df.loc[year_mask, 'Budget_PR'] = current_budget
        current_budget *= (1 - annual_reduction_rate) 
        current_year_start = next_year_start

    # Color-code scatter points based on GHI 
    def get_ghi_color(ghi):
        if ghi < 2:
            return 'navy' # Less than 2: Navy blue
        elif 2 <= ghi < 4:
            return 'lightskyblue' # 2-4: Light blue (changed for better contrast) 
        elif 4 <= ghi < 6:
            return 'orange' # 4-6: Orange
        else: # ghi >= 6
            return 'brown' # >6: Brown 

    df['GHI_Color'] = df['GHI'].apply(get_ghi_color)

    # Creates the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.scatter(df['Date'], df['PR'], c=df['GHI_Color'], s=20, alpha=0.7, label='Daily PR')
    ax.plot(df['Date'], df['PR_moving_avg'], color='red', linewidth=2, label='30-d moving average of PR')
    first_year_budget = budget_start_value
    second_year_budget = budget_start_value * (1 - annual_reduction_rate)
    third_year_budget = second_year_budget * (1 - annual_reduction_rate)
    
    budget_label = (
        f'Target Budget Yield Performance Ratio '
        f'[1Y-{first_year_budget:.1f}%, 2Y-{second_year_budget:.1f}%, 3Y-{third_year_budget:.1f}%]'
    )
    ax.plot(df['Date'], df['Budget_PR'], color='darkgreen', linewidth=2, label=budget_label)

    # Customizes plot
    ax.set_xlabel('')
    ax.set_ylabel('Performance Ratio [%]')

    if start_date and end_date:
        title_text = f'Performance Ratio Evolution\nFrom {pd.to_datetime(start_date).strftime("%Y-%m-%d")} to {pd.to_datetime(end_date).strftime("%Y-%m-%d")}'
    else:
        title_text = f'Performance Ratio Evolution\nFrom {df["Date"].min().strftime("%Y-%m-%d")} to {df["Date"].max().strftime("%Y-%m-%d")}'
    
    ax.set_title(title_text, fontsize=14)


    # Date formatting for x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    plt.xticks(rotation=45, ha='right')

    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_ylim(0, 100)

    legend_elements_ghi = [
        plt.Line2D([0], [0], marker='o', color='w', label='< 2', markerfacecolor='navy', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='2-4', markerfacecolor='lightskyblue', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='4-6', markerfacecolor='orange', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='> 6', markerfacecolor='brown', markersize=7)
    ]
    ghi_legend = ax.legend(handles=legend_elements_ghi, title='Daily Irradiation [kWh/m2]', loc='upper left', bbox_to_anchor=(0.1, 1.0))
    ax.add_artist(ghi_legend)
    legend_elements_main = [
        plt.Line2D([0], [0], marker='o', color='w', label='Daily PR', markerfacecolor='orange', markersize=7),
        plt.Line2D([0], [0], color='red', linewidth=2, label='30-d moving average of PR'),
        plt.Line2D([0], [0], color='darkgreen', linewidth=2, label=budget_label)
    ]
    ax.legend(handles=legend_elements_main, loc='lower center', bbox_to_anchor=(0.5, 0.2), ncol=1)

    pr_above_budget = df[df['PR'] > df['Budget_PR']]
    total_pr_points = len(df)
    num_pr_above_budget = len(pr_above_budget)

    percentage_above_budget = (num_pr_above_budget / total_pr_points) * 100 if total_pr_points > 0 else 0

    ax.text(0.6, 0.4, f'Points above Target Budget PR = {num_pr_above_budget}/{total_pr_points} = {percentage_above_budget:.1f}%',
            transform=ax.transAxes, fontsize=10, color='black',
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.1))

    latest_date = df['Date'].max()

    def get_avg_pr(days):
        if days == 'lifetime':
            return df['PR'].mean()
        else:
            filtered_df = df[df['Date'] >= latest_date - pd.Timedelta(days=days)]
            return filtered_df['PR'].mean() if not filtered_df.empty else np.nan

    avg_pr_7d = get_avg_pr(7)
    avg_pr_30d = get_avg_pr(30)
    avg_pr_60d = get_avg_pr(60)
    avg_pr_90d = get_avg_pr(90)
    avg_pr_365d = get_avg_pr(365)
    avg_pr_lifetime = get_avg_pr('lifetime')

    text_str = (
        f'Average PR last 7-d: {avg_pr_7d:.1f}%\n'
        f'Average PR last 30-d: {avg_pr_30d:.1f}%\n'
        f'Average PR last 60-d: {avg_pr_60d:.1f}%\n'
        f'Average PR last 90-d: {avg_pr_90d:.1f}%\n'
        f'Average PR last 365-d: {avg_pr_365d:.1f}%\n'
        f'Average PR Lifetime: {avg_pr_lifetime:.1f}%'
    )
    ax.text(0.7, 0.05, text_str, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=dict(boxstyle="round,pad=0.5", fc="cyan", alpha=0.1))

    plt.tight_layout()
    
    if start_date and end_date:
        output_filename = f'performance_evolution_{pd.to_datetime(start_date).strftime("%Y%m%d")}_to_{pd.to_datetime(end_date).strftime("%Y%m%d")}.png'
    else:
        output_filename = 'performance_evolution.png'
        
    plt.savefig(output_filename)
    plt.close()