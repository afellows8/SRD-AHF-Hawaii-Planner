import streamlit as st
from openai import OpenAI
import csv
import io
import urllib.parse

st.set_page_config(
    page_title="Andrew & Stephanie Hawaii AI Planner",
    page_icon="🌺",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #fff7e6 0%, #e6f7ff 45%, #fffaf0 100%);
    }

    .main-title {
        font-size: 44px;
        font-weight: 800;
        text-align: center;
        color: #1f6f78;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #4f6f70;
        margin-bottom: 25px;
    }

    .section-card {
        background-color: rgba(255, 255, 255, 0.88);
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 22px;
        border: 1px solid #f2d6a2;
    }

    .small-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 14px;
        border-left: 6px solid #ffb703;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }

    .wedding-box {
        background-color: #fff0f3;
        color: #7a1f3d;
        padding: 16px;
        border-radius: 14px;
        border-left: 6px solid #ff6f91;
        font-weight: 600;
        margin-bottom: 20px;
    }

    .footer-note {
        text-align: center;
        color: #5f6f70;
        font-size: 14px;
        margin-top: 30px;
    }

    div.stButton > button {
        background-color: #ff9f1c;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;
    }

    div.stButton > button:hover {
        background-color: #fb8500;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def search_link(site, query):
    encoded = urllib.parse.quote_plus(query)
    if site == "google":
        return f"https://www.google.com/search?q={encoded}"
    if site == "maps":
        return f"https://www.google.com/maps/search/{encoded}"
    if site == "tripadvisor":
        return f"https://www.tripadvisor.com/Search?q={encoded}"
    if site == "yelp":
        return f"https://www.yelp.com/search?find_desc={encoded}"
    return ""


if "saved_ideas" not in st.session_state:
    st.session_state.saved_ideas = []

# SIDEBAR
st.sidebar.title("🌺 Saved Ideas")
st.sidebar.write("Click ideas you like, then build an itinerary from them.")

if st.session_state.saved_ideas:
    for i, idea in enumerate(st.session_state.saved_ideas):
        st.sidebar.markdown(f"**{i+1}. {idea['name']}**")
        st.sidebar.caption(f"{idea['category']} | {idea['island']}")
        if st.sidebar.button(f"Remove #{i+1}", key=f"remove_{i}"):
            st.session_state.saved_ideas.pop(i)
            st.rerun()
else:
    st.sidebar.info("Saved ideas will appear here.")

if st.session_state.saved_ideas:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["name", "category", "island", "notes", "maps_link", "tripadvisor_link", "yelp_link"]
    )
    writer.writeheader()
    writer.writerows(st.session_state.saved_ideas)

    st.sidebar.download_button(
        "⬇️ Download Saved Ideas",
        output.getvalue(),
        "hawaii_saved_ideas.csv",
        "text/csv"
    )

# HEADER
st.image(
    "SRDAHF.png",
    caption="Andrew & Stephanie 🌺",
    use_container_width=True
)

st.markdown('<div class="main-title">🌴 Andrew & Stephanie’s Hawaii AI Planner 🌺</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Find real ideas, save favorites, and build a romantic Hawaii itinerary around the Honolulu wedding.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="wedding-box">💍 Wedding anchor dates: October 7, 8, and 9 in Honolulu, Oahu. The itinerary must keep Andrew and Stephanie in Honolulu for those dates.</div>',
    unsafe_allow_html=True
)

