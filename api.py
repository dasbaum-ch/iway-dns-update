"""
Handles API login and logout stuff
"""

import yaml
import requests


def get_iway_token(config_path="iway-certbot-dns-auth.yml"):
    """
    Reads the config file, authenticates with iway, and returns the token.
    """
    url = "https://backend.login.iway.ch/api/login"
    # Using a session ensures we capture the cookies sent by the server
    session = requests.Session()
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        payload = {
            "username": config["account"]["username"],
            "password": config["account"]["password"],
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = session.post(url, headers=headers, json=payload, timeout=3)
        response.raise_for_status()
        data = response.json()
        auth_token = data.get("token")
        # Extract the csrftoken from the session cookies
        csrf_token = session.cookies.get("csrftoken")
        return auth_token, csrf_token
        # print(f"Login successful! Token: {token}")
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Authentication failed: {e}")

    return None, None


def logout_iway_token(auth_token, csrf_token):
    """
    Reads the config file, authenticates with iway, and returns the token.
    """
    url = "https://backend.login.iway.ch/api/logout"
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}",
            "X-CSRFToken": csrf_token,
        }
        cookies = {"csrftoken": csrf_token}
        response = requests.post(url, headers=headers, cookies=cookies, timeout=3)
        response.raise_for_status()
        data = response.json()
        return data.get("detail")
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Authentication failed: {e}")
    except () as e:
        print(e)

    return None


def update_dns_record(
    domain, record_name, record_type, new_content, auth_token, csrf_token
):
    """
    Updates a specific RRSet in the iWay DNS forward zone.
    """
    url = f"https://backend.login.iway.ch/api/services/dns/forward/{domain}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,  # Use f"Bearer {auth_token}" if the API requires it
        "X-CSRFToken": csrf_token,
    }

    cookies = {"csrftoken": csrf_token}

    # The payload structure for updating an RRSet
    payload = {
        "rrsets": [
            {
                "name": record_name,
                "type": record_type,
                "ttl": 600,
                "changetype": "REPLACE",
                "records": [{"content": new_content, "disabled": False}],
            }
        ]
    }
    try:
        # We use PATCH to update specific items in the rrsets list
        response = requests.patch(
            url, json=payload, headers=headers, cookies=cookies, timeout=30
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to update DNS: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}")
        return False
