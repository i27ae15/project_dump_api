import json
import threading


from time import sleep


from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


from phrases.models.models import StoryTopic
from phrases.generator import PhraseGenerator


from print_pp.logging import Print



BACKEND_CODES_INFORMATION = {
    "BGT-200": "Topic selected",
    "BGT-400": "Topic not selected",

    "BGP-200": "Initial phrases generated",
    "BGP-205": "Initial phrases still not generated",
}


FRONTEND_CODES_INFORMATION = {
    "FGT-101": "Select topic",

    "FGP-100": "Generate initial phrases requested",
    "FGP-101": "Initial phrases requested",
    "FGP-102": "Next phrases requested",
}


class GamePlayConsumer(WebsocketConsumer):

    MAX_OPTIONS_TO_GENERATE = 10

    def __init__(self, *args, **kwargs):
        self.current_topic = None
        self.codes = {
            "FGT-101": self.set_current_topic,
            "FGP-101": self.return_initial_phrases,
            "FGP-102": self.return_next_phrase,
        }
        super().__init__(*args, **kwargs)
        self.phrases_generator = PhraseGenerator(self.current_topic)


    def connect(self):
        self.options:list = list()
        self.options_lock = threading.Lock()
        self.accept()
        

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
       
        if text_data_json["code"] == 'FGP-100':
            threading.Thread(target=self.generate_phrases).start()
            return

        self.codes[text_data_json["code"]](text_data_json)


    def generate_phrases(self) -> list[str]:
        is_first_time = True
        while True:
            sleep(2)
            options_to_generate = self.MAX_OPTIONS_TO_GENERATE - len(self.options)
            if is_first_time: options_to_generate = 5

            if options_to_generate < 0:
                continue
            
            with self.options_lock:
                options = self.phrases_generator.generate_phrases(num_phrases=options_to_generate)
                self.options.extend(options)
            
            if is_first_time:
                self.send(text_data=json.dumps({"code": "G200"}))
                is_first_time = False

    
    def return_initial_phrases(self, data:dict):

        if not self.options:
            self.send(text_data=json.dumps({"code": "G205"}))
            return

        with self.options_lock:
            self.send(text_data=json.dumps({"code": "G200", "options": self.options[:5]}))
            self.options = self.options[5:]

    
    def return_next_phrase(self, data:dict):

        if not self.options:
            self.send(text_data=json.dumps({"code": "G205"}))
            return

        with self.options_lock:
            self.send(text_data=json.dumps({"code": "G200", "options": self.options[:1]}))
            self.options = self.options[1:]
    

    def set_current_topic(self, data:dict):
        
        topic_id = data['topic_id']

        if topic_id == "NONE":
            self.current_topic = None
            return

        try: self.current_topic = StoryTopic.objects.get(id=topic_id).spanish_name
        except: self.send(text_data=json.dumps({"code": "BGT-404"}))

        self.send(text_data=json.dumps({"code": "BGT-200"}))
