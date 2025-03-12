# Don't Frustrate Dave - Voice Assistant for Cognitive Support

This Pythonista script implements a voice-controlled assistant designed to provide cognitive support for individuals facing challenges with information processing and focus. Specifically, it was created with veterans like Dave in mind, who may experience cognitive impairments.

## Overview

"Don't Frustrate Dave" integrates speech recognition, OpenAI's GPT-3.5-turbo, and the OpenWeather API to provide a range of functionalities, including:

* **Voice-Controlled Question Answering:** Leverages OpenAI to respond to user inquiries.
* **Weather Updates:** Retrieves and vocalizes current weather conditions.
* **Call and Messaging Integration:** Facilitates hands-free calling and text messaging through iOS native features.
* **Simple UI:** Provides a clean and easy-to-navigate interface.

## Features

* **Configurable API Keys:** Uses `assistant_config.json` to securely store API keys for OpenAI and OpenWeather.
* **Robust Error Handling:** Implements comprehensive error handling to minimize user frustration.
* **Threading for API Calls:** Uses threading to prevent UI freezing during API requests.
* **Logging:** Logs all interactions and errors to `assistant.log` for debugging.
* **Humorous Design:** Integrates lighthearted elements to reduce stress and enhance user engagement.

## Prerequisites

* Pythonista for iOS
* OpenAI API Key
* OpenWeather API Key

## Setup

1.  Clone or download the repository.
2.  Create an `assistant_config.json` file in the same directory as the script with the following structure:

    ```json
    {
        "OPENAI_API_KEY": "your_openai_api_key",
        "OPENWEATHER_API_KEY": "your_openweather_api_key",
        "OPENAI_MODEL": "gpt-3.5-turbo",
        "WEATHER_LOCATION": "Austin, TX"
    }
    ```

3.  Open the script in Pythonista and run it.

## Usage

* Use voice commands such as "Ask a question," "Get weather," "Make a call," and "Send a message."
* Utilize the on-screen buttons for the same functions.
* The program will provide spoken and visual feedback.

## Contributing

Contributions are welcome! Please submit pull requests or open issues for feature requests or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgments

* OpenAI for the GPT-3.5-turbo API.
* OpenWeather for the weather API.
* The Pythonista community for their support.

## Contact

For questions or support, please open an issue on GitHub.
