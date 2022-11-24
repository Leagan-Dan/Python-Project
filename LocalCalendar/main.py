import json
import logging
from datetime import datetime

from icalendar import Calendar


def configure_log():
    logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                        format="%(asctime)s %(message)s")


def menu():
    logging.info("[Info] started the menu")
    print("Choose the type of file you want to use: (ICS/JSON) [1/2]:")
    choice_input = input()
    logging.info("[Info] Chose the type of input")

    if choice_input == "1":
        print("Enter the path to the ICS file:")
        try:
            events = read_ics(input())
        except IOError:
            error = IOError("[Error] Couldn't read the ICS from the given path")
            logging.error(error)
            raise error
    elif choice_input == "2":
        print("Enter the path to the JSON file:")
        try:
            events = read_json(input())
        except IOError:
            error = IOError("[Error] Couldn't read the JSON from the given path")
            logging.error(error)
            raise error
    else:
        error = IOError("[Error] Choose 1 or 2 for ICS or JSON")
        logging.error(error)
        raise error
    logging.info("[Info] Read the events from the given file")

    print("Choose the format of the alerts: (Screen/File) [1/2]:")
    choice_output = input()
    logging.info("[Info] Chose the type of output")
    if choice_output == "1":
        generate_alerts_screen(events)
    elif choice_output == "2":
        print("Enter the directory path to the new file:")
        path = input()
        try:
            generate_alerts_file(events, path)
            print("Created Alerts.txt")
        except OSError:
            error = OSError("[Error] Couldn't generate file at the given path")
            logging.error(error)
            raise error
    else:
        error = IOError("[Error] Choose 1 or 2 for Screen or File")
        logging.error(error)
        raise error
    logging.info("[Info] Generated alerts")


def read_ics(path):
    g = open(path, 'rb')
    gcal = Calendar.from_ical(g.read())
    events = []
    for component in gcal.walk():
        event_information = {}
        if component.name == "VEVENT":
            event_information["summary"] = str(component.get('summary'))
            event_information["dtstart"] = component.get('dtstart').dt.strftime("%d-%m-%y %H:%M:%S")
            event_information["dtend"] = component.get('dtend').dt.strftime("%d-%m-%y %H:%M:%S")
            event_information["dtstamp"] = component.get('dtstamp').dt.strftime("%d-%m-%y %H:%M:%S")
            event_information["location"] = str(component.get('location'))
            events.append(event_information)
    g.close()
    return events


def read_json(path):
    f = open(path)
    try:
        data = json.load(f)
    except ValueError:
        error = ValueError("[Error] JSON-decoding has failed")
        logging.error(error)
        raise error

    event_information = {}
    events = []

    for element in data["events"]:
        summary = element['summary']
        dtstart_str = element['dtstart']
        dtend_str = element['dtend']
        dtstamp_str = element['dtstamp']
        location = element['location']

        dtstart = datetime.strptime(dtstart_str, "%Y%m%dT%H%M%SZ").strftime("%d-%m-%y %H:%M:%S")
        dtend = datetime.strptime(dtend_str, "%Y%m%dT%H%M%SZ").strftime("%d-%m-%y %H:%M:%S")
        dtstamp = datetime.strptime(dtstamp_str, "%Y%m%dT%H%M%SZ").strftime("%d-%m-%y %H:%M:%S")

        event_information["summary"] = summary
        event_information["dtstart"] = dtstart
        event_information["dtend"] = dtend
        event_information["dtstamp"] = dtstamp
        event_information["location"] = location

        events.append(event_information)
    f.close()
    return events


def generate_alerts_screen(events):
    for event in events:
        if datetime.strptime(event["dtstart"], "%d-%m-%y %H:%M:%S") > datetime.now():
            print()
            print("EVENT ALERT")
            for key in event.keys():
                if event[key]:
                    if key == "summary":
                        print(f"Summary is: {event[key]}")
                    elif key == "dtstart":
                        print(f"Start time is : {event[key]}")
                    elif key == "dtend":
                        print(f"End time is: {event[key]}")
                    elif key == "dtstamp":
                        print(f"Time stamp is: {event[key]}")
                    elif key == "location":
                        print(f"Location is: {event[key]}")

def generate_alerts_file(events, path):
    f = open(path + "\\Alerts.txt", "w")
    for event in events:
        if datetime.strptime(event["dtstart"], "%d-%m-%y %H:%M:%S") > datetime.now():
            f.write("EVENT ALERT\n")
            for key in event.keys():
                if event[key]:
                    if key == "summary":
                        f.write(f"Summary is: {event[key]}")
                    elif key == "dtstart":
                        f.write(f"Start time is : {event[key]}")
                    elif key == "dtend":
                        f.write(f"End time is: {event[key]}")
                    elif key == "dtstamp":
                        f.write(f"Time stamp is: {event[key]}")
                    elif key == "location":
                        f.write(f"Location is: {event[key]}")
                f.write("\n")
    f.close()

if __name__ == '__main__':
    configure_log()
    logging.debug("[Debug] Configured logging")
    print(read_ics('D:\git\Python\LocalCalendar\leaganndanut@gmail.com.ics'))
    print(read_json('D:\git\Python\LocalCalendar\calendar.json'))
    menu()
