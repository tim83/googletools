import datetime as dt

import googletools.drive

TEST_SHEET_ID = "1FdGvHITMbk_DyONFmE00IcZY79He2SWNUT35klXJu40"
IMPORT_RANGE = "Import Data!A1:F6"


def test_google_modified_date():
    """Test the method for obtaining the modified date for a file from Google Drive"""
    assert isinstance(googletools.drive.modified_date(TEST_SHEET_ID), dt.datetime)
