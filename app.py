import os
import streamlit as st
from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.temporal.time import Date
from jyotisha.panchaanga.writer import md

# Set Swiss Ephemeris path if needed
os.environ["SWEPHEPATH"] = os.path.join(os.path.dirname(__file__), "ephe")

st.set_page_config(page_title="Panchanga Generator", layout="wide")
st.title("📅 Panchanga Generator")
st.markdown("Generate Panchanga for any city and date range using jyotisha.")

with st.form("panchanga_form"):
    st.subheader("Enter Location & Date Range")
    city_name = st.text_input("City Name", value="Kathmandu")
    latitude = st.text_input("Latitude (D:M:S)", value="27:42:00")
    longitude = st.text_input("Longitude (D:M:S)", value="85:19:00")
    timezone = st.text_input("Timezone", value="Asia/Kathmandu")
    start_date_input = st.date_input("Start Date")
    end_date_input = st.date_input("End Date")
    submit = st.form_submit_button("Generate Panchanga")

if submit:
    if not start_date_input or not end_date_input:
        st.error("Please select both start and end dates.")
    elif end_date_input < start_date_input:
        st.error("End Date should be after Start Date.")
    else:
        # Convert to jyotisha Date
        start_date = Date(year=start_date_input.year, month=start_date_input.month, day=start_date_input.day)
        end_date = Date(year=end_date_input.year, month=end_date_input.month, day=end_date_input.day)
        computation_system = ComputationSystem.MULTI_NEW_MOON_SIDEREAL_MONTH_ADHIKA_AMAANTA__CHITRA_180
        try:
            city = City(city_name, latitude, longitude, timezone)
            delta = (end_date_input - start_date_input).days
            if delta > 7:
                st.warning(f"You are generating Panchanga for {delta+1} days. This may take a while...")
            st.info(f"Generating Panchanga for: {city_name} ({latitude}, {longitude}, {timezone}) from {start_date} to {end_date}")
            panchaanga = annual.get_panchaanga_for_given_dates(
                city=city,
                start_date=start_date,
                end_date=end_date,
                computation_system=computation_system,
                allow_precomputed=False
            )
            md_content = md.make_md(panchaanga=panchaanga)
            st.markdown(md_content)
        except Exception as e:
            st.error(f"Error generating Panchanga: {e}")






# import datetime
# import os
# import tempfile
# import subprocess
#
# # ----------- Configuration -----------
# START_YEAR = datetime.date.today().year
# END_YEAR = START_YEAR
# FORMATS = ["md", "ics", "pdf"]  # Choose any combination of: md, ics, pdf
# FESTIVAL_RULE_FILE = None  # Optionally provide a path to .toml or .jsonl festival file
#
# # ----------- Execution -----------
# print("📅 Kathmandu Panchanga Generator")
# print(f"Generating Panchanga for {START_YEAR} to {END_YEAR} in formats: {FORMATS}\n")
#
# with tempfile.TemporaryDirectory() as tmpdir:
#     # Prepare the festival rule file if provided
#     festival_path = None
#     if FESTIVAL_RULE_FILE:
#         suffix = os.path.splitext(FESTIVAL_RULE_FILE)[1]
#         festival_path = os.path.join(tmpdir, f"custom_festivals{suffix}")
#         with open(FESTIVAL_RULE_FILE, "rb") as src, open(festival_path, "wb") as dst:
#             dst.write(src.read())
#
#     # Absolute path to the script
#     project_root = os.path.abspath(os.path.dirname(__file__))
#     script_path = os.path.join(project_root, "scripts", "generate_kathmandu_panchanga.py")
#
#     if not os.path.exists(script_path):
#         raise FileNotFoundError(f"Could not find the script at {script_path}")
#
#     cmd = ["python", script_path, "--start-year", str(START_YEAR), "--end-year", str(END_YEAR), "--output-modes", ",".join(FORMATS)]
#     if festival_path:
#         cmd += ["--festival-rules", festival_path]
#
#     result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
#
#     if result.returncode != 0:
#         print("❌ Failed to generate Panchanga:\n")
#         print(result.stderr)
#     else:
#         print("✅ Panchanga generated successfully!")
#         for fmt in FORMATS:
#             out_dir = os.path.join(project_root, fmt)
#             if os.path.exists(out_dir):
#                 print(f"\n📂 Output files in '{fmt}/':")
#                 for file in os.listdir(out_dir):
#                     print(f"- {file}")
#             else:
#                 print(f"⚠️ No output found for format '{fmt}'")
