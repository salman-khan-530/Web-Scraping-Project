import pandas as pd


def export_to_csv(df, file_path):
    """
    Export product data to a CSV file.

    Args:
        df (pandas.DataFrame): Product DataFrame.
        file_path (str): Output CSV file path.
    """

    try:
        df.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"CSV file saved successfully: {file_path}"
        )

    except Exception as e:
        print(
            f"Error exporting CSV: {e}"
        )


def export_to_excel(df, file_path):
    """
    Export product data to an Excel file.

    Args:
        df (pandas.DataFrame): Product DataFrame.
        file_path (str): Output Excel file path.
    """

    try:
        df.to_excel(
            file_path,
            index=False,
            engine="openpyxl"
        )

        print(
            f"Excel file saved successfully: {file_path}"
        )

    except Exception as e:
        print(
            f"Error exporting Excel: {e}"
        )


def export_data(df, csv_path, excel_path):
    """
    Export product data to both CSV and Excel files.

    Args:
        df (pandas.DataFrame): Product DataFrame.
        csv_path (str): Output CSV file path.
        excel_path (str): Output Excel file path.
    """

    export_to_csv(
        df,
        csv_path
    )

    export_to_excel(
        df,
        excel_path
    )