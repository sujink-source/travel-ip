import streamlit as st

# Class for managing the itinerary
class Itinerary:
    def __init__(self):
        self.itinerary = {}

    def add_destination(self, destination, start_date, end_date, accommodation):
        if destination in self.itinerary:
            return False, f"Destination '{destination}' already exists."
        else:
            self.itinerary[destination] = {
                "start_date": start_date,
                "end_date": end_date,
                "accommodation": accommodation,
                "activities": []
            }
            return True, f"Added {destination} to the itinerary."

    def add_activity(self, destination, activity):
        if destination in self.itinerary:
            self.itinerary[destination]["activities"].append(activity)
            return True, f"Added activity '{activity}' to {destination}."
        else:
            return False, f"Destination '{destination}' does not exist in the itinerary."

    def remove_activity(self, destination, activity):
        if destination in self.itinerary:
            try:
                self.itinerary[destination]["activities"].remove(activity)
                return True, f"Removed activity '{activity}' from {destination}."
            except ValueError:
                return False, f"Activity '{activity}' not found in {destination}."
        else:
            return False, f"Destination '{destination}' does not exist in the itinerary."

    def view_itinerary(self):
        return self.itinerary

# Initialize itinerary in session state if not already present
if 'planner' not in st.session_state:
    st.session_state.planner = Itinerary()

# Streamlit app starts here
st.title("Travel Itinerary Planner")

# Sidebar for adding destinations
st.sidebar.header("Add a Destination")
destination = st.sidebar.text_input("Destination")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
accommodation = st.sidebar.text_input("Accommodation")

if st.sidebar.button("Add Destination"):
    success, message = st.session_state.planner.add_destination(destination, start_date, end_date, accommodation)
    if success:
        st.sidebar.success(message)
    else:
        st.sidebar.error(message)

# Add activities to a destination
st.sidebar.header("Add Activities")
if st.session_state.planner.view_itinerary():
    activity_dest = st.sidebar.selectbox("Select Destination", list(st.session_state.planner.view_itinerary().keys()))
    activity = st.sidebar.text_input("Activity")

    if st.sidebar.button("Add Activity"):
        success, message = st.session_state.planner.add_activity(activity_dest, activity)
        if success:
            st.sidebar.success(message)
        else:
            st.sidebar.error(message)
else:
    st.sidebar.warning("No destinations added yet.")

# Remove activity from a destination
st.sidebar.header("Remove Activities")
if st.session_state.planner.view_itinerary():
    remove_activity_dest = st.sidebar.selectbox("Select Destination to Remove Activity From", list(st.session_state.planner.view_itinerary().keys()), key='remove_activity_dest')
    remove_activity = st.sidebar.text_input("Activity to Remove", key='remove_activity')

    if st.sidebar.button("Remove Activity"):
        success, message = st.session_state.planner.remove_activity(remove_activity_dest, remove_activity)
        if success:
            st.sidebar.success(message)
        else:
            st.sidebar.error(message)
else:
    st.sidebar.warning("No destinations added yet.")

# Main section to display the itinerary
st.header("Current Itinerary")

itinerary = st.session_state.planner.view_itinerary()

if itinerary:
    for dest, details in itinerary.items():
        st.subheader(dest)
        st.write(f"**Start Date**: {details['start_date']}")
        st.write(f"**End Date**: {details['end_date']}")
        st.write(f"**Accommodation**: {details['accommodation']}")
        activities = details['activities'] if details['activities'] else "No activities planned"
        st.write(f"**Activities**: {', '.join(details['activities']) if activities else activities}")
else:
    st.write("No destinations added yet.")


