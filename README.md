# iway-dns-update
Simple script to update DNS records

# Project Structure

* `main.py`: The entry point that handles command-line arguments.
* `api.py`: The core module containing logic for login, CSRF handling, DNS patching, and logout.
* `iway-certbot-dns-auth.yml`: Your private configuration file (contains credentials).

# Setup

## Requirements

I'm using `uv`, but feel free to use what you need.

```
uv sync
uv lock --upgrade
```

## Configuration

Create a file `iway-certbot-dns-auth.yml` with content:
```
account:
  username: 'api user'
  password: 'secret'
```

## Security

Just ensure that you don't save any credentials in this git repo

# Usage

You can run the script from the terminal by passing the domain, record name, type, and the new value.

Example: Update a TLSA record

```bash
python main.py \
  --domain dasbaum.ch \
  --name _25._tcp.mail.dasbaum.ch \
  --type TLSA \
  --value "3 1 1 <sha512>"
```

|Argument|Description|Example|
|--------|-----------|-------|
|--domain|The zone domain|dasbaum.ch
|--name|Full record name|_acme-challenge.dasbaum.ch
|--type|DNS Record Type|"TXT, TLSA, A"
|--value|New record content|your-secret-token
|--config| (Optional) Path to config|my-config.yml

# How it works

1. **Authentication**: The script logs into the iWay API to retrieve a Bearer token and a `csrftoken` cookie.
2. **CSRF Handling**: It extracts the `csrftoken` from the response cookies and includes it in the `X-CSRFToken` header for subsequent requests.
3. **DNS Patching**: It sends a `PATCH` request to the forward zone endpoint to update the specific `rrsets`.
4. **Session Cleanup**: It performs a logout request to invalidate the tokens immediately after the work is done.
