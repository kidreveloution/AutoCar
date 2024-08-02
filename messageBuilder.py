import json
from typing import Any, Dict

class MESSAGE_CLASS:
    def __init__(self, address: str, msg_name: str, dest: str, content: Dict[str, Any]):
        """
        Initializes the message builder with the necessary attributes.

        Args:
            address (str): The address of the sender.
            msg_name (str): The name of the message.
            dest (str): The destination address of the message.
            content (Dict[str, Any]): The content of the message, as a dictionary.
        """
        self.address = address
        self.msg_name = msg_name
        self.dest = dest
        self.content = content  # content is expected to be a dictionary or any JSON-serializable object
    
    def buildMessage(self) -> str:
        """
        Builds the message as a JSON string.

        Returns:
            str: The JSON-encoded message.
        """
        message = {
            'address': self.address,
            'dest': self.dest,
            'msg_name': self.msg_name,
            'content': self.content  # content is already a JSON-serializable object
        }
        return json.dumps(message)

# Example usage
content_data = {
    "subject": "Meeting Reminder",
    "body": "Don't forget about the meeting at 3 PM.",
    "attachments": ["agenda.pdf", "minutes.docx"]
}

msg_builder = MESSAGE_CLASS(
    address="123 Main St",
    msg_name="Notification",
    dest="john.doe@example.com",
    content=content_data
)

json_message = msg_builder.buildMessage()
print(json_message)
