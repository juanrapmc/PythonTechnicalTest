import requests
import os

LEI_API_URL = os.getenv("LEI_API_URL", "https://leilookup.gleif.org/api/v2/leirecords")


def getLeiLegalName(lei):
    """
    Gets legal name of given legal entity identifier from GLEIF LEI Look-up API

    Args:
        lei: legal entity identifier

    Returns:
        Legal name of the LEI if it exists or None if it does not or an exception occured
    """
    try:
        resp = requests.get(LEI_API_URL, params={"lei": lei})
        data = resp.json()
        if not resp.ok or not data:
            raise Exception()

        return data[0]["Entity"]["LegalName"]["$"]
    except Exception:
        return None
