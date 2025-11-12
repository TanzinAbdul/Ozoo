import streamlit as st
from core.game_manager import ZooManager

# --- Initialize game ---
if "zoo_manager" not in st.session_state:
    st.session_state.zoo_manager = ZooManager()

zoo = st.session_state.zoo_manager

# --- Title ---
st.title("🦁 OzZoo Simulation Game")
st.caption("A zoo management simulation built with Python OOP")

# --- Zoo creation ---
if not zoo._zoo:
    st.subheader("Create a Zoo")
    name = st.text_input("Enter zoo name", "My Zoo")
    if st.button("Create Zoo"):
        msg = zoo.create_zoo(name)
        st.success(msg)
else:
    st.subheader(f"📅 Day {zoo._day_count}")
    st.json(zoo.get_zoo_status())

    # --- Actions ---
    st.subheader("🎯 Actions")
    if st.button("Advance Day"):
        result = zoo.advance_day()
        st.write("## 🦓 Daily Summary")
        for msg in result.get("messages", []):
            st.write(msg)
    if st.button("Feed Animals"):
        result = zoo.feed_animals()
        for msg in result.get("messages", []):
            st.write(msg)
    if st.button("Clean Enclosures"):
        result = zoo.clean_enclosures()
        for msg in result.get("messages", []):
            st.write(msg)
