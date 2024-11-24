import streamlit as st
import pandas as pd
import os

# Load or initialize the DataFrame
csv_file = "marathi_plays.csv"

# Initialize the DataFrame
if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except Exception:
        df = pd.DataFrame(columns=[
            "Title (Marathi)", "Title (English)", "Author (Marathi)", "Author (English)", 
            "Length", "Number of Acts", "Genre", "First Performance Year"
        ])
else:
    df = pd.DataFrame(columns=[
        "Title (Marathi)", "Title (English)", "Author (Marathi)", "Author (English)", 
        "Length", "Number of Acts", "Genre", "First Performance Year"
    ])

# Sidebar menu
st.sidebar.title("Marathi Plays Database")
option = st.sidebar.selectbox("Choose an option", ["Display Plays", "Add a New Play", "Export/Import"])

if option == "Display Plays":
    st.title("Browse Marathi Plays")

    # Display language toggle
    display_language = st.sidebar.radio("Select Display Language", ["Marathi", "English"])

    if not df.empty:
        if display_language == "Marathi":
            display_df = df.rename(columns={
                "Title (Marathi)": "Title", "Author (Marathi)": "Author"
            })[["Title", "Author", "Length", "Number of Acts", "Genre", "First Performance Year"]]
        else:
            display_df = df.rename(columns={
                "Title (English)": "Title", "Author (English)": "Author"
            })[["Title", "Author", "Length", "Number of Acts", "Genre", "First Performance Year"]]

        # Filters
        genre_filter = st.sidebar.multiselect("Filter by Genre", options=df["Genre"].unique())

        # Ensure "First Performance Year" has valid min/max values
        if not df["First Performance Year"].isnull().all():
            min_year = int(df["First Performance Year"].dropna().min())
            max_year = int(df["First Performance Year"].dropna().max())
        else:
            min_year, max_year = 1500, 2024  # Default range if column is empty or invalid

        year_filter = st.sidebar.slider(
            "Filter by First Performance Year",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
        )

        # Apply filters
        filtered_df = df.copy()
        if genre_filter:
            filtered_df = filtered_df[filtered_df["Genre"].isin(genre_filter)]
        filtered_df = filtered_df[
            (filtered_df["First Performance Year"] >= year_filter[0])
            & (filtered_df["First Performance Year"] <= year_filter[1])
        ]

        # Search
        search_query = st.text_input("Search Plays (by Title or Author)")
        if search_query:
            filtered_df = filtered_df[
                filtered_df.apply(
                    lambda row: search_query.lower() in str(row["Title (Marathi)"]).lower()
                    or search_query.lower() in str(row["Title (English)"]).lower()
                    or search_query.lower() in str(row["Author (Marathi)"]).lower()
                    or search_query.lower() in str(row["Author (English)"]).lower(),
                    axis=1,
                )
            ]
        st.dataframe(filtered_df)

        # Details view
        st.write("### Play Details")
        if not filtered_df.empty:
            selected_play = st.selectbox("Select a play", options=filtered_df["Title (English)"])
            details = filtered_df[filtered_df["Title (English)"] == selected_play].iloc[0].to_dict()
            for key, value in details.items():
                st.write(f"**{key}**: {value}")
    else:
        st.warning("No data available. Please add plays or upload a database.")

elif option == "Add a New Play":
    st.title("Add a New Marathi Play")

    # Form for adding a new play
    with st.form("Add Play Form"):
        # Compulsory Fields
        title_marathi = st.text_input("Title (Marathi)", help="This field is compulsory.")
        title_english = st.text_input("Title (English)", help="This field is compulsory.")
        author_marathi = st.text_input("Author (Marathi)", help="This field is compulsory.")
        author_english = st.text_input("Author (English)", help="This field is compulsory.")

        # Optional Fields
        length = st.number_input("Length (in minutes)", min_value=1, help="Optional.")
        num_acts = st.number_input("Number of Acts", min_value=1, help="Optional.")
        genre = st.text_input("Genre", help="Optional.")
        first_year = st.number_input("First Performance Year", min_value=1500, max_value=2024, help="Optional.")

        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Validate compulsory fields
            if not title_marathi or not title_english or not author_marathi or not author_english:
                st.error("Please fill out all compulsory fields: Title and Author (both Marathi and English).")
            else:
                # Prepare new entry
                new_entry = {
                    "Title (Marathi)": title_marathi,
                    "Title (English)": title_english,
                    "Author (Marathi)": author_marathi,
                    "Author (English)": author_english,
                    "Length": length,
                    "Number of Acts": num_acts,
                    "Genre": genre,
                    "First Performance Year": first_year,
                }

                # Add to the database
                df = df.append(new_entry, ignore_index=True)
                st.success("New play added successfully!")
                st.dataframe(df)

elif option == "Export/Import":
    st.title("Export or Import Database")

    # Export Database
    if st.sidebar.button("Export Database"):
        df.to_csv(csv_file, index=False)
        st.success(f"Database exported as '{csv_file}'!")

    # Import Database
    uploaded_file = st.file_uploader("Upload Database", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Database loaded successfully!")
        st.dataframe(df)

