import streamlit as st
import pandas as pd
import os

# File to persist the data
csv_file = "plays.csv"

# Load or initialize the DataFrame
if "df" not in st.session_state:
    if os.path.exists(csv_file):
        st.session_state.df = pd.read_csv(
            csv_file,
            dtype={
                "Genre": str,
                "Submitted By": str,
                "Property": str,
                "Availability": str,
                "YouTube": str,
                "Certified By": str
            }
        )
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
                "Submitted By": "",
                "Male Characters": 0,
                "Female Characters": 0,
                "Pages": 0,
                "Property": "",
                "Year of Writing": 0,
                "Availability": "",
                "YouTube": "",
                "Certified By": ""
            }
        ]
        st.session_state.df = pd.DataFrame(data)
        st.session_state.df.to_csv(csv_file, index=False)


# # List of new columns with their default values
# new_columns = {
#     "Male Characters": 0,
#     "Female Characters": 0,
#     "Pages": 0,
#     "Property": "",
#     "Year of Writing": 0,
#     "Availability": "",
#     "YouTube": "",
#     "Certified By": ""
# }

# # Check if each new column exists; if not, add it with a default value
# for col, default_val in new_columns.items():
#     if col not in st.session_state.df.columns:
#         st.session_state.df[col] = default_val

# Convert numeric columns appropriately
st.session_state.df["First Performance Year"] = pd.to_numeric(st.session_state.df["First Performance Year"], errors="coerce")
st.session_state.df["Number of Acts"] = pd.to_numeric(st.session_state.df["Number of Acts"], errors="coerce")
st.session_state.df["Length"] = pd.to_numeric(st.session_state.df["Length"], errors="coerce")
st.session_state.df["Male Characters"] = pd.to_numeric(st.session_state.df["Male Characters"], errors="coerce")
st.session_state.df["Female Characters"] = pd.to_numeric(st.session_state.df["Female Characters"], errors="coerce")
st.session_state.df["Pages"] = pd.to_numeric(st.session_state.df["Pages"], errors="coerce")
st.session_state.df["Year of Writing"] = pd.to_numeric(st.session_state.df["Year of Writing"], errors="coerce")
st.session_state.df["Genre"] = st.session_state.df["Genre"].fillna("").astype(str)

# # Optionally, save the updated DataFrame back to the CSV
# st.session_state.df.to_csv(csv_file, index=False)
# st.success("CSV updated with new columns.")

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
            display_df = st.session_state.df[[
                "Title_Marathi", "Author_Marathi", "Length", "Number of Acts", "Genre",
                "First Performance Year", "Submitted By", "Male Characters", "Female Characters",
                "Pages", "Property", "Year of Writing", "Availability", "YouTube", "Certified By"
            ]].copy()
            display_df.columns = [
                "Title", "Author", "Length (in minutes)", "Number of Acts", "Genre",
                "First Performance Year", "Submitted By", "Male Characters", "Female Characters",
                "Pages", "Property", "Year of Writing", "Availability", "YouTube", "Certified By"
            ]
        else:
            display_df = st.session_state.df[[
                "Title_English", "Author_English", "Length", "Number of Acts", "Genre",
                "First Performance Year", "Submitted By", "Male Characters", "Female Characters",
                "Pages", "Property", "Year of Writing", "Availability", "YouTube", "Certified By"
            ]].copy()
            display_df.columns = [
                "Title", "Author", "Length (in minutes)", "Number of Acts", "Genre",
                "First Performance Year", "Submitted By", "Male Characters", "Female Characters",
                "Pages", "Property", "Year of Writing", "Availability", "YouTube", "Certified By"
            ]

        # Filters
        st.sidebar.write("Filtering:")
        st.sidebar.write("Filter by Genre:")
        filter_genre_options = ["Comedy", "Drama", "Farce", "Historical", "Musical", "Romance", "Satire", "Sci-Fi", "Tragedy", "Other"]
        filter_selected = []
        num_per_row = 2
        for i in range(0, len(filter_genre_options), num_per_row):
            cols = st.sidebar.columns(num_per_row)
            for j in range(num_per_row):
                idx = i + j
                if idx < len(filter_genre_options):
                    opt = filter_genre_options[idx]
                    if cols[j].checkbox(opt, key=f"filter_{opt}"):
                        filter_selected.append(opt)
        acts = st.sidebar.text_input("By Number of Acts")
        author_m = st.sidebar.text_input("By लेखक")
        year_min = st.sidebar.number_input("Filter by Min Year", min_value=1500, max_value=2024, value=1500)
        year_max = st.sidebar.number_input("Filter by Max Year", min_value=1500, max_value=2024, value=2024)
        male_chars_range = st.sidebar.slider("Number of Male Characters", min_value=0, max_value=100, value=(0, 10))
        female_chars_range = st.sidebar.slider("Number of Female Characters", min_value=0, max_value=100, value=(0, 10))

        # Apply filters to display_df
        if filter_selected:
            # Retain rows if any of the selected genres appear in the Genre string.
            display_df = display_df[display_df["Genre"].apply(lambda s: any(filt in s for filt in filter_selected))]
        if acts:
            display_df = display_df[display_df["Number of Acts"] == int(acts)]
        if author_m:
            display_df = display_df[display_df["Author"].str.contains(author_m, case=False, na=False)]
        display_df = display_df[(display_df["First Performance Year"] >= year_min) & 
                                (display_df["First Performance Year"] <= year_max)]
        display_df = display_df[(display_df["Male Characters"] >= male_chars_range[0]) & (display_df["Male Characters"] <= male_chars_range[1])]
        display_df = display_df[(display_df["Female Characters"] >= female_chars_range[0]) & (display_df["Female Characters"] <= female_chars_range[1])]

        st.write(f"Number of plays found: {len(display_df)}")
        # Display the filtered DataFrame
        st.write(display_df)

        # Play details update section
        st.write("### Play Details")
        if not display_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                selected_play = st.selectbox("Select a play", options=display_df["Title"])
            details = display_df[display_df["Title"] == selected_play].iloc[0].to_dict()
            
            updated_details = {}
            for key, value in details.items():
                if key == "Genre":
                    genre_options = ["Comedy", "Drama", "Farce", "Historical", "Musical", "Romance", "Satire", "Sci-Fi", "Tragedy", "Other"]
                    # Ensure the value is a string (convert NaN or None to an empty string)
                    value_str = value if isinstance(value, str) else ""
                    # Split the current genre string by semicolon to get pre-selected genres
                    preselected = [g.strip() for g in value_str.split(";")] if value_str else []
                    st.write("**Genre**")
                    upd_selected = []
                    num_per_row = 5
                    for i in range(0, len(genre_options), num_per_row):
                        upd_cols = st.columns(num_per_row)
                        for j in range(num_per_row):
                            idx = i + j
                            if idx < len(genre_options):
                                g = genre_options[idx]
                                if upd_cols[j].checkbox(g, value=(g in preselected), key=f"upd_{selected_play}_{g}"):
                                    upd_selected.append(g)
                    updated_value = "; ".join(upd_selected)
                else:
                    updated_value = st.text_input(f"**{key}**", value)
                updated_details[key] = updated_value
            
            passphrase = st.text_input("Enter passphrase to save changes", type="password")
            
            if st.button("Save Changes"):
                if passphrase == "nakat":  # Replace with your actual passphrase
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
                            st.session_state.df.loc[
                                st.session_state.df[title_col] == selected_play, key
                            ] = value
                    st.session_state.df.to_csv(csv_file, index=False)
                    st.success("Changes saved successfully!")
                else:
                    st.error("Incorrect passphrase. Changes not saved.")

