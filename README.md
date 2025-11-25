# Telegram MCQ Bot

This project contains a Python script and GitHub Actions workflow to send multiple-choice questions from the `ancient.txt` file to specified Telegram chats every day at a scheduled time.

## How It Works

- A Python script (`bot.py`) reads the `ancient.txt` file and a `progress.txt` file.
- The `progress.txt` file stores the index of the last question sent.
- Every day, the script sends the next 20 questions as polls to the specified Telegram chats.
- It then updates the `progress.txt` file with the new index.
- A GitHub Actions workflow runs this script automatically every day at 11:45 AM IST (06:15 UTC).

## Setup Instructions

To get this bot running, you need to follow these steps:

### 1. Get Your Telegram Bot Token

If you haven't already, you need to create a Telegram bot and get its API token.

1.  Open Telegram and search for the **@BotFather** user.
2.  Start a chat with BotFather and send the `/newbot` command.
3.  Follow the instructions. Give your bot a name and a username.
4.  BotFather will provide you with an **API token**. It will look something like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123456789`.
5.  **Keep this token safe and private!** The token you provided (`XYA8934`) is not a valid token. Please use the real one you get from BotFather in the next step.

### 2. Add Your Token and Chat IDs as GitHub Secrets

To keep your token and chat IDs secure, you should add them as secrets to your GitHub repository.

1.  In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2.  Click the **New repository secret** button for each of the secrets below.
3.  Create the following three secrets:

    - **`TELEGRAM_BOT_TOKEN`**: Paste the real API token you got from BotFather here.
    - **`CHAT_ID_1`**: Your Telegram chat ID (`7695772994`).
    - **`CHAT_ID_2`**: Your friend's Telegram chat ID (`8070930921`).

### 3. Enable GitHub Actions

Workflows must be enabled for scheduling to work.

1.  In your GitHub repository, go to the **Actions** tab.
2.  If you see a button that says **"I understand my workflows, go ahead and enable them"**, click it.

That's it! Once you have set the secrets, the bot will start sending questions automatically according to the schedule.
