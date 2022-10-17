"""
Author:      Lucrezia Grassi
Email:       lucrezia.grassi@edu.unige.it
Affiliation: Laboratorium, DIBRIS, University of Genoa, Italy
Project:     CAIR

This file contains an example of client for the CAIR server
"""

import requests
import os
import json
import time
import zlib

# Location of the API (the server it is running on)
server_IP = "131.175.205.146"
BASE = "http://" + server_IP + ":5000/CAIR_hub"


def retrieve_user_state():
    resp = requests.get(BASE, verify=False)
    dialogue_state = resp.json()['dialogue_state']
    if not dialogue_state:
        print("S: Waiting for CAIR_dialogue service...")
        # Keep on trying to perform requests to the server until it is reachable.
        while not dialogue_state:
            resp = requests.get(BASE, verify=False)
            dialogue_state = resp.json()['dialogue_state']
            time.sleep(1)
    # If the client is not new
    if os.path.exists("dialogue_state.json"):
        print("S: Welcome back! What would you like to talk about?")
    else:
        with open("dialogue_state.json", 'w') as f:
            json.dump(dialogue_state, f)
        print("S: Welcome to CAIR! It's nice to meet you.")
        print("S:", resp.json()['first_sentence'])


def start_dialogue():
    while True:
        sentence = input("U: ")
        # Load the array containing all information about the state of the client
        with open("dialogue_state.json", 'r') as cl_state:
            dialogue_state = json.load(cl_state)
        data = {"client_sentence": sentence, "dialogue_state": dialogue_state}
        encoded_data = json.dumps(data).encode('utf-8')
        compressed_data = zlib.compress(encoded_data)
        response = requests.put(BASE, data=compressed_data, verify=False)
        dialogue_state = response.json()['dialogue_state']
        if dialogue_state:
            with open("dialogue_state.json", 'w') as cl_state:
                json.dump(dialogue_state, cl_state)
        intent_reply = response.json()['plan_sentence']
        plan = response.json()['plan']
        reply = response.json()['dialogue_sentence']

        reply = intent_reply + " " + plan + " " + reply
        print("S:", reply.strip())


if __name__ == '__main__':
    retrieve_user_state()
    start_dialogue()
