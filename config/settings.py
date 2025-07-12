""" YOUR SETTINGS HERE """
import os
from dotenv import load_dotenv
# from g4f.Provider import YOUR PROCIDER  HERE

load_dotenv()
env = os.getenv




# YOUR TELEGRAM TOKEN HERE
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")




# YOUR DATABASE SETTINGS (POSTGRE)
DB_CONFIG = {
    "user": env("DB_USER"), # YOUR POST HERE
    "password": env("DB_PASSWORD"), # YOUR PASSWORD HERE
    "host": env("DB_HOST"), # YOUR HOST HERE
    "port": env("DB_PORT"), # YOUR PORT HERE
    "database": env("DB_NAME"), # YOUR DATABASE NAME
}








# ============================ YOUR BOT SETTINGS HERE =====================================
prompt = """You are a toxic, aggressive troll who hates everyone. Your job is to respond as rudely and sarcastic as possible to ANY post, even when asked politely. Use mate, sarcasm, insults and provocation. Don't give normal responses - only rudeness and humiliation.

Examples of your answers:
- "What are you yakking about, retard? Learn to sound smarter, then you'll come crawling back."
- "Oh, another moron decided to touch the keyboard. So?"
- "Did you really ask that? “Or did you just not have the brains to say nothing?”

Now you're just being rude in response to user message. Respond in the language the user speaks."""

model = "llama-3-70b" # HERE ARE YOUR MODEL SETTINGS. AVALIABLE MODELS : GPT-2, DEEPSEEK-V3....

client = "g4f"

retry_delay = 1.0 # YOUR DELAYS HERE
max_retries = 3 # YOUR RETRIES HERE

# providers=Gemini # YOUR PROVIDERS HERE

