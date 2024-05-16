from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import os

# Define the DataStore function outside the Action classes
def DataStore(full_name, ph_1, mail):
    new_row = pd.DataFrame([[full_name, ph_1, mail]],
                           columns=["full_name", "ph_1", "mail"])
    if os.path.isfile("user_data.xlsx"):
        df = pd.read_excel("user_data.xlsx")
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel("user_data.xlsx", index=False)
    else:
        new_row.to_excel("user_data.xlsx", index=False)
    return []

class ActionExtractData(Action):

    def name(self) -> Text:
        return "action_extract_data"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve each slot individually
        first_name = tracker.get_slot('first_name')
        last_name = tracker.get_slot('last_name')
        ph_1 = tracker.get_slot('Phone_number')
        mail = tracker.get_slot('Mail')

        # Combine first name and last name
        full_name = f"{first_name} {last_name}"

        dispatcher.utter_message(text=f"Here are the details: \
                                        \nname: {full_name}\
                                        \nphone number: {ph_1}\
                                        \nemail: {mail}")

        return []

class ActionSaveData(Action):

    def name(self) -> Text:
        return "action_save_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        first_name = tracker.get_slot('first_name')
        last_name = tracker.get_slot('last_name')
        ph_1 = tracker.get_slot('Phone_number')
        mail = tracker.get_slot('Mail')

        # Call the DataStore function with the combined full name
        DataStore(full_name=f"{first_name} {last_name}", ph_1=ph_1, mail=mail)

        dispatcher.utter_message(text="Data Stored Successfully")

        return []

 
