import json
user_input = 0

while user_input != 1 or user_input != 2:
    user_input = int(input("Which JSON File do you wish to 'send' to Microservice A?\nEnter 1 for conflict_true.json, or 2 for conflict_false.json: "))

    if user_input == 1:
        json_file = open('conflict_true.json')
        json_data = json.load(json_file)
        json_file.close()

        output_file = open('event_input.json', "w")
        output_file.write(json.dumps(json_data, indent=4, default=str))
        output_file.close()
        break

    elif user_input == 2:
        json_file = open('conflict_false.json')
        json_data = json.load(json_file)
        json_file.close()

        output_file = open('event_input.json', "w")
        output_file.write(json.dumps(json_data, indent=4, default=str))
        output_file.close()
        break

    else:
        print ("Invalid user input.")