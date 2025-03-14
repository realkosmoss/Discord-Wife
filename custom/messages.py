import json

MESSAGES_PATH = "messages.json"

class Messages:
    def __init__(self):
        self.messages = self._load_messages()

    def _load_messages(self):
        try:
            with open(MESSAGES_PATH, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get(self):
        return self.messages
    
    def save(self):
        with open(MESSAGES_PATH, 'w') as file:
            json.dump(self.messages, file, indent=4)