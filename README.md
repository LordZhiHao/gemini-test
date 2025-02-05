# Gemini Translation App

A web application that provides translation services using Google's Gemini AI model. Built with FastAPI backend and Vue.js frontend.

![Translation Interface](./assets/translation-interface.png)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/vue-3.0+-green.svg)](https://vuejs.org/)

## Features
- Text translation between multiple languages
- Real-time translation using Gemini AI
- Responsive design using Vuetify components
- User-friendly interface
- Error handling and loading states
- Mobile-responsive layout

## Screenshots
![Mobile View](./assets/mobile-view.png)
![Translation Demo](./assets/translation-demo.gif)

## Prerequisites
- Python 3.8+
- Node.js and npm
- Google Gemini API key
- Git

## Tech Stack
### Backend
- FastAPI
- LangChain
- Google Gemini AI
- Python-dotenv
- Uvicorn

### Frontend
- Vue 3
- Vuetify
- TypeScript
- Axios
- Vite

## Setup and Installation

### Backend Setup
1. Clone the repository
```bash
git clone https://github.com/LordZhiHao/gemini-test.git
cd gemini-test


Create and activate virtual environment

python -m venv venv

# Windows
.\venv\Scripts\activate

# Unix or MacOS
source venv/bin/activate


Install Python dependencies

pip install fastapi uvicorn python-dotenv langchain-google-genai


Create .env file in the backend directory and add your Gemini API key

GEMINI_API_KEY=your_api_key_here


Run the FastAPI server

uvicorn main:app --reload

The backend server will run on http://localhost:8000


Frontend Setup

Navigate to the frontend directory

cd frontend


Install dependencies

npm install


Run the development server

npm run dev

The frontend will be available at http://localhost:5173


Usage

Select the source language from the "From" dropdown
Select the target language from the "To" dropdown
Enter the text you want to translate in the left textarea
Click the "Translate" button
The translated text will appear in the right textarea

API Documentation

Translation Endpoint

POST /translate/

Request Body

{
    "input_language": "English",
    "output_language": "Spanish",
    "text_input": "Hello, how are you?"
}

Response

{
    "translated_text": "Hola, ¿cómo estás?"
}

Project Structure

gemini-test/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── types/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts
└── README.md

Troubleshooting

Common Issues

CORS Error

# Update FastAPI CORS settings in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API Key Issues

Ensure .env file is in the correct location
Check if API key is valid
Verify environment variable is loaded correctly


Node Module Issues

# Remove node_modules and reinstall
rm -rf node_modules
npm install

Development

Running Tests

# Backend tests
pytest

# Frontend tests
npm run test

Building for Production

# Frontend build
npm run build

Deployment

Build the frontend

npm run build


Set up production server (e.g., Nginx)
Configure environment variables
Run backend with production server (e.g., Gunicorn)

Contributing

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

License

This project is licensed under the MIT License - see the LICENSE file for details.


Contact

Your Name - @your_twitter


Project Link: https://github.com/LordZhiHao/gemini-test


Acknowledgments

Google Gemini AI
Vue.js Team
FastAPI Team
Vuetify Team


This comprehensive README includes:
- Project overview and features
- Installation instructions
- Usage guide
- API documentation
- Project structure
- Troubleshooting guide
- Development instructions
- Contribution guidelines
- License information
- Contact details
- Acknowledgments

Remember to:
1. Replace placeholder images with actual screenshots
2. Update contact information
3. Add actual license file
4. Update project structure if different
5. Add specific troubleshooting steps based on common iss
