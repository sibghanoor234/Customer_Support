import json


def read_tickets_json_file():
    try:
        with open("tickets.json", "r") as f:
            try:
                tickets_list = json.load(f)
                print(tickets_list)
            except Exception as e:
                print(str(e))
                return []
        return tickets_list
    except Exception as e:
        print(str(e))
        return []
