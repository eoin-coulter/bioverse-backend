import pandas as pd
import openpyxl
from sqlalchemy import create_engine


# Database connection details (modify accordingly)
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mydatabase"
DB_USER="postgres"
DB_PASSWORD="password"

# Create a database engine for PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def excel_to_db(excel_file: str):
    # Read the Excel workbook
    xls = pd.ExcelFile(excel_file)

    # Loop through all the sheet names
    for sheet_name in xls.sheet_names:
        try:
            # Read each sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Write the DataFrame to the corresponding table in the DB
            df.to_sql(sheet_name, engine, if_exists='replace', index=False)
            print(f"Data from sheet '{sheet_name}' has been successfully inserted into the '{sheet_name}' table.")
        except Exception as e:
            print(f"An error occurred while processing sheet '{sheet_name}': {e}")

if __name__ == '__main__':
    excel_file_path = 'data.xlsx'  # Path to your Excel file
    excel_to_db(excel_file_path)
