import json

from channels.generic.websocket import WebsocketConsumer


from print_pp.logging import Print


from .phrases import generate_options

class GamePlayConsumer(WebsocketConsumer):

    def connect(self):    
        self.current_phrases = generate_options()
        self.accept()


    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))