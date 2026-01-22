"""
Update my DANE TLSA record
"""

import argparse
import sys
from api import get_iway_token, logout_iway_token, update_dns_record
# Call the function to get your token


def main():
    parser = argparse.ArgumentParser(description="Update iWay DNS records via API")
    # Define the required arguments
    parser.add_argument(
        "--domain", required=True, help="The zone domain (e.g., dasbaum.ch)"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Full record name (e.g., _25._tcp.mail.dasbaum.ch)",
    )
    parser.add_argument(
        "--type", required=True, help="Record type (e.g., TLSA, TXT, A, AAAA, CAA)"
    )
    parser.add_argument(
        "--value", required=True, help="The new content/value for the record"
    )

    # Optional: allow path to config file
    parser.add_argument(
        "--config", default="iway-certbot-dns-auth.yml", help="Path to YAML config"
    )

    args = parser.parse_args()

    # 1. Login
    print(f"Authenticating for {args.domain}...")
    auth_token, csrf_token = get_iway_token(args.config)
    if not auth_token or not csrf_token:
        print("Error: Could not obtain authentication tokens.")
        sys.exit(1)

    try:
        # 2. Perform the update using the arguments
        print(f"Updating {args.type} record for {args.name}...")
        success = update_dns_record(
            domain=args.domain,
            record_name=args.name,
            record_type=args.type,
            new_content=args.value,
            auth_token=auth_token,
            csrf_token=csrf_token,
        )

        if success:
            print("DNS record updated successfully.")
        else:
            print("Failed to update DNS record.")
            sys.exit(1)
    finally:
        # 3. Always try to logout to keep the API session clean
        logout_iway_token(auth_token, csrf_token)


if __name__ == "__main__":
    main()
