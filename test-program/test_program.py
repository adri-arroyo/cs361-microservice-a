import json, os, time

# Prompt user for input
user_input = int(input("Which JSON File do you wish to 'send' to Microservice A?\nEnter 1 for conflict_true.json, or 2 for conflict_false.json: "))

# Assigns JSON object to be written into the event_input.json file
if user_input == 1:
    input_filename = 'test-program\conflict_true.json'
elif user_input == 2:
    input_filename = 'test-program\conflict_false.json'
else:
    print ("Invalid user input.")
    exit()

# Deletes current contents of event_output.json
with open('event_output.json', 'w') as event_output:
    event_output.truncate(0)

# Initializes JSON object to write to event_input.json 
json_file = open(input_filename)
json_data = json.load(json_file)
json_file.close()

# Writes JSON object to event_input.json 
output_file = open('event_input.json', "w")
output_file.write(json.dumps(json_data, indent=4, default=str))
output_file.close()

# Refreshes while the Microservice A executes
while os.path.getsize('event_output.json') == 0:
    time.sleep(5)

# Reads the Microservice A's response from event_output.json
with open('event_output.json', 'r') as event_output:
    json_data = json.load(event_output)
    conflict_found = json_data['conflict_found']
    conflicts_list = json_data['conflicts_list']

# Prints the results
if conflict_found:
    print("")
    print("At least one event conflict was detected. :(")
    print("The following events conflict with the event that is being added:")
    print("")
    for event in conflicts_list:
        print(f"Event Name: {event['event_name']}\nStart Time: {event['start_datetime']}\nEnd Time: {event['end_datetime']}\nConflict Time: {event['conflict_time']}")
        print("")
else:
    print("No event conflicts were found. :)")

