"""
Sanitized proof of concept for the Natoos security write-up.

The original issue has been fixed.

This file intentionally does not contain:
- real credentials
- real national codes
- authentication tokens
- bulk scanning logic
- user data

It only shows the basic request structure that was involved
in the original authorized testing.
"""

import requests


BASE_URL = "https://example.invalid"
PLACEMENT_ID = "REDACTED"
REPORT_TOKEN = "REDACTED"


def check_receipt():
    url = f"{BASE_URL}/Education/GetPlacementReceiptShow"

    params = {
        "PlacementId": PLACEMENT_ID,
        "token": REPORT_TOKEN,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    print("Status:", response.status_code)


if __name__ == "__main__":
    check_receipt()