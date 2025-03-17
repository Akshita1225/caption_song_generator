from flask import Flask, render_template, request
import os
from PIL import Image
import random
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64

# Ensure necessary resources are downloaded
nltk.download('stopwords')

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up Spotify API
SPOTIPY_CLIENT_ID = "d48f514a873145dd8059b91b21e71651"
SPOTIPY_CLIENT_SECRET = "6fc3e06d70b04c44ab6f896bb7109aa8"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Function to extract keywords from user input
def extract_keywords(text):
    words = text.lower().split()
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords[:3]  # Limit to 3 main keywords

# Function to detect emotion from a description
def detect_emotion(text):
    sentiment = sentiment_analyzer(text)[0]
    return "happy" if sentiment['label'] == "POSITIVE" else "melancholic"

# Function to generate captions without BLIP
def generate_caption(image_path, user_keywords=""):
    image = Image.open(image_path).convert("RGB")

    # Placeholder method for describing the image (you can integrate an image-to-text model here)
    image_caption = "Aesthetic view with vibrant colors"  # Example placeholder text

    # Extract emotion & keywords
    emotion = detect_emotion(image_caption)
    keywords = extract_keywords(user_keywords)

    # Caption styles for different vibes
    caption_templates = [
        f"This pic screams {emotion} vibes ✨",
        f"{random.choice(['Slay', 'Mood', 'Vibe check'])} 😎 #Aesthetic",
        f"{' '.join(keywords)} - That’s the energy we need!",
        f"Just me, my {random.choice(keywords) if keywords else 'vibe'}, and the moment 💫",
        f"{random.choice(['Lost in the moment', 'Feeling myself', 'Unreal vibes'])} 😍",
        f"POV: You're living your best life ❤️",
        f"When life gives you {random.choice(keywords) if keywords else 'a moment'}... capture it! 📸"
    ]

    return random.sample(caption_templates, k=random.randint(5, 7))  # Return 5-7 captions

# Function to recommend a song based on the caption
def recommend_song(caption):
    results = sp.search(q=caption, limit=1, type='track')

    if results["tracks"]["items"]:
        return results["tracks"]["items"][0]["external_urls"]["spotify"]

    return "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH"  # Default song

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["image"]
        caption_style = request.form["caption_style"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            caption = generate_caption(filepath, caption_style)
            song_link = recommend_song(caption[0])

            return render_template("index.html", image=filepath, caption=caption, song=song_link)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)