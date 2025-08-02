import os, json, time
from datetime import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
INPUT_JSON_FILENAME = 'event_input.json'
OUTPUT_JSON_FILENAME = 'event_output.json'
PRINT_STATEMENT_SLEEP = 1
WHILE_LOOP_SLEEP = 5

def read_event_data() -> tuple[datetime, datetime, dict]:
    """
    Reads the contents of INPUT_JSON_FILENAME and returns a tuple with
    the new event information and a dictionary of all existing event
    objects. The datetime values of the JSON file must be in the same
    format as the TIMESTAMP_FORMAT global variable.

    :return: Tuple containing the new event's start datetime, 
             end datetime and a dictionary of the user's 
             existing events.
    """

    # Open the JSON file
    json_file = open(INPUT_JSON_FILENAME)

    print("")
    print("Reading event data...")

    # Return JSON object as a dictionary
    json_data = json.load(json_file)

    # Convert all timestamp strings to datetime objects
    json_data['start_datetime'] = datetime.strptime(json_data['start_datetime'], TIMESTAMP_FORMAT)
    json_data['end_datetime'] = datetime.strptime(json_data['end_datetime'], TIMESTAMP_FORMAT)
    for event in json_data['events_list']:
        event['start_datetime'] = datetime.strptime(event['start_datetime'], TIMESTAMP_FORMAT)
        event['end_datetime'] = datetime.strptime(event['end_datetime'], TIMESTAMP_FORMAT)

    # Initialize tuple variables
    start_datetime = json_data['start_datetime']
    end_datetime = json_data['end_datetime']
    events_dict = json_data['events_list']

    # Clear out JSON file contents
    json_file.close()
    json_file = open(INPUT_JSON_FILENAME, "w")
    json_file.truncate(0)

    # Close the JSON file
    json_file.close()

    print(f"Successfully received event data from the Main Program.")
    time.sleep(PRINT_STATEMENT_SLEEP)
    return (start_datetime, end_datetime, events_dict)

def event_conflict_check(start_datetime, end_datetime, events_dict) -> list:
    """
    Iterates through all of the user's events and returns a list
    containing all event objects that conflict with the new event's
    start or end datetime.

    :param start_datetime: New event's start date/time.
    :param end_datetime: New event's end date/time.
    :param events_dict: Dictionary of the user's existing events.

    :return: List containing all event objects that conflict with 
             the new event's start and/or end datetime values.
    """
        
    conflicts_list = []
    print(" ")
    print("Checking events list for conflicts...")

    time.sleep(PRINT_STATEMENT_SLEEP)

    # Create list of events that conflict with the new event
    for event in events_dict:
        if event['start_datetime'] <= start_datetime <= event['end_datetime']:
            print(f"    Conflict Detected: This event overlaps with the \033[36m'{event['event_name']}'\033[0m event on your calendar.")
            conflicts_list.append(event)
            time.sleep(PRINT_STATEMENT_SLEEP)

        elif event['start_datetime'] <= end_datetime <= event['end_datetime']:
            print(f"    Conflict Detected: This event overlaps with the \033[36m'{event['event_name']}'\033[0m event on your calendar.")
            conflicts_list.append(event)
            time.sleep(PRINT_STATEMENT_SLEEP)
    
    return conflicts_list

def write_conflict_data(conflicts_list) -> None:
    """
    Creates JSON object with the Conflict Check results and writes it
    to the OUTPUT_JSON_FILENAME file.

    :param conflicts_list: List containing all event objects that 
                           conflict with the new event's start and/or 
                           end datetime values.

    :return: Tuple containing the new event's start time,end time 
             and a dictionary of the user's existing events.
    """

    output_json = {}

    # Count number of event conflicts
    if len(conflicts_list) == 0:
        print(f"No event conflicts were detected.")
        output_json['conflict_found'] = False
        time.sleep(PRINT_STATEMENT_SLEEP)
    else:
        if len(conflicts_list) == 1:
            print(f"A total of {len(conflicts_list)} Event Conflict was detected.")
        else:
            print(f"A total of {len(conflicts_list)} Event Conflicts were detected.")
        output_json['conflict_found'] = True
        print(" ")
        time.sleep(PRINT_STATEMENT_SLEEP)
    
    # Send event conflict check results to Main Program
    print(f"Sending Event Conflict Checker output to the Main Program...")
    time.sleep(PRINT_STATEMENT_SLEEP)

    output_json['conflicts_list'] = conflicts_list
    output_file = open(OUTPUT_JSON_FILENAME, "w")
    output_file.write(json.dumps(output_json, indent=4, default=str))
    output_file.close()

    print(f"\033[33mSuccessfully sent Event Conflict Checker output to the Main Program!\033[0m")
    print("")
    time.sleep(PRINT_STATEMENT_SLEEP)

# Define the Main Function
def main():
    while True:
        # Checks if file exists
        input_json_exists = os.path.exists(INPUT_JSON_FILENAME) 

        if input_json_exists == True and os.path.getsize(INPUT_JSON_FILENAME) != 0:
            print(f"The file \033[36m'{INPUT_JSON_FILENAME}'\033[0m was found in the directory.")
            time.sleep(PRINT_STATEMENT_SLEEP)

            try:
                results = read_event_data()
            except:
                print("\033[31mERROR: JSON file contains one or more errors.\033[0m")
                print("\033[31mRefer to the README file for more details on the required format.\033[0m")
                print(" ")

                json_file = open(INPUT_JSON_FILENAME, "w")
                json_file.truncate(0)
                json_file.close()

                time.sleep(WHILE_LOOP_SLEEP)
                continue
            
            conflicts_list = event_conflict_check(results[0], results[1], results[2])
            write_conflict_data(conflicts_list)

        time.sleep(WHILE_LOOP_SLEEP)

# Call the Main Function
if __name__=="__main__":
    main()
