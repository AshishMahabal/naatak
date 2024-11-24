import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# Placeholder database
data = [
    {
        "Title (Marathi)": "नाटक 1",
        "Title (English)": "Play 1",
        "Author (Marathi)": "लेखक अ",
        "Author (English)": "Author A",
        "Length": 120,
        "Major Characters (Male)": 2,
        "Major Characters (Female)": 3,
        "Major Characters (Other/Animals)": 0,
        "Minor Characters (Male)": 1,
        "Minor Characters (Female)": 2,
        "Minor Characters (Other/Animals)": 0,
        "Number of Acts": 3,
        "Synopsis": "A drama about family values.",
        "Translated From": "Marathi",
        "Translated To": "English",
        "Genre": "Drama",
        "First Performance Year": 1990,
        "Notes": "Critically acclaimed.",
    },
]
df = pd.DataFrame(data)

# Authentication setup
credentials = {"usernames": {"admin": {"password": stauth.Hasher(["password123"]).generate()[0]}}}
authenticator = stauth.Authenticate(credentials, "marathi_play_app", "secret_key", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status:
    st.sidebar.success(f"Welcome, {name}!")

    # Sidebar menu
    st.sidebar.title("Marathi Plays Database")
    option = st.sidebar.selectbox("Choose an option", ["Display Plays", "Add a New Play", "Export/Import"])

    if option == "Display Plays":
        st.title("Browse Marathi Plays")

        # Display language toggle
        display_language = st.sidebar.radio("Select Display Language", ["Marathi", "English"])

        if display_language == "Marathi":
            display_df = df.rename(columns={"Title (Marathi)": "Title", "Author (Marathi)": "Author"})[
                ["Title", "Author", "Length", "Number of Acts"]
            ]
        else:
            display_df = df.rename(columns={"Title (English)": "Title", "Author (English)": "Author"})[
                ["Title", "Author", "Length", "Number of Acts"]
            ]

        # Filters
        genre_filter = st.sidebar.multiselect("Filter by Genre", options=df["Genre"].unique())
        year_filter = st.sidebar.slider(
            "Filter by First Performance Year",
            min_value=int(df["First Performance Year"].min()),
            max_value=int(df["First Performance Year"].max()),
            value=(int(df["First Performance Year"].min()), int(df["First Performance Year"].max())),
        )

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

    elif option == "Add a New Play":
        st.title("Add a New Marathi Play")

        # Form for adding a new play
        with st.form("Add Play Form"):
            title_marathi = st.text_input("Title (Marathi)")
            title_english = st.text_input("Title (English)")
            author_marathi = st.text_input("Author (Marathi)")
            author_english = st.text_input("Author (English)")
            length = st.number_input("Length (in minutes)", min_value=1)
            major_male = st.number_input("Major Characters (Male)", min_value=0)
            major_female = st.number_input("Major Characters (Female)", min_value=0)
            major_other = st.number_input("Major Characters (Other/Animals)", min_value=0)
            minor_male = st.number_input("Minor Characters (Male)", min_value=0)
            minor_female = st.number_input("Minor Characters (Female)", min_value=0)
            minor_other = st.number_input("Minor Characters (Other/Animals)", min_value=0)
            num_acts = st.number_input("Number of Acts", min_value=1)
            synopsis = st.text_area("Synopsis")
            translated_from = st.text_input("Translated From (leave blank if not applicable)")
            translated_to = st.text_input("Translated To (comma-separated if multiple)")
            genre = st.text_input("Genre")
            first_year = st.number_input("First Performance Year", min_value=1500, max_value=2024)
            notes = st.text_area("Notes (optional)")

            submitted = st.form_submit_button("Submit")
            if submitted:
                new_entry = {
                    "Title (Marathi)": title_marathi,
                    "Title (English)": title_english,
                    "Author (Marathi)": author_marathi,
                    "Author (English)": author_english,
                    "Length": length,
                    "Major Characters (Male)": major_male,
                    "Major Characters (Female)": major_female,
                    "Major Characters (Other/Animals)": major_other,
                    "Minor Characters (Male)": minor_male,
                    "Minor Characters (Female)": minor_female,
                    "Minor Characters (Other/Animals)": minor_other,
                    "Number of Acts": num_acts,
                    "Synopsis": synopsis,
                    "Translated From": translated_from,
                    "Translated To": translated_to,
                    "Genre": genre,
                    "First Performance Year": first_year,
                    "Notes": notes,
                }
                df = df.append(new_entry, ignore_index=True)
                st.success("New play added successfully!")
                st.dataframe(df)

    elif option == "Export/Import":
        st.title("Export or Import Database")

        # Export Database
        if st.sidebar.button("Export Database"):
            df.to_csv("marathi_plays.csv", index=False)
            st.success("Database exported as 'marathi_plays.csv'!")

        # Import Database
        uploaded_file = st.file_uploader("Upload Database", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("Database loaded successfully!")
            st.dataframe(df)

elif authentication_status == False:
    st.error("Username or password is incorrect.")
else:
    st.warning("Please enter your username and password.")