# MAIN LAYOUT
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("✈️ Trip Setup")

    island_count = st.selectbox(
        "How many islands?",
        ["Not Sure - Recommend", "One Island", "Two Islands", "Three Islands"]
    )

    all_islands = ["Oahu", "Maui", "Kauai", "Big Island"]

    if island_count == "One Island":
        selected_islands = st.multiselect("Choose island", all_islands, default=["Oahu"], max_selections=1)
    elif island_count == "Two Islands":
        selected_islands = st.multiselect("Choose two islands", all_islands, default=["Oahu", "Maui"], max_selections=2)
    elif island_count == "Three Islands":
        selected_islands = st.multiselect("Choose three islands", all_islands, default=["Oahu", "Maui", "Kauai"], max_selections=3)
    else:
        selected_islands = []

    before_wedding_days = st.slider("Days in Hawaii before the wedding", 0, 10, 3)
    after_wedding_days = st.slider("Days in Hawaii after the wedding", 0, 10, 4)

    budget = st.selectbox("Budget", ["Budget", "Moderate", "Luxury"])

    vibe = st.multiselect(
        "Vacation style",
        ["Romantic", "Adventure", "Food", "Relaxation", "Hiking", "Snorkeling", "Beaches", "Luxury", "Culture"],
        default=["Romantic", "Food", "Beaches"]
    )

    must_do = st.text_area(
        "Things we absolutely want to do",
        "Snorkeling, great seafood, beach day, romantic sunset dinner"
    )

    flight_preference = st.selectbox(
        "Flight preference",
        ["Delta Only", "Delta Preferred", "Use SkyMiles If Possible", "Best Delta Schedule"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🌊 How This Works")

    st.markdown("""
    <div class="small-card">
    <b>1. Generate ideas</b><br>
    The app suggests activities, restaurants, beaches, hikes, and romantic experiences.
    </div>

    <div class="small-card">
    <b>2. Click and research</b><br>
    Each idea gets Google Maps, Tripadvisor, and Yelp-style search links.
    </div>

    <div class="small-card">
    <b>3. Save favorites</b><br>
    Add the ideas you like to the saved list in the sidebar.
    </div>

    <div class="small-card">
    <b>4. Build itinerary</b><br>
    When you are ready, the AI turns saved ideas into a realistic Hawaii plan.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# IDEA GENERATOR
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🌺 Step 1: Generate Actionable Ideas")

idea_category = st.selectbox(
    "What kind of ideas?",
    ["Activities", "Restaurants", "Romantic Ideas", "Beaches", "Hikes", "Hidden Gems", "All of the Above"]
)

number_of_ideas = st.slider("How many ideas?", 5, 20, 8)

if st.button("🌴 Find Ideas with Links"):

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
Generate {number_of_ideas} succinct Hawaii trip ideas for Andrew and Stephanie.

Context:
- Wedding is October 7, 8, and 9 in Honolulu, Oahu.
- They must be in Honolulu during the wedding dates.
- Stephanie flies Syracuse to Seattle, then they fly together Seattle to Hawaii.
- Hawaii flights should focus on Delta.
- Island count: {island_count}
- Selected islands: {selected_islands}
- Days before wedding: {before_wedding_days}
- Days after wedding: {after_wedding_days}
- Budget: {budget}
- Vacation style: {vibe}
- Must-do items: {must_do}
- Idea category requested: {idea_category}

Return ideas in this exact format:

IDEA NAME:
ISLAND:
CATEGORY:
WHY IT FITS:
WHAT TO CHECK IN REVIEWS:

Keep each idea short and actionable.
Do not invent review scores.
Focus on real places, activities, restaurants, tours, beaches, hikes, and experiences.
"""

    with st.spinner("Finding Hawaii ideas..."):
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )

    st.session_state.latest_ideas_text = response.output_text

if "latest_ideas_text" in st.session_state:
    st.markdown(st.session_state.latest_ideas_text)

    st.subheader("❤️ Save an Idea You Like")

    save_name = st.text_input("Idea name to save")
    save_island = st.selectbox("Island for saved idea", all_islands)
    save_category = st.selectbox(
        "Category for saved idea",
        ["Activity", "Restaurant", "Beach", "Hike", "Romantic Idea", "Hidden Gem", "Flight", "Other"]
    )
    save_notes = st.text_area("Notes for saved idea")

    maps_link = search_link("maps", f"{save_name} {save_island} Hawaii")
    tripadvisor_link = search_link("tripadvisor", f"{save_name} {save_island} Hawaii")
    yelp_link = search_link("yelp", f"{save_name} {save_island} Hawaii")

    if save_name:
        st.markdown(f"[Google Maps]({maps_link}) | [Tripadvisor]({tripadvisor_link}) | [Yelp]({yelp_link})")

    if st.button("❤️ Save This Idea"):
        if save_name.strip():
            st.session_state.saved_ideas.append({
                "name": save_name,
                "category": save_category,
                "island": save_island,
                "notes": save_notes,
                "maps_link": maps_link,
                "tripadvisor_link": tripadvisor_link,
                "yelp_link": yelp_link
            })
            st.success("Saved!")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ITINERARY BUILDER
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🗓️ Step 2: Build Itinerary From Saved Ideas")

if st.button("🌅 Create Itinerary From Saved Ideas"):

    if not st.session_state.saved_ideas:
        st.warning("Save some ideas first.")
    else:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Create a Hawaii itinerary for Andrew and Stephanie using these saved ideas:

{st.session_state.saved_ideas}

Wedding details:
- Wedding is October 7, 8, and 9 in Honolulu, Oahu.
- Keep those days light and based in Honolulu.

Travel logistics:
- Stephanie flies Syracuse to Seattle.
- Andrew and Stephanie fly together round trip Seattle to Hawaii.
- Focus on Delta flight timing and strategy.

Trip settings:
- Days before wedding: {before_wedding_days}
- Days after wedding: {after_wedding_days}
- Island count: {island_count}
- Selected islands: {selected_islands}
- Budget: {budget}
- Style: {vibe}
- Must-do items: {must_do}
- Flight preference: {flight_preference}

Build a practical day-by-day itinerary.
Include:
- Dates
- Islands
- Morning / afternoon / evening plan
- Which saved ideas fit where
- Delta flight strategy
- Inter-island travel notes if needed
- Final recommendation on whether the trip is too rushed or well balanced
"""

        with st.spinner("Building your Hawaii itinerary..."):
            response = client.responses.create(
                model="gpt-5-nano",
                input=prompt
            )

        st.success("Itinerary complete!")
        st.subheader("🌴 Your Hawaii Itinerary")
        st.markdown(response.output_text)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Made for Andrew & Stephanie’s Hawaii adventure 🌺 | Wedding in Honolulu: October 7–9</div>',
    unsafe_allow_html=True
)
