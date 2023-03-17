"""Module for interacting with Google Sheets"""
from __future__ import annotations

import locale

import googleapiclient.discovery
import pandas as pd

import googletools.credentials


def load_sheet_api(api_version: str = "v4"):
    """
    Returns the API object for manipulating sheets
    :param api_version: The version of the API to use
    """
    credentials = googletools.credentials.obtain_credentials()
    service = googleapiclient.discovery.build(
        "sheets", api_version, credentials=credentials, cache_discovery=False
    )
    sheet = service.spreadsheets()  # pylint: disable=no-member
    return sheet


def import_spreadsheet(
    sheet_id: str,
    selected_range: str,
    column_header: bool = True,
    row_index: bool = True,
) -> pd.DataFrame:
    """Import the content from a Google Sheet as a pandas dataframe
    :param sheet_id: The ID of the sheet (can be found in the URL of the sheet)
    :param selected_range: The range that contains the to be imported data (
    e.g. Blad1!A1:B5)
    :param column_header: Treat the first column as a header
    :param row_index: Treat the first row as a header
    :return The dataframe containing the selected data from the sheet"""

    sheet = load_sheet_api()
    result = sheet.values().get(spreadsheetId=sheet_id, range=selected_range).execute()
    values = result.get("values", [])
    locale.setlocale(locale.LC_NUMERIC, "")

    data = pd.DataFrame(values)
    if column_header:
        column_headers = data.iloc[0]
        data.drop(data.index[0], inplace=True)
        data.rename(columns=column_headers, inplace=True)
    else:
        column_headers = data.columns

    if row_index:
        data.set_index(column_headers[0], inplace=True)

    return data


def export_to_sheet(sheet_id: str, selected_range: str, data: pd.DataFrame):
    """
    Exports data to a google sheet

    :rtype: None
    :param data: A matrix containing every match and its score
    :param sheet_id: The ID of the sheet (can be found in the URL of the sheet)
    :param selected_range: The range that contains the to be imported data (
    e.g. Blad1!A1:B5)
    """
    sheet = load_sheet_api()
    sheet.values().update(
        spreadsheetId=sheet_id,
        valueInputOption="RAW",
        range=selected_range,
        body={
            "majorDimension": "ROWS",
            "values": data.T.reset_index().T.values.tolist(),
        },
    ).execute()
