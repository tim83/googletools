import datetime as dt

import googletools.drive
import tests.data


def test_google_modified_date():
    """Test the method for obtaining the modified date for a file from Google Drive"""
    assert isinstance(
        googletools.drive.modified_date(tests.data.TEST_SHEET_ID), dt.datetime
    )
