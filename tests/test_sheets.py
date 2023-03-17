import pandas as pd

import googletools.sheets

TEST_SHEET_ID = "1FdGvHITMbk_DyONFmE00IcZY79He2SWNUT35klXJu40"
IMPORT_RANGE = "Import Data!A1:F6"


def test_google_import_spreadsheet():
    """Test the models to import data from Google sheets"""
    correct_data_headers = pd.DataFrame(
        [[str(row * 10 + column) for column in range(1, 6)] for row in range(1, 6)],
        columns=[f"Column {column}" for column in range(1, 6)],
        index=[f"Row {row}" for row in range(1, 6)],
    )
    correct_data_noheaders = pd.DataFrame(
        [[""] + [f"Column {column}" for column in range(1, 6)]]
        + [
            [f"Row {row}"] + [str(row * 10 + column) for column in range(1, 6)]
            for row in range(1, 6)
        ]
    )
    google_data_noheaders = googletools.sheets.import_spreadsheet(
        TEST_SHEET_ID,
        IMPORT_RANGE,
        column_header=False,
        row_index=False,
    )
    google_data_headers = googletools.sheets.import_spreadsheet(
        TEST_SHEET_ID,
        IMPORT_RANGE,
        column_header=True,
        row_index=True,
    )
    assert correct_data_headers.equals(google_data_headers)
    assert correct_data_noheaders.equals(google_data_noheaders)
