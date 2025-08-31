import pandas as pd
import os

def process_sales_data():
    data_folder = "data"
    csv_files = ["daily_sales_data_0.csv",
                 "daily_sales_data_1.csv",
                 "daily_sales_data_2.csv"]

    # Read, filter, clean, and process all CSVs in one go
    combined_df = pd.concat([
        pd.read_csv(os.path.join(data_folder, file))
          .query("product.str.lower() == 'pink morsel'", engine="python")
          .assign(price_clean=lambda x: x['price'].str.replace('$','').astype(float),
                  Sales=lambda x: x['quantity'] * x['price_clean'])
          .loc[:, ['Sales', 'date', 'region']]
          .rename(columns={'date': 'Date', 'region': 'Region'})
        for file in csv_files
    ], ignore_index=True).sort_values("Date")

    # Save output
    output_file = "formatted_sales_data.csv"
    combined_df.to_csv(output_file, index=False)

    # Quick summary
    print(f"Output saved to: {output_file}")
    print(f"Total rows: {len(combined_df)}")
    print(f"Date range: {combined_df['Date'].min()} → {combined_df['Date'].max()}")
    print(f"Regions: {sorted(combined_df['Region'].unique())}")
    print(f"Total Sales: ${combined_df['Sales'].sum():,.2f}")
    print("\nPreview:")
    print(combined_df.head(10))

    return combined_df

if __name__ == "__main__":
    process_sales_data()
