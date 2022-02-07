from __future__ import annotations

import datetime as dt
import os

import googleapiclient.discovery
import pytz
from apiclient.http import MediaFileUpload

import googletools.credentials


def _load_drive_api():
    """Returns the API object for manipulating files"""
    credentials = googletools.credentials.obtain_credentials()
    service = googleapiclient.discovery.build(
        "drive", "v3", credentials=credentials, cache_discovery=False
    )
    return service


def upload_file(filename: str, file_id: str = None):
    """ "
    Uploads or updates a file in Google Drive

    :rtype: None
    :param filename: The file thats needs to be uploaded
    :param file_id: The ID of the to be uploaded file if not provided,
    a new file will be created
    """
    basename: str = os.path.basename(filename)
    title, _ = os.path.splitext(filename)

    drive_api = _load_drive_api()

    file_metadata = {"name": basename, "title": title}

    media_body = MediaFileUpload(filename, resumable=True)

    if file_id is None:
        file = (
            drive_api.files()
            .create(body=file_metadata, media_body=media_body, fields="id")
            .execute()
        )
        file_id = file.get("ID")
        print(f"The file ID is {file_id}")
    else:
        drive_api.files().update(
            fileId=file_id, body=file_metadata, media_body=media_body
        ).execute()


def modified_date(file_id: str) -> dt.datetime:
    """
    Returns the datetime when a file was last modified
    :param file_id: The file ID of the file
    :return: The modified time
    """
    drive_api = _load_drive_api()
    file = drive_api.files().get(fileId=file_id, fields="modifiedTime").execute()
    date_str = file.get("modifiedTime")
    date = dt.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    date_utc = date.replace(tzinfo=pytz.utc)
    return date_utc.astimezone()
