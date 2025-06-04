# Voice Cooking Assistant

A web-based cooking assistant that helps you find and follow recipes using voice commands. The application features voice recognition for recipe search and voice narration for step-by-step cooking instructions.

## Features

- Voice-controlled recipe search
- Recipe narration with text-to-speech
- Ingredient-based recipe filtering
- Cuisine type filtering
- Detailed recipe view with instructions
- Modern, responsive web interface

## Technologies Used

- Backend:
  - Python 3.x
  - Flask
  - SQLAlchemy
  - OpenAI API
  - SpeechRecognition

- Frontend:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
  - Web Speech API
  - jQuery

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd voice-cooking-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_openai_api_key
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:8081`

## Usage

1. **Voice Search**:
   - Click the microphone button
   - Speak your recipe request
   - Results will appear automatically

2. **Recipe Narration**:
   - View a recipe
   - Click "Narrate Recipe" to start voice instructions
   - Use "Stop Narration" to stop the narration

3. **Manual Search**:
   - Type in the search bar
   - Add ingredients to filter results
   - Select cuisine type from the dropdown

## Project Structure

```
voice-cooking-assistant/
├── app.py              # Flask application
├── main.py            # Core functionality
├── models.py          # Database models
├── requirements.txt   # Python dependencies
├── static/           # Static files
│   ├── css/         # Stylesheets
│   └── js/          # JavaScript files
└── templates/        # HTML templates
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. # Maya_the_cooking_AI