# Add a New Play
elif option == "Add a New Play":
    st.title("Add a New Marathi Play")

    with st.form("Add Play Form"):
        # Compulsory Fields
        title_marathi = st.text_input("Title_Marathi", help="This field is compulsory.")
        title_english = st.text_input("Title_English", help="This field is compulsory.")
        author_marathi = st.text_input("Author_Marathi", help="This field is compulsory.")
        author_english = st.text_input("Author_English", help="This field is compulsory.")

        # Optional Fields
        length = st.number_input("Length (in minutes)", min_value=1, help="Optional.")
        num_acts = st.number_input("Number of Acts", min_value=1, help="Optional.")
        st.write("Select Genre(s) (optional):")
        genre_options = ["Comedy", "Drama", "Farce", "Historical", "Musical", "Romance", "Satire", "Sci-Fi", "Tragedy", "Other"]
        add_selected = []
        num_per_row = 5
        for i in range(0, len(genre_options), num_per_row):
            cols = st.columns(num_per_row)
            for j in range(num_per_row):
                idx = i + j
                if idx < len(genre_options):
                    opt = genre_options[idx]
                    if cols[j].checkbox(opt, key=f"add_genre_{opt}"):
                        add_selected.append(opt)
        # Save as semicolon-separated list; if nothing is selected, genre remains an empty string.
        genre = "; ".join(add_selected)
        first_year = st.number_input("First Performance Year", min_value=1500, max_value=2024, help="Optional.")
        submitted_by = st.text_input("Submitted By", help="Optional.")
        male_chars = st.number_input("Number of Male Characters", min_value=0, help="Optional.")
        female_chars = st.number_input("Number of Female Characters", min_value=0, help="Optional.")
        pages = st.number_input("Number of Pages", min_value=0, help="Optional.")
        property_val = st.text_input("Property", help="Optional.")
        year_writing = st.number_input("Year of Writing", min_value=1500, max_value=2024, help="Optional.")
        availability = st.text_input("Availability", help="Optional.")
        youtube_link = st.text_input("YouTube (Link)", help="Optional.")
        certified_by = st.text_input("Certified By", help="Optional.")

        submitted = st.form_submit_button("Submit")
        if submitted:
            new_entry = {
                "Title_Marathi": title_marathi,
                "Title_English": title_english,
                "Author_Marathi": author_marathi,
                "Author_English": author_english,
                "Length": length,
                "Number of Acts": num_acts,
                "Genre": genre,
                "First Performance Year": first_year,
                "Submitted By": submitted_by,
                "Male Characters": male_chars,
                "Female Characters": female_chars,
                "Pages": pages,
                "Property": property_val,
                "Year of Writing": year_writing,
                "Availability": availability,
                "YouTube": youtube_link,
                "Certified By": certified_by
            }

            if not title_marathi or not title_english or not author_marathi or not author_english:
                st.error("Please fill out all compulsory fields: Title and Author (both Marathi and English).")
            else:
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
                save_to_csv()
                st.success("New play added successfully!")
                st.dataframe(st.session_state.df)

# Export Data
elif option == "Export Data":
    st.title("Export Database")
    if st.button("Save to CSV"):
        save_to_csv()
