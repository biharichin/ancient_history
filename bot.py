import os
import re
import requests
import time

# --- Configuration ---
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# A list of chat IDs to send the polls to.
# The script will retrieve up to 10 chat IDs from environment variables (CHAT_ID_1, CHAT_ID_2, etc.)
CHAT_IDS = [os.getenv(f"CHAT_ID_{i}") for i in range(1, 11) if os.getenv(f"CHAT_ID_{i}")]

QUESTIONS_FILE = "ancient.txt"
PROGRESS_FILE = "progress.txt"
QUESTIONS_PER_DAY = 20

# --- Functions ---

def parse_questions(filename):
    """Parses the MCQ file into a list of question objects."""
    questions = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []

    # Split the file content into blocks for each question.
    # Each question block is separated by one or more blank lines.
    question_blocks = re.split(r'\n\s*\n', content.strip())

    for block in question_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 6:
            continue

        question_text = lines[0]
        options = [re.sub(r'^[a-d]\)\s*', '', line) for line in lines[1:5]]
        
        # Extract the correct answer letter and find its index
        answer_line = lines[5]
        match = re.search(r'Answer:\s*([a-d])', answer_line, re.IGNORECASE)
        if not match:
            continue
        
        correct_option_letter = match.group(1).lower()
        correct_option_index = ord(correct_option_letter) - ord('a')

        if 0 <= correct_option_index < len(options):
            questions.append({
                "question": question_text,
                "options": options,
                "correct_option_index": correct_option_index
            })
            
    return questions

def get_progress():
    """Reads the index of the next question to send."""
    try:
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def update_progress(index):
    """Saves the index of the next question to send."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))

def send_poll(chat_id, question_data):
    """Sends a single question as a quiz poll to a specified chat."""
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
    
    payload = {
        'chat_id': chat_id,
        'question': question_data['question'],
        'options': question_data['options'],
        'type': 'quiz',
        'correct_option_id': question_data['correct_option_index'],
        'is_anonymous': False  # So you can see who answers
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Poll sent successfully to chat_id: {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending poll to {chat_id}: {e}")
        print(f"Response body: {response.text}")


def send_message(chat_id, text):
    """Sends a simple text message."""
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Message sent successfully to chat_id: {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to {chat_id}: {e}")

# --- Main Execution ---

if __name__ == "__main__":
    if not CHAT_IDS:
        print("Error: No chat IDs provided. Please set CHAT_ID_1, CHAT_ID_2, etc. as environment variables.")
    else:
        all_questions = parse_questions(QUESTIONS_FILE)
        start_index = get_progress()

        if not all_questions:
            print("No questions found in the file. Exiting.")
        elif start_index >= len(all_questions):
            print("All questions have been sent.")
            for chat_id in CHAT_IDS:
                send_message(chat_id, "no question, we done")
        else:
            end_index = min(start_index + QUESTIONS_PER_DAY, len(all_questions))
            questions_to_send = all_questions[start_index:end_index]
            
            print(f"Sending questions {start_index + 1} to {end_index}...")

            for i, question_data in enumerate(questions_to_send):
                for chat_id in CHAT_IDS:
                    print(f"Sending question {start_index + i + 1} to chat {chat_id}")
                    send_poll(chat_id, question_data)
                    # Add a small delay between polls to avoid hitting rate limits
                    time.sleep(2) 
            
            # Update progress for the next run
            update_progress(end_index)
            print("Daily questions sent. Progress updated.")
