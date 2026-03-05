from application.ports import OutputMessagePort, InputMessagePort, RepositoryPort
from Domain.Message import Message

class ReceiveMessageService(InputMessagePort):
    def __init__(self, repository_port: RepositoryPort):
        self.repository_port = repository_port

    def receive_message(self, content: str, user: str):
        message = Message(id=None, content=content, user=user)
        self.repository_port.save_message(message)
        SendMessageService.send_messages()

class SendMessageService:
    def __init__(self, repository_port: RepositoryPort, output_message_port: OutputMessagePort):
        self.repository_port = repository_port
        self.output_message_port = output_message_port

    def send_messages(self):
        messages = self.repository_port.get_all_messages()
        OutputMessagePort.send_messages(self.output_message_port, messages=messages)