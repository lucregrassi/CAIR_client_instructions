# CAIR client example
This repository contains a simple Python script that allows everyone to interact with the CAIR server.  
By running the script you can have an entertaining dialogue with our system for autonomous conversation.

**Requirements**: 
```
Python 3.x
pip
requests
```
The latest stable version of Python 3 can be downloaded from the official website: [download Python 3.9.6](https://www.python.org/downloads/release/python-396/).   
Usually, pip is automatically installed along with Python. However, if you have Python but not pip, you can install it by following this guide: [pip documentation](https://pip.pypa.io/en/stable/installation/).  
To install the requests package, open the terminal and type:
```
pip install requests
```

**Note**: as the server is implemented as a REST API, no data related to the client is stored on the server.

## How does it work?
Launch the script by opening the terminal in the script folder and typing:
```
$ python CAIRclient.py
```
The first thing that the script does is to check if a file called *dialogue_state.json* exists in the same folder of the script. 
* If no file is present, the script assumes that the client is new and it has never made a request to the server.  
  A GET request is performed to the server to get the initial state and start the conversation. This request does not require any parameter.  
  The json response contains two fields:
  ```
  dialogue_state
  first_sentence
  ```
  The script creates the **dialogue_state.json** file and stores the received initial client state in it, then a welcome message and the first server sentence are shown to the user.
* If the file is already present, it means that the client has already interacted with the server and its last state is stored in this file.  
  In this case, the script just shows a welcome back message and it encourages the user to talk about something.
  
Each time the user writes something, the script retrieves the client data from the *dialogue_state.json* file and performs a PUT request to the server. This request expects the sentence as parameter and the client state as additional data which is then used by the server to provide the appropriate response.  
The response provided by the PUT request contains four fields:
```
dialogue_state
plan_sentence
plan
dialogue_sentence
```
The updated client state is immediately stored in the *dialogue_state.json*, while the strings contained in the other three fields are used to make up the sentence which is then shown to the user. In particular:
* The *plan_sentence* is a specific response to the user request of executing a task 
* The *plan* is the actual sequence of actions and related parameters that the client should execute following a user request
* The *dialogue_sentence* is the reply of the system

**Note**: to delete all client data and restart the conversation from zero, it is sufficient to remove the *dialogue_state.json* file before launching the script.

## How can you develop your custom client?
A client for the CAIR server can be developed for any device equipped with a microphone/keyboard and a speaker/screen to acquire and provide speech or text.  
The example script provided in this repository can be used as a starting point for implementing a client for any device.  
The only thing that should be customized is the way in which the client performs the actions contained in the **plan** field of the response to the PUT request.

For the current list of Intents with their plan and corresponding parameters consult Chapter 2.1 of the following guide: [CAIR_Developer_Guide_Plans.pdf](https://github.com/lucregrassi/CAIRclient_example/files/7039311/CAIR_Developer_Guide_Plans.pdf)


For an example of client for the SoftBank Robotics' Pepper and Nao robots that manages all the actions received by the server, please refer to: https://github.com/lucregrassi/SoftBank_CAIRclient/tree/main

