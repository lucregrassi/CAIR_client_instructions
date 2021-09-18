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

# Location of the server
server_IP = "131.175.198.134"
BASE = "http://" + server_IP + ":5000/"

# If the client is new create a file in which its state will be stored
if not os.path.exists("state.txt"):
    resp = requests.put(BASE + "CAIR_server", verify=False)
    state = resp.json()['client_state']
    # Save the client state contained in the response in a file
    with open("state.txt", 'wb') as f:
        pickle.dump(state, f)
    # Welcome the user and start the conversation
    print("S: Welcome to CAIR!")
    print("S:", resp.json()['reply'])
# If the client is not new start the conversation
else:
    print("S: I missed you. What would you like to talk about?")


def main():
    while True:
        # Wait for the user to write something
        sentence = input("U: ")
        # Load the array containing all information about the state of the client
        with open("state.txt", 'rb') as cl_state:
            client_state = pickle.load(cl_state)
        # Perform the request to the server, sending both the sentence and the client state
        response = requests.get(BASE + "CAIR_server/" + sentence, data=json.dumps(client_state), verify=False)
        # Update the client state data structure with the one contained in the response
        client_state = response.json()['client_state']
        # print(client_state)
        # Update the client state in the file
        with open("state.txt", 'wb') as cl_state:
            pickle.dump(client_state, cl_state)
        # Retrieve the other fields of the server response
        intent_reply = response.json()['intent_reply']
        plan = response.json()['plan']
        reply = response.json()['reply']

        if intent_reply:
            if plan:
                reply = intent_reply + " " + plan + " " + reply
            else:
                reply = intent_reply + " " + reply

        # Print the reply
        print("S:", reply)


if __name__ == '__main__':
    main()
