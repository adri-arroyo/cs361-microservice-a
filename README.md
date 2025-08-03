
# CS361-Microservice-A

The objective of this project was to create a fully functional Microservice meant to be integrated within an event planner web application. The Microservice receives the datetime information of a new event to be created, along with a list of events that currently exist in the user's calendar. The Microservice check if any of the existing events overlap with the new event's datetime, or if no conflicts are found. A response indicating if conflicts were detected will be sent back to the main program together with a list of conflicts (if any were found).

# Features

+ **Data Validation:** When the data request is received, the microservice will validate the contents of the JSON file to ensure that the JSON object is in the required format before proceeding with the event conflict checks.
+ **Color Coded CLI Text:** The microservice will print text on the terminal to indicate if the request was successfully received, if any conflicts were found, and if the output was successfully sent back to the main program. Certain print statements also include color-coding to highlight important sections within the print statement.
+ **Control Execution Speed:** Users can control the execution speed of the program by changing the values of the PRINT_STATEMENT_SLEEP global variable, which adds a delay after each print statement, or the WHILE_LOOP_SLEEP global variable which determines the sleep time between data request loops.
+ **Customizable filenames:** Users can change the name of the default input/output JSON files used to communicate with the microservice by changing the value of the INPUT_JSON_FILENAME / OUTPUT_JSON_FILENAME global variables.
+ **Customizable datetime format:** Users can customize the datetime format of the JSON file datetime objects by changing the value of the TIMESTAMP_FORMAT global variable.

Below are the default values of the global variables used by the microservice:
```
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
INPUT_JSON_FILENAME = 'event_input.json'
OUTPUT_JSON_FILENAME = 'event_output.json'
PRINT_STATEMENT_SLEEP = 1
WHILE_LOOP_SLEEP = 5
```

## Getting Started
The communication pipeline between the Main Program and the Microservice will be performed by reading/writing JSON files. A JSON object containing the new event's start datetime, end datetime and the list of event objects must be read by the Microservice for it to check for conflicts.

Below is an example of the required format of the JSON object to be sent to the Microservice.

```
{
  "start_datetime": "YYYY-MM-DD HH:MM:SS",
  "end_datetime": "YYYY-MM-DD HH:MM:SS",
  "events_list": [
    {
      "event_name"    : "EXISTING EVENT NAME 01",
      "start_datetime": "YYYY-MM-DD HH:MM:SS",
      "end_datetime"  : "YYYY-MM-DD HH:MM:SS"
    },
    {
      "event_name"    : "EXISTING EVENT NAME 02",
      "start_datetime": "YYYY-MM-DD HH:MM:SS",
      "end_datetime"  : "YYYY-MM-DD HH:MM:SS"
    },
    {
      "event_name"    : "EXISTING EVENT NAME 03",
      "start_datetime": "YYYY-MM-DD HH:MM:SS",
      "end_datetime"  : "YYYY-MM-DD HH:MM:SS"
    }
  ]
}

```

Make sure that the **event_input.json** and **event_output.json** files are in the same directory as **event_conflict_check.py** before executing the microservice.

After checking for conflicts, the microservice will write the resulting JSON object into the **event_output.json** file. The JSON object will contain a boolean response equal to TRUE if conflicts were found, otherwise it will equal false. If conflicts were found, the JSON object will contain a list of all event objects that conflict with the new event that is being created, sorted in ascending order from least time conflict to most time conflict. 

(Time conflict refers to the amount of hours in overlap between the new event that is being created and the existing event.)

Below is an example of the format of the JSON object that is sent as a response from the Microservice.

```
{
    "conflict_found": true,
    "conflicts_list": [
        {
            "event_name"    : "EXISTING EVENT NAME 01",
            "start_datetime": "YYYY-MM-DD HH:MM:SS",
            "end_datetime"  : "YYYY-MM-DD HH:MM:SS",
            "conflict_time": 0.5
        },
        {
            "event_name"    : "EXISTING EVENT NAME 01",
            "start_datetime": "YYYY-MM-DD HH:MM:SS",
            "end_datetime"  : "YYYY-MM-DD HH:MM:SS",
            "conflict_time": 1.5
        },
        {
            "event_name"    : "EXISTING EVENT NAME 01",
            "start_datetime": "YYYY-MM-DD HH:MM:SS",
            "end_datetime"  : "YYYY-MM-DD HH:MM:SS",
            "conflict_time": 2.0
        }
    ]
}

```

## How to REQUEST data from the Microservice
To request data from the Microservice, your Main Program must write the JSON object containing the new event's start and end datetime, along with the list of the user's existing events to the **event_input.json** file.

In a terminal separate from your main program, move to the directory where the **event_conflict_check.py** is located and execute it by running the following command:
```
py event_conflict_check.py
```

Next, request data from the microservice by writing the JSON object to the **event_input.json** file. An example call would be the following:

```
import json 

json_data = { JSON OBJECT }

with open("event_input.json", "w") as event_input:
    event_input.write(json.dumps(json_data, indent=4, default=str))

```
Another example call would be the following: 

```
import json 

json_data = { JSON OBJECT }

event_input = open('event_input.json', "w")
event_input.write(json.dumps(json_data, indent=4, default=str))
event_input.close()
```
Once the request is received through the microservice, the terminal for the microservice will print out a statement indicating that the event data was received from the Main Program.

## How to RECEIVE data from the Microservice
The microservice will automatically write the event conflict checker results to the **event_output.json** once it finishes executing. A message will also be displayed on the terminal indicating that the data was successfully sent to the Main Program. 

To access the output data, your main program must open the JSON file and read its contents. For easier data segregation, you can intialize the data through indexing  by key-value pairs as per the following example.

```
import json 

with open('event_output.json', 'r') as event_output:
    json_data = json.load(event_output)
    conflict_found = json_data['conflict_found']
    conflicts_list = json_data['conflicts_list']
```
Another example call would be the following: 
```
import json 

event_output = open('event_output.json', 'r')
json_data = json.load(event_output)

conflict_found = json_data['conflict_found']
conflicts_list = json_data['conflicts_list']

event_output.close()

```

## Testing the Microservice

The program can be tested using the provided *test_program.py* file to ensure that it meets the requirements and behaves as expected. 

## UML Sequence Diagram for the Microservice

<img alt="UML Diagram for Event Conflict Checker (Microservice A)" src="https://github.com/adri-arroyo/cs361-microservice-a/blob/main/Microservice_A_UML_Diagram.png" />

## Acknowledgements

This project was developed as part of the course CS361 - Software Engineering I, at Oregon State University.


