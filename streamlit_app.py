import streamlit as st
from core.game_manager import ZooManager

st.set_page_config(page_title="OzZoo Simulation", page_icon="🦁")

# Initialize ZooManager once
if "zoo_manager" not in st.session_state:
    st.session_state.zoo_manager = ZooManager()
    st.session_state.day = 1

zoo = st.session_state.zoo_manager

st.title("🦁 OzZoo Simulation Game")
st.write("Welcome to the virtual zoo! Manage your animals, staff, and daily operations.")

# Display zoo summary
st.subheader(f"📅 Day {st.session_state.day}")
st.write(zoo.get_status_summary())  # replace with your actual method

st.subheader("🎯 Actions")

col1, col2, col3 = st.columns(3)

if col1.button("Feed Animals"):
    zoo.feed_animals()
    st.success("Animals have been fed!")

if col2.button("Clean Enclosures"):
    zoo.clean_enclosures()
    st.info("The zoo looks spotless!")

if col3.button("Next Day"):
    zoo.next_day()  # your daily simulation logic
    st.session_state.day += 1
    st.success(f"Day advanced to {st.session_state.day}!")

# You can add more controls:
# e.g. Add animal, hire staff, view reports, etc.

st.write("---")
st.caption("🐨 Built with ❤️ using Python OOP and Streamlit.")
