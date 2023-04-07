import json
import threading


from time import sleep
from asgiref.sync import sync_to_async


from channels.generic.websocket import WebsocketConsumer


from phrases.models.models import StoryTopic
from phrases.generator import PhraseGenerator


from gameplay.codes import (
    Code, BKFirstPhrasesGenerated, BKNotEnoughPhrasesToReturn, BKTopicNotSelected, BKTopicSelected,
    FNReturnPentagonPhrases, FNReturnMonoPhrase, FNSelectTopic
)


from print_pp.logging import Print



BACKEND_CODES_INFORMATION = {
    "BGT-200": "Topic selected",
    "BGT-400": "Topic not selected",

    "BGP-200": "First phrases generated",
    "BGP-205": "Not enough phrases to return",
}


FRONTEND_CODES_INFORMATION = {
    "FGT-101": "Select topic",

    "FGP-100": "Start phrase generation",
    "FGP-101": "Returns 5 phrases",
    "FGP-102": "Returns 1 phrases",
}


class GamePlayConsumer(WebsocketConsumer):

    MAX_OPTIONS_TO_GENERATE = 10


    def __init__(self, *args, **kwargs):
        self.current_topic = None
        self.codes = {
            FNSelectTopic.code: self.set_current_topic,
            FNReturnPentagonPhrases.code: self.return_phrases,
            FNReturnMonoPhrase.code: self.return_phrases,
        }
        super().__init__(*args, **kwargs)
        self.phrases_generator = PhraseGenerator(self.current_topic, testing=True)


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
                self.send_response(code=BKFirstPhrasesGenerated)
                is_first_time = False

    
    def return_phrases(self, data:dict):
        

        if data['code'] == FNReturnMonoPhrase.code:
            options_to_return = 1
        elif data['code'] == FNReturnPentagonPhrases.code:
            options_to_return = 5

        if not self.options:
            self.send_response(code=BKNotEnoughPhrasesToReturn)
            return

        with self.options_lock:
            self.send_response(code=BKFirstPhrasesGenerated, extra_data={"options": self.options[:options_to_return]})
            self.options = self.options[5:]


    def set_current_topic(self, data:dict):
        
        topic_id = data['topic_id']

        if topic_id == "NONE":
            self.current_topic = None
            return

        try: 
            self.current_topic = StoryTopic.objects.get(id=topic_id).name
        except: 
            self.send_response(code=BKTopicNotSelected)

        self.send_response(code=BKTopicSelected, extra_data={"topic_name": self.current_topic})

    
    def send_response(self, code:Code, extra_data:dict=None):

        data = {"code": code.code}
        
        if extra_data: 
            data.update(extra_data)
        
        self.send(text_data=json.dumps(data))

