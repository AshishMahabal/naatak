# Clean the "First Performance Year" column to ensure all values are integers
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

