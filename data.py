import streamlit as st
import json
import pandas as pd
import plotly.express as px
from collections import Counter

st.set_page_config(page_title="PrivacyLens", layout="wide")

@st.cache_data
def load_data():
    with open("enhanced_data_collected.json", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

st.markdown("""
<style>
    body {
        background-color: #f0f4f8;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-weight: 700;
        margin-bottom: 0.6rem;
    }
    h1 {
        font-size: 2.5rem;
    }
    h2 {
        font-size: 1.8rem;
    }
    h3 {
        font-size: 1.4rem;
    }
    p, li, div {
        font-size: 1.05rem;
    }

    .app-card {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.4rem;
        width: 100%;
        max-width: 400px;
        height: 180px;
        flex: 0 0 auto;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        color: white;
        font-size: 1.15rem;
        text-align: center;
        font-weight: bold;
    }

    .row {
        display: flex;
        width: 100%;
        justify-content: center;
        flex-wrap: nowrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
        box-sizing: border-box;
        overflow-x: auto;
    }

    .footer {
        margin-top: 3rem;
        padding: 1rem;
        font-size: 0.9rem;
        color: #555;
        text-align: center;
        border-top: 1px solid #ccc;
    }

    @media (max-width: 1024px) {
        .row { width: 90%; gap: 0.4rem; }
        .app-card { max-width: 300px; height: 160px; font-size: 0.9rem; }
    }
    @media (max-width: 768px) {
        .row { width: 100%; flex-wrap: wrap; justify-content: center; }
        .app-card { max-width: 45%; height: 160px; font-size: 0.85rem; }
    }
    @media (max-width: 480px) {
        .row { flex-direction: column; width: 100%; gap: 0.75rem; }
        .app-card { max-width: 100%; height: auto; min-height: 140px; font-size: 0.8rem; margin: 0.25rem 0; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;'>PrivacyLens</h1>
<p style='text-align:center;'>Explore how your data is handled by trending social apps in India</p>
""", unsafe_allow_html=True)


tab = st.radio("", ["App-Wise View", "Data Collections", "Stay Protected"], horizontal=True)

if tab == "App-Wise View":
    st.markdown("<h3 class='section-header'>App-Wise Privacy Details</h3>", unsafe_allow_html=True)
    app_names = sorted([app.get("app_name", app["app_id"]).capitalize() for app in data])
    sel = st.selectbox("Select an App", [""] + app_names)

    bright = ['#FF6B6B','#FFD93D','#6BCB77','#4D96FF','#A66DD4','#FF8FAB','#00C2D1','#FF9F1C','#9B5DE5','#F15BB5']
    for i, app in enumerate(data):
        name = app.get("app_name", app["app_id"]).capitalize()
        if sel and sel.lower() != name.lower():
            continue
        st.markdown(f"<h4 style='text-align:center;'>{name}</h4>", unsafe_allow_html=True)
        cards = {
            "Data Collected": ", ".join(app.get("collected", [])) or "Not Specified",
            "Shared With": ", ".join(app.get("shared_with", [])) or "Not Specified",
            "Encrypted": app.get("encrypted", "Unknown"),
            "User Control": app.get("user_control", "Unknown"),
            "Purpose": ", ".join(app.get("purpose", [])) or "Not Specified",
            "Retention": app.get("retention_period", "Unknown"),
            "SDK Count(Third party apps) Estimated": app.get("third_party_sdk_count", "Unknown"),
            "App ID": app.get("app_id", "Unknown")
        }
        keys = list(cards.keys())
        mid = 5
        rows = [keys[:mid], keys[mid:]]
        for row_keys in rows:
            st.markdown("<div class='row'>", unsafe_allow_html=True)
            for j, key in enumerate(row_keys):
                val = cards[key]
                color = bright[(i * len(keys) + keys.index(key)) % len(bright)]
                st.markdown(f"<div class='app-card' style='background-color:{color};'><b>{key}</b><br>{val}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif tab == "Data Collections":
    st.markdown("<h3 style='text-align:center;'>App Data Collection Process</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Understand how each app collects data — simplified for all users</p>", unsafe_allow_html=True)

    app_names = sorted([app.get("app_name", app["app_id"]).capitalize() for app in data])
    sel = st.selectbox("Select an App", [""] + app_names)

    flashcards = {
        "Instagram": [
            "📸 Uses your camera input to apply face filters and analyze engagement.",
            "📍 Collects GPS and background location for reels & ad targeting.",
            "📱 Tracks in-app activity — likes, scroll behavior, stories viewed.",
            "🔗 Integrates Facebook SDK to collect cross-platform data.",
            "🗣️ Records voice input and usage during Reels or Lives."
        ],
        "Whatsapp": [
            "📇 Accesses your contact list to auto-populate messaging options.",
            "📊 Collects metadata — who you chat with, how often, and when.",
            "🛰️ Tracks IP, OS version, and battery level for diagnostics.",
            "💾 Syncs media shared (images/audio) for cloud backup.",
            "🔐 Doesn’t access message content (E2E encrypted), but collects usage stats."
        ],
        "Facebook": [
            "🧑‍💻 Captures all profile info, posts, likes, comments, and photos.",
            "🌐 Tracks off-platform browsing via Facebook Pixel.",
            "📍 Monitors real-time location to show local events & ads.",
            "🗂️ Gathers device identifiers, cookies, and connection info.",
            "📱 Records app activity like scrolling speed and reading time."
        ],
        "Twitter": [
            "📝 Tracks tweets, retweets, quote tweets, and engagement time.",
            "📍 Collects location when geotagging is enabled.",
            "🔎 Logs search queries and hashtags followed.",
            "📲 Captures device data and app version.",
            "🎯 Uses ad interaction behavior to tailor promoted tweets."
        ],
        "Snapchat": [
            "🎭 Uses face mapping through AR lenses in real-time.",
            "📸 Continuously accesses camera and mic for content creation.",
            "📡 Collects GPS data for geo-filters and nearby stories.",
            "🧠 Tracks snap views, screenshot attempts, and story replays.",
            "🔗 SDK links with Bitmoji and Snap Ads to collect cross-data."
        ],
        "Telegram": [
            "📱 Only collects phone number and basic device data.",
            "👥 Syncs contact list to show known Telegram users.",
            "🌐 Stores IP address for session control and security.",
            "🔐 Doesn’t track message content or usage analytics.",
            "🛡️ End-to-end encrypted messages for secret chats only."
        ],
        "YouTube": [
            "📺 Tracks watch history and video interactions (likes/comments).",
            "🔍 Analyzes search queries and autocomplete usage.",
            "🧠 Records pause/skip/rewatch behavior for recommendations.",
            "🎤 Collects voice input if enabled for search.",
            "🌐 Shares data across Google services for ad targeting."
        ],
        "Linkedin": [
            "💼 Collects work history, resume uploads, and application data.",
            "📲 Tracks scroll behavior, profile views, and job clicks.",
            "🎯 Uses ad interaction to profile user intent and interest.",
            "🧑‍🤝‍🧑 Monitors connection network and message metadata.",
            "🧠 Analyzes typing speed and mouse movement for fraud detection."
        ],
        "Sharechat": [
            "📍 Detects region and language preference automatically.",
            "📱 Collects content interactions like shares, likes, time spent.",
            "🎙️ Uses voice inputs for regional content engagement.",
            "📡 Tracks device info, connection strength, and location.",
            "🎯 Pushes regional trend-based suggestions using behavior modeling."
        ],

        "Messenger": [
            "📞 Accesses call logs and audio for call features.",
            "📨 Collects contacts and chat metadata.",
            "📲 Tracks active status and message timing.",
            "🔗 Integrates with Facebook data to create unified profiles.",
            "🔒 Chats may be encrypted depending on user settings."
        ],
        "Tiktok": [
            "📹 Uses camera, mic, and device motion sensors.",
            "📍 Collects device location and usage patterns.",
            "🎯 Tracks watch history and user preferences for algorithmic feeds.",
            "🧠 Learns user behavior via interaction timing and content pauses.",
            "📦 Shares data with advertisers and partners via embedded SDKs."
        ],
        "Bigo live": [
            "📸 Constant camera/mic usage during live streams.",
            "🌐 IP address and device data logged for moderation.",
            "📊 Tracks interactions — likes, comments, gifts.",
            "🔔 Collects push notification tokens and activity sessions.",
            "🎤 Analyzes voice and screen content for violations or ads."
        ]
    }

    card_colors = ["#FCE4EC", "#FFF3E0", "#E3F2FD", "#F1F8E9", "#F0F4C3", "#EDE7F6", "#FFEBEE", "#E8F5E9", "#FFFDE7", "#E0F7FA"]

    if sel:
        st.markdown(f"<h4 style='text-align:center;'>{sel} - Data Collection </h4>", unsafe_allow_html=True)
        for i, point in enumerate(flashcards.get(sel, ["No detailed data available for this app."])):
            st.markdown(f"""
            <div style="
                background-color: {card_colors[i % len(card_colors)]};
                padding: 1rem 1.25rem;
                margin: 1rem auto;
                border-radius: 12px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                font-size: 1.1rem;
                line-height: 1.6;
                width: 100%;
                max-width: 850px;
            ">
                {point}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Please select an app to view how it collects your data.")

else:
    st.markdown("<h3 class='section-header'>Stay Protected: Tips & Tech News</h3>", unsafe_allow_html=True)
    st.markdown("""
    <ul>
      <li><b>Limit Permissions:</b> Only necessary access—esp. camera, mic, location.</li><br>
      <li><b>Review Settings:</b> Check permissions and privacy controls periodically.</li><br>
      <li><b>Use Privacy-Friendly Apps:</b> Eg: Signal instead of mainstream messengers.</li><br>
      <li><b>Avoid Social Logins:</b> Reduces cross-app tracking.</li><br>
      <li><b>Clear Data Often:</b> Especially for apps you rarely use.</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("### Data Privacy News")
    news = [
        ("Instagram rolls out new privacy dashboard in India", "https://economictimes.indiatimes.com/news/international/us/instagram-launches-new-teen-accounts-with-privacy-controls-amid-growing-concerns/articleshow/113436849.cms"),
        ("WhatsApp updates location-sharing controls globally", "https://faq.whatsapp.com/6780014865351544"),
        ("Facebook fined over data policy violations", "https://www.nytimes.com/2023/05/22/business/meta-facebook-eu-privacy-fine.html"),
        ("Snapchat introduces encrypted backups", "https://www.socialsamosa.com/2019/01/snapchat-end-to-end-encryption/"),
        ("Twitter tightens data retention rules for user DMs", "https://economictimes.indiatimes.com/tech/technology/twitter-restricts-dms-for-unverified-accounts-to-reduce-spam/articleshow/102034511.cms?")
    ]
    for title, link in news:
        st.markdown(f"- [{title}]({link})")

st.markdown("""
<div class="footer">
    © 2025 PrivacyLens. All rights reserved.
</div>
""", unsafe_allow_html=True)
