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
        # Removed language selection – always display both Marathi and English columns.
        display_df = st.session_state.df[[
            "Title_Marathi", "Author_Marathi",
            "Title_English", "Author_English",
            "Length", "Number of Acts", "Genre",
            "First Performance Year", "Submitted By", "Male Characters", "Female Characters",
            "Pages", "Property", "Year of Writing", "Availability", "YouTube", "Certified By"
        ]].copy()

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
        act_options_sidebar = [1, 1.5, 2, 3, 4, 0, -1]
        acts = st.sidebar.radio("By Number of Acts", options=act_options_sidebar, horizontal=True)
        author_m = st.sidebar.text_input("By लेखक")
        year_min = st.sidebar.number_input("Filter by Min Year", min_value=1500, max_value=2024, value=1500)
        year_max = st.sidebar.number_input("Filter by Max Year", min_value=1500, max_value=2024, value=2024)
        male_chars_range = st.sidebar.slider("Number of Male Characters", min_value=0, max_value=100, value=(0, 10))
        female_chars_range = st.sidebar.slider("Number of Female Characters", min_value=0, max_value=100, value=(0, 10))

        # Apply filters to display_df
        if filter_selected:
            # Retain rows if any of the selected genres appear in the Genre string.
            display_df = display_df[display_df["Genre"].apply(lambda s: any(filt in s for filt in filter_selected))]
        if acts > 0:
            display_df = display_df[display_df["Number of Acts"] == acts]
        elif acts == 0:
            display_df = display_df[display_df["Number of Acts"].isna()]
        # else:
        #     display_df = display_df[display_df["Number of Acts"] > 0]
        if author_m:
            display_df = display_df[display_df["Author"].str.contains(author_m, case=False, na=False)]
        display_df = display_df[(display_df["First Performance Year"] >= year_min) & 
                                (display_df["First Performance Year"] <= year_max)]
        display_df = display_df[(display_df["Male Characters"] >= male_chars_range[0]) & (display_df["Male Characters"] <= male_chars_range[1])]
        display_df = display_df[(display_df["Female Characters"] >= female_chars_range[0]) & (display_df["Female Characters"] <= female_chars_range[1])]

        st.write(f"Number of plays found: {len(display_df)}")
        # Reset selection when filters change.
        if len(display_df) > 0:
            st.session_state.selected_index = 0
            st.session_state.selected_play = display_df.iloc[0]["Title_English"]
        else:
            st.session_state.selected_index = None
            st.session_state.selected_play = ""

        # Insert a "Select" column showing row index.
        display_df = display_df.reset_index(drop=True)
        display_df.insert(0, "Select", display_df.index)

        from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
        st.write("#### Click the index (Select) button to choose a play:")
        gb = GridOptionsBuilder.from_dataframe(display_df)

        # Configure the "Select" column with a custom JS cell renderer that displays a styled button.
        custom_cell_renderer = """
        function(params) {
            return '<button style="background-color:#2980b9; color:white; border:none; padding:5px 10px; border-radius:3px;">' + params.value + '</button>';
        }
        """
        gb.configure_column("Select", headerName="Select", cellRenderer=custom_cell_renderer, width=80, suppressSizeToFit=True)

        gb.configure_selection(selection_mode="single", use_checkbox=False)
        grid_response = AgGrid(
            display_df, 
            gridOptions=gb.build(), 
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="streamlit",
            allow_unsafe_jscode=True  # Enable the custom JS renderer
        )
        selected_rows = grid_response.get("selected_rows", [])
        if not isinstance(selected_rows, list):
            selected_rows = [selected_rows]

        if selected_rows and selected_rows[0] is not None and "Select" in selected_rows[0]:
            sel_index = selected_rows[0]["Select"].values[0]
            selected_play = display_df.iloc[sel_index]["Title_English"]
            st.session_state.selected_play = selected_play
            st.write(f"In if: Selected Play: {selected_play}")
        else:
            if "selected_play" not in st.session_state:
                st.session_state.selected_play = display_df.iloc[0]["Title_English"]
            st.write(f"In else: Selected Play: {st.session_state.selected_play}")
        if st.session_state.selected_index is None:
            st.write("No play selected because no plays match the filter criteria.")
        else:
            st.write(f"Selected Play: {st.session_state.selected_play}")

        # Play details update section
        st.write("### Play Details")
        if not display_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                # Use the AgGrid-based selection if available.
                if "selected_play" in st.session_state:
                    selected_play = st.session_state.selected_play
                else:
                    selected_play = st.selectbox("Select a play", options=display_df["Title"])
            filtered = display_df[display_df["Title_English"].astype(str) == str(selected_play)]
            if not filtered.empty:
                details = filtered.iloc[0].to_dict()
            else:
                st.error("No play found matching the selected title. Please re-check your selection!")
                details = {}
            
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
                elif key == "Number of Acts":
                    act_options = [1, 1.5, 2, 3, 4]
                    try:
                        default_index = act_options.index(value)
                    except ValueError:
                        default_index = 0
                    updated_value = st.radio("**Number of Acts**", options=act_options, index=default_index, key=f"upd_{selected_play}_acts", horizontal=True)
                elif key == "Property":
                    property_options = ["Unknown", "No property", "Minimal", "Extensive", "Different acts"]
                    # Set default index based on current value or default to 0 if not in options
                    try:
                        default_index = property_options.index(value)
                    except ValueError:
                        default_index = 0
                    updated_value = st.radio("**Property**", options=property_options, index=default_index, key=f"upd_{selected_play}_Property", horizontal=True)
                elif key == "Availability":
                    availability_options = ["Print", "Abhivyakti", "CALAA", "NULL"]
                    st.write("**Availability**")
                    avail_selected = []
                    num_per_row = len(availability_options)
                    upd_cols = st.columns(num_per_row)
                    for i, opt in enumerate(availability_options):
                        # Pre-select if the current value string contains this option.
                        preselected = opt in value.split(";") if isinstance(value, str) else False
                        if upd_cols[i].checkbox(opt, value=preselected, key=f"upd_{selected_play}_{opt}"):
                            avail_selected.append(opt)
                    if "NULL" in avail_selected and len(avail_selected) > 1:
                        avail_selected.remove("NULL")
                    updated_value = "; ".join(avail_selected)
                else:
                    updated_value = st.text_input(f"**{key}**", value)
                updated_details[key] = updated_value
            
            passphrase = st.text_input("Enter passphrase to save changes", type="password")
            
            if st.button("Save Changes"):
                if passphrase == st.secrets["credentials"]["passphrase"]:
                    # Use Title_English as the unique identifier
                    original_title_english = details.get("Title_English")
                    mask = (st.session_state.df["Title_English"] == original_title_english)
                    idx_list = st.session_state.df[mask].index.tolist()
                    if idx_list:
                        row_idx = idx_list[0]
                        for key, value in updated_details.items():
                            st.session_state.df.at[row_idx, key] = value
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
        act_options = [1, 1.5, 2, 3, 4]
        num_acts = st.radio("Number of Acts", options=act_options, index=0, horizontal=True)
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
        property_options = ["Unknown", "No property", "Minimal", "Extensive", "Different acts"]
        property_val = st.radio("Property", options=property_options, index=0, horizontal=True)
        st.write("Selected:", property_val)
        year_writing = st.number_input("Year of Writing", min_value=1500, max_value=2024, help="Optional.")
        availability_options = ["Print", "Abhivyakti", "CALAA", "NULL"]
        st.write("Availability")
        avail_selected = []
        num_per_row = len(availability_options)
        cols = st.columns(num_per_row)
        for i, opt in enumerate(availability_options):
            if cols[i].checkbox(opt, key=f"avail_{opt}"):
                avail_selected.append(opt)
        # If any non-NULL option is selected, remove "NULL" even if checked.
        if "NULL" in avail_selected and len(avail_selected) > 1:
            avail_selected.remove("NULL")
        # Join selections into a string (or process as needed)
        availability = "; ".join(avail_selected)
        st.write("Selected: ", availability)
        youtube_link = st.text_input("YouTube (Link)", help="Optional.")
        certified_by = st.text_input("Certified By", help="Optional.")

        submitted = st.form_submit_button("Submit")
        passphrase = st.text_input("Enter passphrase to submit the new play", type="password", key="passphrase_add")
        if submitted:
            if passphrase != st.secrets["credentials"]["passphrase"]:
                st.error("Incorrect passphrase. New play not added.")
            else:
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
