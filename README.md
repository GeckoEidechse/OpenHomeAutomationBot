Random change to test action

# OpenHomeAutomationBot

A reddit bot written in Python to crosspost reddit post matching some keywords from one subreddit to another

## Usage

Generate appropriate tokens for your reddit bot

Create config file for [`praw`](https://praw.readthedocs.io/)

```bash
cat > praw.ini << EOF
[openhomeautomationbot]
client_id = YOUR_CLIENT_ID_HERE
client_secret = YOUR_CLIENT_SECRET_HERE
username = YOUR_USERNAME_HERE
password = YOUR_PASSWORD_HERE
user_agent = YOUR_USER_AGENTEOF_HERE
EOF
```

This project uses [Poetry](https://python-poetry.org/). To run, [install Poetry](https://python-poetry.org/docs/#installation) then simply run:

```bash
poetry run openhomeautomationbot
```
