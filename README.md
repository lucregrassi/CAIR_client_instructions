# CAIR client tutorial
This repository contains a simple Python script that allows everyone to interact with the CAIR server.  
By running the script you can have an entertaining dialogue with our system for autonomous conversation.

**Requirements**: Make sure you have Python3 installed on your device.

**Note**: no data related to the client is stored on the server.

## How does it work?
Launch the script by opening the terminal in the script folder and typing:
```
$ python3 CAIR_client_example.py
```
The first thing that the script does is to check if a file called *state.txt* exists in the same folder of the script. 
* If no file is present, the script assumes that the client is new and it has never made a request to the server.  
  A PUT request is performed to the server to get the initial state and start the conversation. This request does not require any parameter.  
  The json response contains two fields:
  ```
  client_state
  reply
  ```
  The script creates the **state.txt** file and stores the received initial client state in it, then a welcome message and the first server sentence are shown to the user.
* If the file is already present, it means that the client has already interacted with the server and its last state is stored in this file.  
  In this case, the script just shows a welcome back message and it encourages the user to talk about something.
  
Each time the user writes something, the script retrieves the client data from the *state.txt* file and performs a GET request to the server. This request expects the sentence as parameter and the client state as additional data which is then used by the server to provide the appropriate response.  
The response provided by the GET request contains four fields:
```
client_state
intent_reply
plan
reply
```
The updated client state is immediately stored in the *state.txt*, while the strings contained in the other three fields are used to make up the sentence which is then shown to the user. In particular:
* The *intent_reply* is a specific response to the user request of executing a task 
* The *plan* is the actual sequence of actions and related parameters that the client should execute following a user request
* The *reply* is the reply of the system

## How can you develop your custom client?
A client for the CAIR server can be developed for any device equipped with a microphone/keyboard and a speaked/screen to acquire and provide speech or text.  
The example script provided in this repository can be used as a starting point for implementing a client for any device.  
The only thing that should be customized is the way in which the client performs the actions contained in the **plan** field of the response to the GET request.

For the complete list of actions and parameters consult the following guide: <fare pdf con lista di tutti gli intent + trigger sentences + plan>

For an example of client for the SoftBank Robotics' Pepper and Nao robots that manages all the actions received by the server, please refer to: https://github.com/lucregrassi/CAIRclient

