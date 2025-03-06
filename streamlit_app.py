import streamlit as st
import pandas as pd
import os

# File to persist the data
csv_file = "plays.csv"

# Load or initialize the DataFrame
if "df" not in st.session_state:
    if os.path.exists(csv_file):
        st.session_state.df = pd.read_csv(csv_file)
    else:
        # Create dummy data if CSV doesn't exist
        data = [
            {
                "Title_Marathi": "नाटक 1",
                "Title_English": "Play 1",
                "Author_Marathi": "लेखक अ",
                "Author_English": "Author A",
                "Length": 120,
                "Number of Acts": 3,
                "Genre": "Drama",
                "First Performance Year": 1990,
                "Submitted By": '',
            }
        ]
        st.session_state.df = pd.DataFrame(data)
        st.session_state.df.to_csv(csv_file, index=False)

# Convert columns to numeric
st.session_state.df["First Performance Year"] = pd.to_numeric(st.session_state.df["First Performance Year"], errors="coerce")
st.session_state.df["Number of Acts"] = pd.to_numeric(st.session_state.df["Number of Acts"], errors="coerce")

# Helper function to save DataFrame to CSV
def save_to_csv():
    st.session_state.df.to_csv(csv_file, index=False)
    st.success("Data saved to 'plays.csv'!")

# Sidebar menu
st.sidebar.title("Marathi Plays Database")
option = st.sidebar.radio("Choose an option", ["Display Plays", "Add a New Play", "Export Data"])

# Display Plays
if option == "Display Plays":
    st.title("Browse Marathi Plays")

    if st.session_state.df.empty:
        st.warning("No data available. Please add plays or upload a database.")
    else:
        # Display language toggle
        display_language = st.sidebar.radio("Select Display Language", ["Marathi", "English"])

        if display_language == "Marathi":
            # Select only Marathi-specific columns and rename them
            display_df = st.session_state.df[["Title_Marathi", "Author_Marathi", "Length", "Number of Acts", "Genre", "First Performance Year", "Submitted By"]].copy()
            display_df.columns = ["Title", "Author", "Length", "Number of Acts", "Genre", "First Performance Year", "Submitted By"]
        else:
            # Use only the English-specific columns and rename them
            display_df = st.session_state.df[["Title_English", "Author_English", "Length", "Number of Acts", "Genre", "First Performance Year", "Submitted By"]].copy()
            display_df.columns = ["Title", "Author", "Length", "Number of Acts", "Genre", "First Performance Year", "Submitted By"]

        # Filters
        st.sidebar.write("Filtering:")
        genre_filter = st.sidebar.text_input("By Genre (e.g., Drama, Comedy)")
        acts = st.sidebar.text_input("By number of acts")
        author_m = st.sidebar.text_input("By लेखक")
        year_min = st.sidebar.number_input("Filter by Min Year", min_value=1500, max_value=2024, value=1500)
        year_max = st.sidebar.number_input("Filter by Max Year", min_value=1500, max_value=2024, value=2024)

        # Apply filters to display_df
        if genre_filter:
            display_df = display_df[display_df["Genre"].str.contains(genre_filter, case=False, na=False)]
        if acts:
            display_df = display_df[display_df["Number of Acts"] == int(acts)]
        if author_m:
            display_df = display_df[display_df["Author"].str.contains(author_m, case=False, na=False)]
        display_df = display_df[(display_df["First Performance Year"] >= year_min) & (display_df["First Performance Year"] <= year_max)]

        # Display the filtered DataFrame
        st.write(display_df)

        # Play details
        st.write("### Play Details")
        if not display_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                selected_play = st.selectbox("Select a play", options=display_df["Title"])
            details = display_df[display_df["Title"] == selected_play].iloc[0].to_dict()
            
            updated_details = {}
            for key, value in details.items():
                updated_value = st.text_input(f"**{key}**", value)
                updated_details[key] = updated_value
            
            passphrase = st.text_input("Enter passphrase to save changes", type="password")
            
            if st.button("Save Changes"):
                if passphrase == "nakat":  # Replace with your actual passphrase
                    # Determine the underlying title and author columns based on display language
                    if display_language == "Marathi":
                        title_col = "Title_Marathi"
                        author_col = "Author_Marathi"
                    else:
                        title_col = "Title_English"
                        author_col = "Author_English"

                    # Update each field appropriately:
                    for key, value in updated_details.items():
                        if key == "Title":
                            st.session_state.df.loc[
                                st.session_state.df[title_col] == selected_play, title_col
                            ] = value
                        elif key == "Author":
                            st.session_state.df.loc[
                                st.session_state.df[author_col] == selected_play, author_col
                            ] = value
                        else:
                            # For other fields, update directly using the row identified by the title in the language-specific column.
                            st.session_state.df.loc[
                                st.session_state.df[title_col] == selected_play, key
                            ] = value
                    st.session_state.df.to_csv('plays.csv', index=False)
                    st.success("Changes saved successfully!")
                else:
                    st.error("Incorrect passphrase. Changes not saved.")

# Add a New Play
elif option == "Add a New Play":
    st.title("Add a New Marathi Play")

    # Form for adding a new play
    with st.form("Add Play Form"):
        # Compulsory Fields
        title_marathi = st.text_input("Title_Marathi", help="This field is compulsory.")
        title_english = st.text_input("Title_English", help="This field is compulsory.")
        author_marathi = st.text_input("Author_Marathi", help="This field is compulsory.")
        author_english = st.text_input("Author_English", help="This field is compulsory.")

        # Optional Fields
        length = st.number_input("Length (in minutes)", min_value=1, help="Optional.")
        num_acts = st.number_input("Number of Acts", min_value=1, help="Optional.")
        genre = st.text_input("Genre", help="Optional.")
        first_year = st.number_input("First Performance Year", min_value=1500, max_value=2024, help="Optional.")
        submitted_by = st.text_input("Submitted By", help="Optional.")

        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Prepare new entry
            new_entry = {
                "Title_Marathi": title_marathi,
                "Title_English": title_english,
                "Author_Marathi": author_marathi,
                "Author_English": author_english,
                "Length": length,
                "Number of Acts": num_acts,
                "Genre": genre,
                "First Performance Year": first_year,
                "Submitted By": '',
            }

            # Validate compulsory fields
            if not title_marathi or not title_english or not author_marathi or not author_english:
                st.error("Please fill out all compulsory fields: Title and Author (both Marathi and English).")
            else:
                # Append new entry to session state DataFrame
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
                save_to_csv()  # Save to CSV
                st.success("New play added successfully!")
                st.dataframe(st.session_state.df)

# Export Data
elif option == "Export Data":
    st.title("Export Database")

    # Button to save data
    if st.button("Save to CSV"):
        save_to_csv()
