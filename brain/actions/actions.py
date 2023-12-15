# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text

from rasa_sdk.events import UserUtteranceReverted, ConversationPaused, FollowupAction
from utils import ask_llm




class ClassifyIntent(Action):

    def name(self) -> Text:
        return "action_classify_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ranking = tracker.latest_message['intent_ranking']

        for intent in ranking:
            name = intent['name']
            confidence = int(intent['confidence']*100)
            print(f'Confidence of intent {name} is {confidence}%.')
        # dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionItemAvailabilityCheck(Action):

    def name(self) -> Text:
        return "action_item_availability_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name =  tracker.get_slot('product_name')

        if product_name:
            dispatcher.utter_message(text=f'{product_name} is available')
        else:
            dispatcher.utter_message(text=f'No product name found!')

        return []

class ActionOrderStatusCheck(Action):

    def name(self) -> Text:
        return "action_order_status_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id =  tracker.get_slot('order_id')

        if order_id:
            dispatcher.utter_message(text=f'{order_id} is available')
        else:
            dispatcher.utter_message(text=f'No order id found!')

        return []
    
class ActionOutOfScope(Action):

    def name(self) -> Text:
        return "action_out_of_scope"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message =  tracker.latest_message

        if user_message:
            response = ask_llm(user_message, channel='huggingface')
            # print(user_message)
            # response = 'test'
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f'Currently I am not able to answer it! I am still learning...')

        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # tell the user they are being passed to a customer service agent
        
        # assume there's a function to call customer service
        # pass the tracker so that the agent has a record of the conversation between the user
        # and the bot for context
        # call_customer_service(tracker)
        latest_message = tracker.latest_message
        dispatcher.utter_message(text=f"your message {latest_message} is being passed to open ai bot...")
     
        # pause the tracker so that the bot stops responding to user input
        return [ConversationPaused(), UserUtteranceReverted()]