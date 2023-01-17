import re
import datetime
import win10toast
import threading

def find_closest_match(pattern, text):
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)

    # Get the current date and time
    now = datetime.datetime.now()

    # Set the minimum difference to the maximum possible value
    min_difference = datetime.timedelta.max

    # Set the closest match to None
    closest_match = None

    # Iterate over the matches
    for match in matches:
        # Parse the date and time from the match
        date = datetime.datetime.strptime(match, '%Y-%m-%d %H:%M:%S')

        # Calculate the difference between the current date and time and the match
        difference = abs(date - now)

        # If the difference is smaller than the minimum difference, set the closest match to the current match
        if difference < min_difference:
            min_difference = difference
            closest_match = match

    # Return the closest match
    return closest_match

def extract_command(file):
    # Read the Markdown file
    with open(file, 'r') as f:
        text = f.read()

    # Extract the command from the text
    pattern = r'\*\*(.+?)\*\*'
    match = find_closest_match(pattern, text)

    if match:
        # Split the command into time and message
        time, message = match.group(1).split(';')

        # Strip leading and trailing whitespace from the time and message
        time = time.strip()
        message = message.strip()

        return time, message

    return None, None

def launch_alarm(file):
    # Create a ToastNotifier object
    toaster = win10toast.ToastNotifier()

    # Extract the command from the Markdown file
    time, message = extract_command(file)

    if time and message:
        # Parse the time and display a notification
        alarm_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        toaster.show_toast("Alarm", message, alarm_time)
    else:
        print("Command not found")

def run_alarm_thread(file):
    # Create a ToastNotifier object
    toaster = win10toast.ToastNotifier()

    # Extract the command from the Markdown file
    time, message = extract_command(file)

    # Set the current alarm to None
    current_alarm = None

    # Run the loop indefinitely
    while True:
        # If the current alarm is None or has already gone off, extract the next command from the file
        if not current_alarm or current_alarm < datetime.datetime.now():
            time, message = extract_command(file)
            current_alarm = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        # Calculate the time until the next alarm
        time_until_alarm = current_alarm - datetime.datetime.now()

        # Sleep for the time until the next alarm
        time.sleep(time_until_alarm.total_seconds())

        # Display the notification
        toaster.show_toast("Alarm", message, current_alarm)
def run_alarm(file):
    # Create a ToastNotifier object
    toaster = win10toast.ToastNotifier()

    # Extract the command from the Markdown file
    time, message = extract_command(file)

    # Set the current alarm to None
    current_alarm = None

    # Run the loop indefinitely
    while True:
        # If the current alarm is None or has already gone off, extract the next command from the file
        if not current_alarm or current_alarm < datetime.datetime.now():
            time, message = extract_command(file)
            current_alarm = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        # Calculate the time until the next alarm
        time_until_alarm = current_alarm - datetime.datetime.now()

        # Sleep for the time until the next alarm
        time.sleep(time_until_alarm.total_seconds())

        # Display the notification
        toaster.show_toast("Alarm", message, current_alarm)

# Run the alarm
#run_alarm('alarm.md')

# Create a thread to run the alarm in the background
#alarm_thread = threading.Thread(target=run_alarm_thread, args=('alarm.md',))

# Start the thread
#alarm_thread.start()

#launch_alarm('alarm.md')


# example of md file
#**2022-01-01 00:00:00; Wake up!**
#It's time to start your day.
