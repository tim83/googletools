from __future__ import annotations

import typing
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import googletools.settings

SCOPES: list[str] = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def obtain_credentials() -> Credentials:
    """Logs the user in and returns the credentials"""

    token_file: Path = googletools.settings.CACHE_DIR / "google_token.json"

    # Load credentials if they exist
    credentials: typing.Optional[Credentials] = None
    if token_file.exists():
        credentials = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(googletools.settings.GOOGLE_CLIENT_SECRET_FILE), SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        token_dir: Path = token_file.parent
        if not token_dir.is_dir():
            token_dir.mkdir()

        with open(token_file, "w") as token:
            token.write(credentials.to_json())

    return credentials
