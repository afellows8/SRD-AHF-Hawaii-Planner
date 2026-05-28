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

st.sidebar.title("❤️ Saved Ideas")

if st.session_state.saved_ideas:
    for i, idea in enumerate(st.session_state.saved_ideas):
        st.sidebar.markdown(f"**{i+1}. {idea['name']}**")
        st.sidebar.caption(f"{idea['category']} | {idea['island']}")
        if st.sidebar.button(f"Remove #{i+1}", key=f"remove_{i}"):
            st.session_state.saved_ideas.pop(i)
            st.rerun()
else:
    st.sidebar.write("Ideas you like will appear here.")

if st.session_state.saved_ideas:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["name", "category", "island", "notes", "maps_link", "tripadvisor_link", "yelp_link"]
    )
    writer.writeheader()
    writer.writerows(st.session_state.saved_ideas)

    st.sidebar.download_button(
        "Download Saved Ideas",
        output.getvalue(),
        "hawaii_saved_ideas.csv",
        "text/csv"
    )

st.image(
    "SRDAHF.png",
    caption="Andrew & Stephanie 🌺",
    use_container_width=True
)

st.title("🌺 Andrew & Stephanie's Hawaii AI Planner")

st.markdown("""
Pick islands, generate real activity ideas with clickable research links,
save the ones you like, then turn your saved ideas into an itinerary.
""")

st.info(
    "Wedding dates are October 7, 8, and 9 in Honolulu, Oahu. "
    "The itinerary must keep Andrew and Stephanie in Honolulu for those dates."
)

st.subheader("Trip Setup")

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

st.divider()

st.subheader("Step 1: Generate Actionable Ideas")

idea_category = st.selectbox(
    "What kind of ideas?",
    ["Activities", "Restaurants", "Romantic Ideas", "Beaches", "Hikes", "Hidden Gems", "All of the Above"]
)

number_of_ideas = st.slider("How many ideas?", 5, 20, 8)

if st.button("Find Ideas with Links"):

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

    with st.spinner("Finding ideas..."):
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )

    raw_output = response.output_text
    st.session_state.latest_ideas_text = raw_output

if "latest_ideas_text" in st.session_state:
    st.markdown(st.session_state.latest_ideas_text)

    st.subheader("Save an Idea You Like")

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

    if st.button("Save This Idea"):
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

st.divider()

st.subheader("Step 2: Build Itinerary From Saved Ideas")

if st.button("Create Itinerary From Saved Ideas"):

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

        with st.spinner("Building itinerary..."):
            response = client.responses.create(
                model="gpt-5-nano",
                input=prompt
            )

        st.subheader("🌴 Your Saved-Ideas Itinerary")
        st.markdown(response.output_text)
