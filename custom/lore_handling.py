import json
import os

class LoreHandling:
    def __init__(self, user, channelid):
        self.user = user # Should be userid based.
        self.messages_file = f"custom/user/{channelid}.json"
        self.channels_file = f"custom/user/{self.user}_channels.json"
        self.channels = self._load_channels()
        self.messages = self._load_messages()

    def _load_messages(self):
        if os.path.exists(self.messages_file):
            try:
                with open(self.messages_file, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError):
                return []
        return []

    def _load_channels(self):
        if os.path.exists(self.channels_file):
            try:
                with open(self.channels_file, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError):
                return []
        return []

    def get(self):
        return self.messages
    
    def save(self):
        """Saves messages"""
        with open(self.messages_file, 'w') as file:
            json.dump(self.messages, file, indent=4)
    
    def save_channels(self):
        with open(self.channels_file, 'w') as file:
            json.dump(self.channels, file, indent=4)

    def save_all(self):
        self.save()
        self.save_channels()

    def delete(self):
        """Deletes the whole message json (No return)"""
        if os.path.exists(self.messages_file):
            os.remove(self.messages_file)