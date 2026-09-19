Study Forge ⚔️

Live App: studyforgeapp.streamlit.app <-- (Click to try it out live!)

    ⚠️ Warning: Gemini API Rate Limits
    The live application runs on the free tier of the Google Gemini API, which has strict rate limits. If you are playing around with the app and it hangs or throws a rate-limit message, just give it about 60 seconds to cool down and try generating your study guide again!

The Backstory

Ended up naming this project Study Forge because I'm a big fan of medieval games, and "forging" something just felt right for crafting study materials from scratch. Originally, I just wanted to experiment and build an AI-powered application, but I didn't know what to make. I realized that since I'm currently grinding through my Computer Science degree and my sister is tackling her Nursing program, we were constantly handing each other flashcards. I figured the best way to put this Gemini API to work was to build us an automated study partner. It helped me actually put a real project into use, rather than just building something that sits on a hard drive.
Core Features

Instead of making something super corporate, I built the features around how my sister and I actually study:

    Custom Study Guides: You just toss in your syllabus or a class objective, and the AI hammers out a customized review sheet so you know what to focus on.

    Interactive Flashcards: We used to hand each other physical cards. Now, the app forces the AI to output raw JSON, which gets parsed into a clean drop-down UI for active recall testing.

    Exam Simulator: This generates a 15-question multiple-choice practice test. I wired up an automated grading system into the Streamlit widgets, so we can actually get a final score and review the explanations when we get an answer wrong.

    Rate-Limit Catcher: Added a quick safety net so the app politely tells you to wait 60 seconds instead of violently crashing if we hit the Google free-tier limits.

Tech Stack

    Frontend: Streamlit (Python) with custom injected CSS to give it an industrial, dark-mode terminal vibe.

    Backend: Python 3.9

    AI Integration: Google Generative AI (Gemini 3 Flash), strictly prompted to enforce JSON data schemas.

Installation & Setup

If you want to run this locally:

    Clone the repository and navigate to the directory:

Bash

git clone https://github.com/Shanils123/Study_Forge.git
cd Study_Forge

    Create a virtual environment and install dependencies:

Bash

python3 -m venv venv
source venv/bin/activate
pip install streamlit google-generativeai

    Create a .streamlit/secrets.toml file in the root directory and drop in your API key:

Ini, TOML

GEMINI_API_KEY = "your_api_key_here"

    Fire up the forge:

Bash

streamlit run app.py
