"""
Author:      Lucrezia Grassi
Email:       lucrezia.grassi@edu.unige.it
Affiliation: Laboratorium, DIBRIS, University of Genoa, Italy
Project:     CAIR

This file contains an example of client for the CAIR server
"""

import requests
import os
import pickle
import json
import time
import zlib

# Location of the API (the server it is running on)
server_IP = "131.175.205.146"
BASE = "http://" + server_IP + ":5000/CAIR_hub"


def retrieve_user_state():
    resp = requests.put(BASE, verify=False)
    dialogue_state = resp.json()['dialogue_state']
    if not dialogue_state:
        print("S: Waiting for CAIR_dialogue service...")
        # Keep on trying to perform requests to the server until it is reachable.
        while not dialogue_state:
            resp = requests.put(BASE, verify=False)
            dialogue_state = resp.json()['dialogue_state']
            time.sleep(1)
    # If the client is not new
    if os.path.exists("dialogue_state.txt"):
        print("S: Welcome back!")
        print("S: I missed you. What would you like to talk about?")
    else:
        with open("dialogue_state.txt", 'wb') as f:
            pickle.dump(dialogue_state, f)
        print("S: Hey, you're new!")
        print("S:", resp.json()['reply'])


def start_dialogue():
    while True:
        sentence = input("U: ")
        # Load the array containing all information about the state of the client
        with open("dialogue_state.txt", 'rb') as cl_state:
            dialogue_state = pickle.load(cl_state)
        data = {"sentence": sentence, "dialogue_state": dialogue_state}
        encoded_data = json.dumps(data).encode('utf-8')
        compressed_data = zlib.compress(encoded_data)
        response = requests.get(BASE, data=compressed_data, verify=False)
        dialogue_state = response.json()['dialogue_state']
        if dialogue_state:
            with open("dialogue_state.txt", 'wb') as cl_state:
                pickle.dump(dialogue_state, cl_state)
        intent_reply = response.json()['intent_reply']
        plan = response.json()['plan']
        reply = response.json()['reply']

        reply = intent_reply + " " + plan + " " + reply
        print("S:", reply)


if __name__ == '__main__':
    retrieve_user_state()
    start_dialogue()
