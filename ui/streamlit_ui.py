import streamlit as st
from core.game_manager import ZooManager

def run_streamlit_app():
    """Run OzZoo game in a Streamlit UI."""

    st.set_page_config(page_title="OzZoo Simulation Game", page_icon="🦁")

    # Initialize zoo manager once
    if "zoo_manager" not in st.session_state:
        st.session_state.zoo_manager = ZooManager()
        st.session_state.day = 1
        st.session_state.zoo_created = False

    zoo = st.session_state.zoo_manager

    st.title("🦁 OzZoo Simulation Game")
    st.caption("A zoo management simulation built with Python OOP")

    # If zoo not yet created, show creation form
    if not st.session_state.zoo_created:
        st.subheader("🎮 Create Your Zoo")

        zoo_name = st.text_input("Enter your zoo name:")
        if st.button("Create Zoo"):
            if zoo_name:
                zoo.create_zoo(zoo_name, initial_funds=50000.0)
                st.session_state.zoo_created = True
                st.success(f"Zoo '{zoo_name}' created with $50,000 starting funds!")
            else:
                st.error("Please enter a valid zoo name.")
        return  # stop here until zoo is created

    # Show current zoo summary
    st.subheader(f"📅 Day {st.session_state.day}")
    st.write(zoo.get_zoo_status())

    # ---- ACTION BUTTONS ----
    st.divider()
    st.subheader("🎯 Actions")

    col1, col2, col3 = st.columns(3)

    if col1.button("🐾 Add Animal"):
        st.session_state.show_add_animal = True

    if col2.button("🍽️ Feed Animals"):
        result = zoo.feed_animals()
        st.success("Animals fed successfully!")

    if col3.button("🧹 Clean Enclosures"):
        cleaned = zoo.clean_enclosures()
        st.info(f"Cleaned {cleaned} enclosures!")

    if st.button("🌅 Advance to Next Day"):
        result = zoo.advance_day()
        st.session_state.day += 1
        st.success(f"Advanced to Day {st.session_state.day}")

    # ---- ADD ANIMAL POPUP ----
    if st.session_state.get("show_add_animal", False):
        st.subheader("🐾 Add a New Animal")

        available_animals = zoo.get_available_animals()
        animal_type = st.selectbox("Choose species:", available_animals)
        name = st.text_input("Animal name:")
        age = st.number_input("Age (years)", min_value=0, max_value=50, value=1)

        # Get enclosure list
        status = zoo.get_zoo_status()
        enclosure_names = [e["name"] for e in status["enclosures"]]
        selected_enclosure = st.selectbox("Choose enclosure:", enclosure_names)

        if st.button("Add Animal"):
            try:
                success = zoo.add_animal_to_zoo(animal_type, name, age, selected_enclosure)
                if success:
                    st.success(f"{name} the {animal_type} added to {selected_enclosure}!")
                    st.session_state.show_add_animal = False
                else:
                    st.error("Failed to add animal.")
            except Exception as e:
                st.error(str(e))

    st.divider()
    st.caption("🐨 Built with ❤️ using Streamlit + OOP Python")
