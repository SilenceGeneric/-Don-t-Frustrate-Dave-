import ui
import speech
import requests
import threading
import json
import logging
import objc
import datetime

# === Configuration & Environment Variables ===
CONFIG_FILE = "assistant_config.json"
DEFAULT_CONFIG = {
    "OPENAI_API_KEY": "",
    "OPENWEATHER_API_KEY": "",
    "OPENAI_MODEL": "gpt-3.5-turbo",
    "WEATHER_LOCATION": "Austin, TX"
}

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# Check if API keys are missing
if not config["OPENAI_API_KEY"] or not config["OPENWEATHER_API_KEY"]:
    raise ValueError("API keys for OpenAI and Weather are required in assistant_config.json")

# === Logging Configuration ===
LOG_FILE = "assistant.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variables for conversation and reminders.
conversation_history = []

# === Speech Functions ===
def speak(text):
    logging.info(f"Speaking: {text}")
    speech.say(text)

def listen_for_commands():
    while True:
        try:
            text = speech.recognize()
            if text:
                process_voice_command(text.lower())
        except Exception as e:
            logging.error(f"Error recognizing speech: {e}")

def process_voice_command(command):
    if 'question' in command:
        ask_question()
    elif 'weather' in command:
        get_weather()
    elif 'call' in command:
        make_call()
    elif 'message' in command:
        send_message()
    elif 'help' in command:
        provide_help()
    elif 'close' in command:
        close_app()

# === OpenAI (ChatGPT) Integration ===
def ask_question():
    question = speech.recognize()
    if not question:
        speak("No question provided.")
        return
    conversation_history.append({"role": "user", "content": question})
    
    def call_openai():
        try:
            response_data = api_request(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {config['OPENAI_API_KEY']}"},
                json_data={
                    "model": config["OPENAI_MODEL"],
                    "messages": conversation_history,
                    "max_tokens": 150,
                    "temperature": 0.7,
                }
            )
            if response_data and "choices" in response_data and len(response_data["choices"]) > 0:
                answer = response_data["choices"][0]["message"]["content"].strip()
                conversation_history.append({"role": "assistant", "content": answer})
                speak(answer)
                feedback_label.text = "Ready for next command."
            else:
                feedback_label.text = "Error: No valid response from AI."
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            speak("I couldn't get an answer right now.")
            feedback_label.text = "Error: AI request failed."
    
    threading.Thread(target=call_openai).start()
    feedback_label.text = "Processing... (Question)"

# === Weather API ===
def get_weather():
    try:
        weather_data = api_request(
            f"http://api.openweathermap.org/data/2.5/weather?q={config['WEATHER_LOCATION']}&appid={config['OPENWEATHER_API_KEY']}"
        )
        if weather_data and "main" in weather_data and "weather" in weather_data:
            main = weather_data["main"]
            temp = main["temp"] - 273.15  # Convert Kelvin to Celsius
            desc = weather_data["weather"][0]["description"]
            weather_report = f"The weather is {desc} with a temperature of {temp:.2f}°C."
            speak(weather_report)
            feedback_label.text = "Ready for next command."
        else:
            speak("I couldn't fetch the weather information.")
            feedback_label.text = "Error: Weather data not found."
    except Exception as e:
        logging.error(f"Weather API error: {e}")
        speak("I couldn't get the weather right now.")
        feedback_label.text = "Error: Weather API failed."

# === Call and Message Functions ===
def make_call():
    contact_name = speech.recognize()
    if contact_name:
        speak(f"Calling {contact_name}")
        # iOS Call functionality using objc
        try:
            url = f"tel://{contact_name}"
            objc_util.open_url(url)
        except Exception as e:
            logging.error(f"Error calling {contact_name}: {e}")
            speak(f"Failed to call {contact_name}.")
            feedback_label.text = f"Error: Call failed to {contact_name}."
    else:
        speak("Please specify a contact name.")
        feedback_label.text = "Error: No contact name specified."

def send_message():
    contact_name = speech.recognize()
    if contact_name:
        speak(f"Sending message to {contact_name}")
        message = speech.recognize()
        if message:
            speak(f"Message: {message}")
            # iOS SMS functionality using objc
            try:
                sms_url = f"sms:{contact_name}&body={message}"
                objc_util.open_url(sms_url)
            except Exception as e:
                logging.error(f"Error sending message to {contact_name}: {e}")
                speak(f"Failed to send message to {contact_name}.")
                feedback_label.text = f"Error: Message failed to {contact_name}."
        else:
            speak("Please specify the message.")
            feedback_label.text = "Error: No message specified."
    else:
        speak("Please specify a contact name.")
        feedback_label.text = "Error: No contact name specified."

# === Help Menu ===
def provide_help():
    help_text = "I can help you with various tasks like asking questions, getting weather information, making calls, sending messages, and more."
    speak(help_text)
    feedback_label.text = "Ready for next command."

# === Close the App ===
def close_app():
    speak("Goodbye!")
    feedback_label.text = "Goodbye!"
    # Terminate the program.
    exit()

# === UI Setup ===
def create_ui():
    main_view = ui.View()
    main_view.name = "Voice Assistant"
    main_view.background_color = 'white'

    # Large buttons
    button_size = (200, 50)

    # Ask Question button
    ask_button = ui.Button(frame=(20, 100, *button_size))
    ask_button.title = "Ask a Question"
    ask_button.action = lambda sender: ask_question()
    main_view.add_subview(ask_button)

    # Weather button
    weather_button = ui.Button(frame=(20, 170, *button_size))
    weather_button.title = "Get Weather"
    weather_button.action = lambda sender: get_weather()
    main_view.add_subview(weather_button)

    # Call button
    call_button = ui.Button(frame=(20, 240, *button_size))
    call_button.title = "Make a Call"
    call_button.action = lambda sender: make_call()
    main_view.add_subview(call_button)

    # Message button
    message_button = ui.Button(frame=(20, 310, *button_size))
    message_button.title = "Send Message"
    message_button.action = lambda sender: send_message()
    main_view.add_subview(message_button)

    # Close button
    close_button = ui.Button(frame=(20, 380, *button_size))
    close_button.title = "Close"
    close_button.action = lambda sender: close_app()
    main_view.add_subview(close_button)

    # Feedback label
    feedback_label = ui.Label(frame=(20, 450, 280, 50))
    feedback_label.text = "Ready for next command."
    feedback_label.alignment = ui.ALIGN_CENTER
    feedback_label.font = ('<System>', 16)
    main_view.add_subview(feedback_label)

    return main_view

# === Main Program Execution ===
def main():
    global feedback_label
    ui_view = create_ui()
    ui_view.present('sheet')
    feedback_label = ui_view['feedback_label']
    listen_for_commands()

if __name__ == "__main__":
    main()
