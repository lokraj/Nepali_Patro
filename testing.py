import os
from datetime import datetime, date

from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
from jyotisha.panchaanga.temporal.festival import rules
from jyotisha.panchaanga.spatio_temporal import City, annual

import os
import logging

from jyotisha.panchaanga.temporal import festival, ComputationSystem

from jyotisha.panchaanga.spatio_temporal import annual

logging.basicConfig(level=logging.INFO)

def main():
    # Paths and config
    repo_path = "/home/lokraj/PycharmProjects/panchanga/adyatithi/nepali/festivals"
    year = 2025
    city = City.get_city_from_db("Kathmandu")   # ✅ This works, provided Kathmandu is in the .tsv file!


    # Try both ways of creating festival options depending on your Jyotisha version
    try:
        # If RulesRepo object is available, use it
        rules_repo = festival.rules.RulesRepo(
            name="nepali",
            path=repo_path,
            base_url="https://github.com/jyotisham/adyatithi/blob/master/nepali"
        )
        festival_options = festival.FestivalOptions(fest_repos=[rules_repo])
    except Exception as e:
        # Otherwise, fallback to plain dict
        print("[WARN] Could not use RulesRepo object, falling back to dict.")
        festival_options = festival.FestivalOptions(
            repos=[{
                "name": "nepali",
                "path": repo_path,
                "base_url": "https://github.com/jyotisham/adyatithi/blob/master/nepali"
            }]
        )

    # Print out debug info for the options
    print("festival_options.fest_repos:", getattr(festival_options, "fest_repos", None))
    print("festival_options.repos:", getattr(festival_options, "repos", None))

    # List out festival files found
    print("[DEBUG] Festival repo files:")
    if os.path.exists(repo_path):
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".toml"):
                    print(os.path.join(root, file))

    # Set up computation system
    computation_system = ComputationSystem(festival_options=festival_options)

    # Generate the panchaanga
    panchaanga = annual.get_panchaanga_for_civil_year(
        city=city,
        year=year,
        computation_system=computation_system,
        allow_precomputed=False
    )

    print("panchaanga type:", type(panchaanga))
    print("Has attribute daily_panchaangas:", hasattr(panchaanga, "daily_panchaangas"))
    print("daily_panchaangas:", getattr(panchaanga, "daily_panchaangas", None))
    print("Has attribute festival_id_to_instance:", hasattr(panchaanga, "festival_id_to_instance"))
    print("festival_id_to_instance:", getattr(panchaanga, "festival_id_to_instance", None))

    # Try to manually populate festival mapping if missing
    if getattr(panchaanga, "daily_panchaangas", None) is None or \
       getattr(panchaanga, "festival_id_to_instance", None) is None:
        print("[DEBUG] Attempting to manually populate festivals...")
        try:
            festival.populate_festival_mapping(panchaanga, festival_options)
            print("After manual population:")
            print("daily_panchaangas:", getattr(panchaanga, "daily_panchaangas", None))
            print("festival_id_to_instance:", getattr(panchaanga, "festival_id_to_instance", None))
        except Exception as e:
            print(f"[ERROR] populate_festival_mapping failed: {e}")

    # Show daily festivals
    daily_panchaangas = getattr(panchaanga, "daily_panchaangas", [])
    if daily_panchaangas is None:
        print("[ERROR] Still no daily_panchaangas after mapping.")
        return

    for dp in daily_panchaangas:
        print(f"{getattr(dp, 'date', None)}: festivals: {getattr(dp, 'festivals', None)}")

if __name__ == "__main__":
    main()


# import os
# import logging
# from datetime import datetime, date
# import swisseph as swe
# from doc_curation.md.file import MdFile
# from indic_transliteration import sanscript
#
# from jyotisha.panchaanga.writer import md, ics
# from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
# from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
# from jyotisha.panchaanga.temporal.festival import rules
# from jyotisha.panchaanga.spatio_temporal import City, annual
#
# # ===== CONFIGURABLE PARAMETERS =====
# SWE_EPHE_PATH = "/home/lokraj/PycharmProjects/panchanga/ephe"
# CITY_NAME = "Kathmandu"
# CITY_LAT = "27:42:00"
# CITY_LON = "85:18:00"
# CITY_TZ = "Asia/Kathmandu"
# FESTIVAL_REPO = "/home/lokraj/PycharmProjects/panchanga/adyatithi/nepali/festivals"
# START_DATE = "2025-01-06"
# END_DATE = "2025-01-12"
# OUTPUT_BASE = "./output_kathmandu"
#
# def parse_date(date_str):
#     return datetime.strptime(date_str, "%Y-%m-%d").date()
#
# def extract_date(dp):
#     d = getattr(dp, "date", None)
#     if d is None:
#         return None
#     if hasattr(d, "get_date_obj") and callable(d.get_date_obj):
#         try:
#             result = d.get_date_obj()
#             if isinstance(result, date):
#                 return result
#         except Exception:
#             return None
#     if isinstance(d, date):
#         return d
#     if isinstance(d, datetime):
#         return d.date()
#     if all(hasattr(d, attr) for attr in ("year", "month", "day")):
#         try:
#             return date(d.year, d.month, d.day)
#         except Exception:
#             return None
#     return None
#
# def main():
#     print(f"🚀 Starting Panchanga Festival Mapping for {CITY_NAME} ({START_DATE} to {END_DATE})")
#     swe.set_ephe_path(SWE_EPHE_PATH)
#     logging.getLogger("jyotisha").setLevel(logging.INFO)
#
#     print("🏙️ Initializing city object...")
#     city = City(CITY_NAME, CITY_LAT, CITY_LON, CITY_TZ)
#
#     print(f"🛕 Setting up computation system with festival repo: {FESTIVAL_REPO}")
#     computation_system = ComputationSystem(
#         lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
#         ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
#         short_id="नेपा॰",
#         festival_options=FestivalOptions(
#             fest_repos=[
#                 rules.RulesRepo("nepali", FESTIVAL_REPO)
#             ]
#         )
#     )
#
#     year = parse_date(START_DATE).year
#     print(f"📅 Generating annual Panchanga for year: {year}")
#     try:
#         panchaanga = annual.get_panchaanga_for_civil_year(
#             city=city,
#             year=year,
#             computation_system=computation_system,
#             allow_precomputed=False
#         )
#     except AttributeError as e:
#         print(f"💥 CRASH! Jyotisha panchaanga computation failed. Error:\n{e}")
#         return
#
#     print(f"🔍 Filtering daily Panchanga for dates {START_DATE} to {END_DATE}...")
#     start = parse_date(START_DATE)
#     end = parse_date(END_DATE)
#     daily_panchaangas = []
#     for dp in panchaanga.date_str_to_panchaanga.values():
#         if dp is None:
#             continue
#         day_obj = extract_date(dp)
#         if day_obj is None:
#             continue
#         if start <= day_obj <= end:
#             daily_panchaangas.append(dp)
#     if not daily_panchaangas:
#         print(f"❌ No Panchanga found for range {START_DATE} to {END_DATE}")
#         return
#
#     # Sort by date
#     daily_panchaangas = sorted(daily_panchaangas, key=lambda dp: extract_date(dp))
#     panchaanga.daily_panchaangas = daily_panchaangas
#
#     print("\n========= DETAILED DAYWISE FESTIVAL MAPPING =========")
#     for idx, dp in enumerate(daily_panchaangas, 1):
#         date_str = ""
#         if hasattr(dp.date, "get_date_str"):
#             date_str = dp.date.get_date_str()
#         else:
#             date_str = str(extract_date(dp))
#         print(f"\n--- [{idx}] --- {date_str} ---")
#         summary = ""
#         if hasattr(dp, "get_summary_text") and callable(dp.get_summary_text):
#             try:
#                 summary = dp.get_summary_text()
#             except Exception as e:
#                 summary = f"(Error getting summary: {e})"
#         else:
#             summary = str(dp)
#         print("Summary:", summary)
#
#         festivals_found = False
#         # Show all possible festival fields
#         if hasattr(dp, "festival_summary") and dp.festival_summary:
#             festivals_found = True
#             print("उत्सवाः (festival_summary):")
#             for fest in dp.festival_summary:
#                 print("  -", fest)
#         if hasattr(dp, "festivals") and dp.festivals:
#             festivals_found = True
#             print("उत्सवाः (festivals):")
#             for fest in dp.festivals:
#                 # Print as dict if possible, else just string
#                 if isinstance(fest, dict):
#                     print(f"  - {fest.get('name', '')} :: {fest.get('en', '')}")
#                 elif hasattr(fest, "name"):
#                     print(f"  - {fest.name}")
#                 else:
#                     print("  -", fest)
#         if not festivals_found:
#             print("No festivals mapped.")
#
#     print("\n========= END OF FESTIVAL MAPPING =========\n")
#
#     # (Optional) You can keep the output writers if desired
#     os.makedirs(OUTPUT_BASE, exist_ok=True)
#     range_str = f"{START_DATE}_to_{END_DATE}"
#
#     # Markdown output
#     md_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.md")
#     print(f"📝 Writing Markdown to {md_path} ...")
#     try:
#         md_file = MdFile(file_path=md_path)
#         md_file.dump_to_file(
#             metadata={"title": f"Nepali Panchanga {range_str.replace('_', ' ')} - {CITY_NAME}"},
#             content=md.make_md(panchaanga=panchaanga),
#             dry_run=False
#         )
#         print(f"✅ Markdown saved at: {md_path}")
#     except Exception as e:
#         print(f"❌ Failed to write Markdown: {e}")
#
#     # ICS output
#     ics_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.ics")
#     print(f"📅 Writing ICS to {ics_path} ...")
#     try:
#         ics_calendar = ics.compute_calendar(panchaanga)
#         ics.write_to_file(ics_calendar, ics_path)
#         print(f"✅ ICS saved at: {ics_path}")
#     except Exception as e:
#         print(f"❌ Failed to write ICS: {e}")
#
#     # LaTeX output
#     tex_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.tex")
#     print(f"📜 Writing LaTeX to {tex_path} ...")
#     try:
#         with open(tex_path, 'w', encoding='utf-8') as tex_file:
#             emit(
#                 panchaanga,
#                 output_stream=tex_file,
#                 languages=["sa", "ne"],
#                 scripts=[sanscript.DEVANAGARI, sanscript.DEVANAGARI]
#             )
#         print(f"✅ LaTeX saved at: {tex_path}")
#     except Exception as e:
#         print(f"❌ Failed to write LaTeX: {e}")
#
#     print("\n🎉 Panchanga generation and festival mapping completed.\n")
#
# if __name__ == "__main__":
#     main()


# import os
# import logging
# from datetime import datetime, date
# import swisseph as swe
# from doc_curation.md.file import MdFile
# from indic_transliteration import sanscript
#
# from jyotisha.panchaanga.writer import md, ics
# from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
# from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
# from jyotisha.panchaanga.temporal.festival import rules
# from jyotisha.panchaanga.spatio_temporal import City, annual
# import toml
#
# SWE_EPHE_PATH = "/home/lokraj/PycharmProjects/panchanga/ephe"
# CITY_NAME = "Kathmandu"
# CITY_LAT = "27:42:00"
# CITY_LON = "85:18:00"
# CITY_TZ = "Asia/Kathmandu"
# FESTIVAL_REPO = "/home/lokraj/PycharmProjects/panchanga/adyatithi/nepali/festivals"
# START_DATE = "2025-01-06"
# END_DATE = "2025-01-12"
# OUTPUT_BASE = "./output_kathmandu"
#
# def parse_date(date_str):
#     return datetime.strptime(date_str, "%Y-%m-%d").date()
#
# import re
# def extract_tithi_lunar_month(dp):
#     print(f"\n[extract_tithi_lunar_month] dp: {dp}")
#     # tithi_at_sunrise
#     tithi = None
#     sda = getattr(dp, "sunrise_day_angas", None)
#     if sda:
#         if hasattr(sda, "tithi_at_sunrise"):
#             tas = getattr(sda, "tithi_at_sunrise", None)
#             if hasattr(tas, "index"):
#                 tithi = tas.index
#             elif isinstance(tas, dict):
#                 tithi = tas.get("index", None)
#     # Try lunar_date.month for month
#     lunar_month = None
#     ld = getattr(dp, "lunar_date", None)
#     print(f"  tithi_at_sunrise: {getattr(sda, 'tithi_at_sunrise', None) if sda else None}")
#     print(f"  ld: {ld}")
#     if ld:
#         if hasattr(ld, "month"):
#             lm = getattr(ld, "month", None)
#             print(f"    ld.month: {lm} {type(lm)}")
#             # If it's an Anga object (not int/float/str), extract index attribute
#             if hasattr(lm, "index"):
#                 print(f"      Extracted from Anga.index: {lm.index}")
#                 lunar_month = lm.index
#             elif isinstance(lm, (int, float)):
#                 lunar_month = int(lm)
#             elif isinstance(lm, str):
#                 m = re.search(r"(\d+(\.\d+)?)$", lm)
#                 if m:
#                     lunar_month = int(float(m.group(1)))
#         elif isinstance(ld, dict):
#             lm = ld.get("month", None)
#             if isinstance(lm, (int, float)):
#                 lunar_month = int(lm)
#             elif isinstance(lm, str):
#                 m = re.search(r"(\d+(\.\d+)?)$", lm)
#                 if m:
#                     lunar_month = int(float(m.group(1)))
#     print(f"[extract_tithi_lunar_month] Extracted tithi={tithi}, lunar_month={lunar_month}")
#     return tithi, lunar_month
#
# def extract_date(dp):
#     d = getattr(dp, "date", None)
#     if d is None:
#         return None
#     if hasattr(d, "get_date_obj") and callable(d.get_date_obj):
#         try:
#             result = d.get_date_obj()
#             if isinstance(result, date):
#                 return result
#         except Exception:
#             return None
#     if isinstance(d, date):
#         return d
#     if isinstance(d, datetime):
#         return d.date()
#     if all(hasattr(d, attr) for attr in ("year", "month", "day")):
#         try:
#             return date(d.year, d.month, d.day)
#         except Exception:
#             return None
#     return None
#
# def write_dummy_festival_toml(dp, base_repo_dir):
#     tithi, lunar_month = extract_tithi_lunar_month(dp)
#     date_str = dp.date.get_date_str() if hasattr(dp.date, "get_date_str") else str(extract_date(dp))
#     if tithi is None or lunar_month is None:
#         print(f"Skipping TOML for {date_str} - tithi/lunar_month missing. [tithi={tithi}, lunar_month={lunar_month}]")
#         return
#     try:
#         tithi_number = int(tithi)
#     except Exception:
#         tithi_number = str(tithi)
#     try:
#         month_number = int(lunar_month)
#     except Exception:
#         month_number = str(lunar_month)
#     subdir = os.path.join(base_repo_dir, "lunar_month", "tithi", f"{month_number}", f"{tithi_number}")
#     os.makedirs(subdir, exist_ok=True)
#     file_path = os.path.join(subdir, f"dummy_{date_str}.toml")
#     toml_dict = {
#         "type": "HinduCalendarEvent",
#         "jsonClass": "HinduCalendarEvent",
#         "name": f"Dummy Festival for Month {month_number} Tithi {tithi_number}",
#         "description": f"Auto-generated dummy festival for month {month_number}, tithi {tithi_number}, date {date_str}",
#         "observed_on": "tithi",
#         "tags": ["Dummy", "Autogen", "Nepali"],
#         "rules": {
#             "tithi": tithi_number,
#             "month": month_number
#         },
#         "timing": {
#             "type": "HinduCalendarEventTiming",
#             "jsonClass": "HinduCalendarEventTiming",
#             "month_type": "lunar_month",
#             "month_number": month_number,
#             "anga_type": "tithi",
#             "anga_number": tithi_number
#         },
#         "details": {
#             "en": f"Dummy festival on tithi {tithi_number}, month {month_number}, date {date_str}",
#             "ne": f"डमी पर्व: महिना {month_number}, तिथि {tithi_number}, मिति {date_str}"
#         }
#     }
#     with open(file_path, "w", encoding="utf-8") as f:
#         toml.dump(toml_dict, f)
#     print(f"✅ Written dummy festival TOML: {file_path}")
#
# def print_day_intervals(panchaanga):
#     print("\n--- Checking available intervals for all days ---")
#     if hasattr(panchaanga, "daily_panchaangas") and panchaanga.daily_panchaangas:
#         for dp in panchaanga.daily_panchaangas:
#             date_str = dp.date.get_date_str() if hasattr(dp.date, "get_date_str") else str(extract_date(dp))
#             day_periods = getattr(dp, "day_length_based_periods", None)
#             print(f"{date_str} intervals: {list(day_periods.keys()) if day_periods else 'None'}")
#     print("--- End intervals check ---\n")
#
# def main():
#     print(f"🚀 Starting Panchanga Generation for {CITY_NAME} ({START_DATE} to {END_DATE})")
#     swe.set_ephe_path(SWE_EPHE_PATH)
#     logging.getLogger("jyotisha").setLevel(logging.INFO)
#     print("🏙️ Initializing city object...")
#     city = City(CITY_NAME, CITY_LAT, CITY_LON, CITY_TZ)
#     print(f"🛕 Setting up computation system with custom festival repo: {FESTIVAL_REPO}")
#     computation_system = ComputationSystem(
#         lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
#         ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
#         short_id="नेपा॰",
#         festival_options=FestivalOptions(
#             fest_repos=[
#                 rules.RulesRepo("nepali", FESTIVAL_REPO)
#             ]
#         )
#     )
#     year = parse_date(START_DATE).year
#     print(f"📅 Generating annual Panchanga for year: {year}")
#     try:
#         panchaanga = annual.get_panchaanga_for_civil_year(
#             city=city,
#             year=year,
#             computation_system=computation_system,
#             allow_precomputed=False
#         )
#     except AttributeError as e:
#         print(f"💥 CRASH! Jyotisha panchaanga computation failed. Error:\n{e}")
#         print("👉 This likely means your festival TOML expects a time interval not present on this day.")
#         print("👉 Try removing or adjusting 'kaala' in your festival TOML, or check available intervals below.")
#         try:
#             print_day_intervals(panchaanga)
#         except Exception:
#             pass
#         return
#
#     print_day_intervals(panchaanga)
#     print(f"🔍 Filtering daily Panchanga for dates {START_DATE} to {END_DATE}...")
#     start = parse_date(START_DATE)
#     end = parse_date(END_DATE)
#
#     # **THIS IS THE CRUCIAL PART: Only collect real panchaanga day objects!**
#     daily_panchaangas = []
#     for dp in panchaanga.date_str_to_panchaanga.values():
#         # Defensive: skip objects that don't have the attributes of daily panchaanga
#         if not hasattr(dp, "lunar_date") or not hasattr(dp, "sunrise_day_angas"):
#             print("WARNING: dp is not a DailyPanchaanga object! Skipping:", type(dp))
#             continue
#         day_obj = extract_date(dp)
#         if day_obj is None:
#             print(f"⚠️ Skipping entry with unrecognized date: {getattr(dp, 'date', None)}")
#             continue
#         if start <= day_obj <= end:
#             daily_panchaangas.append(dp)
#     if not daily_panchaangas:
#         print(f"❌ No Panchanga found for range {START_DATE} to {END_DATE}")
#         return
#     # Sort by date
#     daily_panchaangas = sorted(daily_panchaangas, key=lambda dp: extract_date(dp))
#     panchaanga.daily_panchaangas = daily_panchaangas
#
#     print("\n=== Generating Dummy Festival TOML files for matched days ===")
#     for dp in panchaanga.daily_panchaangas:
#         print(f"\n--- Debug for {extract_date(dp)} ---")
#         print(f"lunar_date (raw): {getattr(dp, 'lunar_date', None)}")
#         if hasattr(dp, 'lunar_date') and dp.lunar_date is not None:
#             print(f"  lunar_date.month: {getattr(dp.lunar_date, 'month', None)}")
#         sda = getattr(dp, "sunrise_day_angas", None)
#         print(f"sunrise_day_angas (raw): {getattr(dp, 'sunrise_day_angas', None)}")
#         if sda:
#             if hasattr(sda, "__dict__"):
#                 print(f"  tithi_at_sunrise: {getattr(sda, 'tithi_at_sunrise', None)}")
#             elif isinstance(sda, dict):
#                 print(f"  tithi_at_sunrise: {sda.get('tithi_at_sunrise', None)}")
#         write_dummy_festival_toml(dp, FESTIVAL_REPO)
#
#     print(f"✅ Loaded {len(daily_panchaangas)} entries for {START_DATE} to {END_DATE}.")
#
#     print("\n========= DETAILED DAYWISE DEBUGGING =========")
#     for idx, dp in enumerate(daily_panchaangas, 1):
#         date_str = ""
#         if hasattr(dp.date, "get_date_str"):
#             date_str = dp.date.get_date_str()
#         else:
#             date_str = str(extract_date(dp))
#         print(f"\n--- [{idx}] --- {date_str} ---")
#         summary = ""
#         if hasattr(dp, "get_summary_text") and callable(dp.get_summary_text):
#             try:
#                 summary = dp.get_summary_text()
#             except Exception as e:
#                 summary = f"(Error getting summary: {e})"
#         else:
#             summary = str(dp)
#         print("Summary:", summary)
#         festivals_found = False
#         if hasattr(dp, "festival_summary") and dp.festival_summary:
#             festivals_found = True
#             print("उत्सवाः (festival_summary):")
#             for fest in dp.festival_summary:
#                 print("  -", fest)
#         if hasattr(dp, "festivals") and dp.festivals:
#             festivals_found = True
#             print("उत्सवाः (festivals):")
#             for fest in dp.festivals:
#                 if isinstance(fest, dict):
#                     print(f"  - {fest.get('name','')} :: {fest.get('en','')}")
#                 else:
#                     print("  -", fest)
#         if not festivals_found:
#             print("No festivals mapped.")
#     print("\n========= END OF DEBUGGING =========\n")
#
#     # 5. Write outputs
#     os.makedirs(OUTPUT_BASE, exist_ok=True)
#     range_str = f"{START_DATE}_to_{END_DATE}"
#
#     # Markdown
#     md_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.md")
#     print(f"📝 Writing Markdown to {md_path} ...")
#     try:
#         md_file = MdFile(file_path=md_path)
#         md_file.dump_to_file(
#             metadata={"title": f"Nepali Panchanga {range_str.replace('_', ' ')} - {CITY_NAME}"},
#             content=md.make_md(panchaanga=panchaanga),
#             dry_run=False
#         )
#         print(f"✅ Markdown saved at: {md_path}")
#     except Exception as e:
#         print(f"❌ Failed to write Markdown: {e}")
#
#     # ICS
#     ics_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.ics")
#     print(f"📅 Writing ICS to {ics_path} ...")
#     try:
#         ics_calendar = ics.compute_calendar(panchaanga)
#         ics.write_to_file(ics_calendar, ics_path)
#         print(f"✅ ICS saved at: {ics_path}")
#     except Exception as e:
#         print(f"❌ Failed to write ICS: {e}")
#
#     # LaTeX
#     tex_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.tex")
#     print(f"📜 Writing LaTeX to {tex_path} ...")
#     try:
#         with open(tex_path, 'w', encoding='utf-8') as tex_file:
#             emit(
#                 panchaanga,
#                 output_stream=tex_file,
#                 languages=["sa", "ne"],
#                 scripts=[sanscript.DEVANAGARI, sanscript.DEVANAGARI]
#             )
#         print(f"✅ LaTeX saved at: {tex_path}")
#     except Exception as e:
#         print(f"❌ Failed to write LaTeX: {e}")
#
#     print("\n🎉 Panchanga generation for the selected week completed.\n")
#
# if __name__ == "__main__":
#     main()


# import os
# import logging
# from datetime import datetime, date
# import swisseph as swe
# from doc_curation.md.file import MdFile
# from indic_transliteration import sanscript
#
# from jyotisha.panchaanga.writer import md, ics
# from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
# from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
# from jyotisha.panchaanga.temporal.festival import rules
# from jyotisha.panchaanga.spatio_temporal import City, annual
#
# import toml
#
# # ===== CONFIGURABLE PARAMETERS =====
# SWE_EPHE_PATH = "/home/lokraj/PycharmProjects/panchanga/ephe"
# CITY_NAME = "Kathmandu"
# CITY_LAT = "27:42:00"
# CITY_LON = "85:18:00"
# CITY_TZ = "Asia/Kathmandu"
# FESTIVAL_REPO = "/home/lokraj/PycharmProjects/panchanga/adyatithi/nepali/festivals"
# START_DATE = "2025-01-06"
# END_DATE = "2025-01-12"
# OUTPUT_BASE = "./output_kathmandu"
#
# def parse_date(date_str):
#     return datetime.strptime(date_str, "%Y-%m-%d").date()
#
# def extract_date(dp):
#     d = getattr(dp, "date", None)
#     if d is None:
#         return None
#     if hasattr(d, "get_date_obj") and callable(d.get_date_obj):
#         try:
#             result = d.get_date_obj()
#             if isinstance(result, date):
#                 return result
#         except Exception:
#             return None
#     if isinstance(d, date):
#         return d
#     if isinstance(d, datetime):
#         return d.date()
#     if all(hasattr(d, attr) for attr in ("year", "month", "day")):
#         try:
#             return date(d.year, d.month, d.day)
#         except Exception:
#             return None
#     return None
#
# import re
# def extract_lunar_month(dp):
#     # Try direct attribute first
#     if hasattr(dp, "lunar_month") and dp.lunar_month is not None:
#         print("Found dp.lunar_month =", dp.lunar_month)
#         return dp.lunar_month
#     # Try dp.lunar_date.month if available
#     if hasattr(dp, "lunar_date") and hasattr(dp.lunar_date, "month"):
#         month_val = dp.lunar_date.month
#         print("DEBUG dp.lunar_date.month =", month_val)
#         # Extract trailing number using regex
#         m = re.search(r"(\d+(\.\d+)?)$", str(month_val))
#         if m:
#             try:
#                 print("Extracted lunar_month =", int(float(m.group(1))))
#                 return int(float(m.group(1)))
#             except Exception as e:
#                 print("Extraction failed:", e)
#                 return None
#         # Sometimes it's just an int/float
#         if isinstance(month_val, (int, float)):
#             return int(month_val)
#     print("No lunar month found!")
#     return None
#
#
#
# def extract_tithi_lunar_month(dp):
#     print("\n[extract_tithi_lunar_month] dp:", dp)
#     tithi = None
#     sda = getattr(dp, "sunrise_day_angas", None)
#     if sda:
#         if hasattr(sda, "tithi_at_sunrise"):
#             tas = getattr(sda, "tithi_at_sunrise", None)
#             print("  tithi_at_sunrise:", tas)
#             if hasattr(tas, "index"):
#                 tithi = tas.index
#             elif isinstance(tas, dict):
#                 tithi = tas.get("index", None)
#     lunar_month = None
#     ld = getattr(dp, "lunar_date", None)
#     print("  ld:", ld)
#     if ld:
#         if hasattr(ld, "month"):
#             lm = getattr(ld, "month", None)
#             print("    ld.month:", lm, type(lm))
#             # NEW: handle Anga object
#             if hasattr(lm, "index"):
#                 print("      Extracted from Anga.index:", lm.index)
#                 lunar_month = int(lm.index)
#             elif isinstance(lm, str):
#                 match = re.search(r'(\d+(\.\d+)?)$', lm.strip())
#                 print("      regex match:", match.group(1) if match else "No match")
#                 if match:
#                     lunar_month = int(float(match.group(1)))
#             elif isinstance(lm, (int, float)):
#                 lunar_month = int(lm)
#     print(f"[extract_tithi_lunar_month] Extracted tithi={tithi}, lunar_month={lunar_month}")
#     return tithi, lunar_month
#
#
#
#
# def print_day_intervals(panchaanga):
#     # Prints what intervals exist on each day, for debugging festival mapping
#     print("\n--- Checking available intervals for all days ---")
#     if hasattr(panchaanga, "daily_panchaangas") and panchaanga.daily_panchaangas:
#         for dp in panchaanga.daily_panchaangas:
#             date_str = dp.date.get_date_str() if hasattr(dp.date, "get_date_str") else str(extract_date(dp))
#             day_periods = getattr(dp, "day_length_based_periods", None)
#             print(f"{date_str} intervals: {list(day_periods.keys()) if day_periods else 'None'}")
#     print("--- End intervals check ---\n")
#
# def write_dummy_festival_toml(dp, base_repo_dir):
#     tithi, lunar_month = extract_tithi_lunar_month(dp)
#     date_str = dp.date.get_date_str() if hasattr(dp.date, "get_date_str") else str(extract_date(dp))
#
#     if tithi is None or lunar_month is None:
#         print(f"Skipping TOML for {date_str} - tithi/lunar_month missing. [tithi={tithi}, lunar_month={lunar_month}]")
#         return
#
#     # Use int() just to be sure, but if it's not, fallback to str()
#     try:
#         tithi_number = int(tithi)
#     except Exception:
#         tithi_number = str(tithi)
#     try:
#         month_number = int(lunar_month)
#     except Exception:
#         month_number = str(lunar_month)
#
#     subdir = os.path.join(base_repo_dir, "lunar_month", "tithi", f"{month_number}", f"{tithi_number}")
#     os.makedirs(subdir, exist_ok=True)
#     file_path = os.path.join(subdir, f"dummy_{date_str}.toml")
#
#     toml_dict = {
#         "type": "HinduCalendarEvent",
#         "jsonClass": "HinduCalendarEvent",
#         "name": f"Dummy Festival for Month {month_number} Tithi {tithi_number}",
#         "description": f"Auto-generated dummy festival for month {month_number}, tithi {tithi_number}, date {date_str}",
#         "observed_on": "tithi",
#         "tags": ["Dummy", "Autogen", "Nepali"],
#         "rules": {
#             "tithi": tithi_number,
#             "month": month_number
#         },
#         "timing": {
#             "type": "HinduCalendarEventTiming",
#             "jsonClass": "HinduCalendarEventTiming",
#             "month_type": "lunar_month",
#             "month_number": month_number,
#             "anga_type": "tithi",
#             "anga_number": tithi_number
#         },
#         "details": {
#             "en": f"Dummy festival on tithi {tithi_number}, month {month_number}, date {date_str}",
#             "ne": f"डमी पर्व: महिना {month_number}, तिथि {tithi_number}, मिति {date_str}"
#         }
#     }
#
#     with open(file_path, "w", encoding="utf-8") as f:
#         toml.dump(toml_dict, f)
#     print(f"✅ Written dummy festival TOML: {file_path}")
#
#
# def main():
#     print(f"🚀 Starting Panchanga Generation for {CITY_NAME} ({START_DATE} to {END_DATE})")
#     swe.set_ephe_path(SWE_EPHE_PATH)
#     logging.getLogger("jyotisha").setLevel(logging.INFO)
#
#     print("🏙️ Initializing city object...")
#     city = City(CITY_NAME, CITY_LAT, CITY_LON, CITY_TZ)
#
#     print(f"🛕 Setting up computation system with custom festival repo: {FESTIVAL_REPO}")
#     computation_system = ComputationSystem(
#         lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
#         ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
#         short_id="नेपा॰",
#         festival_options=FestivalOptions(
#             fest_repos=[
#                 rules.RulesRepo("nepali", FESTIVAL_REPO)
#             ]
#         )
#     )
#
#     year = parse_date(START_DATE).year
#     print(f"📅 Generating annual Panchanga for year: {year}")
#     try:
#         panchaanga = annual.get_panchaanga_for_civil_year(
#             city=city,
#             year=year,
#             computation_system=computation_system,
#             allow_precomputed=False
#         )
#     except AttributeError as e:
#         print(f"💥 CRASH! Jyotisha panchaanga computation failed. Error:\n{e}")
#         print("👉 This likely means your festival TOML expects a time interval not present on this day.")
#         print("👉 Try removing or adjusting 'kaala' in your festival TOML, or check available intervals below.")
#         try:
#             print_day_intervals(panchaanga)
#         except Exception:
#             pass
#         return
#
#     print_day_intervals(panchaanga)
#
#     print(f"🔍 Filtering daily Panchanga for dates {START_DATE} to {END_DATE}...")
#     start = parse_date(START_DATE)
#     end = parse_date(END_DATE)
#     daily_panchaangas = []
#     for dp in panchaanga.date_str_to_panchaanga.values():
#         if dp is None:
#             continue
#         day_obj = extract_date(dp)
#         if day_obj is None:
#             print(f"⚠️ Skipping entry with unrecognized date: {getattr(dp, 'date', None)}")
#             continue
#         if start <= day_obj <= end:
#             daily_panchaangas.append(dp)
#     if not daily_panchaangas:
#         print(f"❌ No Panchanga found for range {START_DATE} to {END_DATE}")
#         return
#
#     # Sort by date
#     daily_panchaangas = sorted(daily_panchaangas, key=lambda dp: extract_date(dp))
#     panchaanga.daily_panchaangas = daily_panchaangas
#     panchaanga.date_str_to_panchaanga = {
#         str(extract_date(dp)): dp for dp in daily_panchaangas
#     }
#
#     print("\n=== Generating Dummy Festival TOML files for matched days ===")
#     for dp in panchaanga.daily_panchaangas:
#         # Print extra debugging info
#         print(f"\n--- Debug for {extract_date(dp)} ---")
#         print(f"lunar_date (raw): {getattr(dp, 'lunar_date', None)}")
#         if hasattr(dp, 'lunar_date') and dp.lunar_date is not None:
#             print(f"  lunar_date.month: {getattr(dp.lunar_date, 'month', None)}")
#         sda = getattr(dp, "sunrise_day_angas", None)
#         print(f"sunrise_day_angas (raw): {getattr(dp, 'sunrise_day_angas', None)}")
#         if sda:
#             if hasattr(sda, "__dict__"):
#                 print(f"  tithi_at_sunrise: {getattr(sda, 'tithi_at_sunrise', None)}")
#             elif isinstance(sda, dict):
#                 print(f"  tithi_at_sunrise: {sda.get('tithi_at_sunrise', None)}")
#         write_dummy_festival_toml(dp, FESTIVAL_REPO)
#
#     print(f"✅ Loaded {len(daily_panchaangas)} entries for {START_DATE} to {END_DATE}.")
#
#     print("\n========= DETAILED DAYWISE DEBUGGING =========")
#     for idx, dp in enumerate(daily_panchaangas, 1):
#         date_str = ""
#         if hasattr(dp.date, "get_date_str"):
#             date_str = dp.date.get_date_str()
#         else:
#             date_str = str(extract_date(dp))
#         print(f"\n--- [{idx}] --- {date_str} ---")
#         summary = ""
#         if hasattr(dp, "get_summary_text") and callable(dp.get_summary_text):
#             try:
#                 summary = dp.get_summary_text()
#             except Exception as e:
#                 summary = f"(Error getting summary: {e})"
#         else:
#             summary = str(dp)
#         print("Summary:", summary)
#
#         festivals_found = False
#         if hasattr(dp, "festival_summary") and dp.festival_summary:
#             festivals_found = True
#             print("उत्सवाः (festival_summary):")
#             for fest in dp.festival_summary:
#                 print("  -", fest)
#         if hasattr(dp, "festivals") and dp.festivals:
#             festivals_found = True
#             print("उत्सवाः (festivals):")
#             for fest in dp.festivals:
#                 if isinstance(fest, dict):
#                     print(f"  - {fest.get('name','')} :: {fest.get('en','')}")
#                 else:
#                     print("  -", fest)
#         if not festivals_found:
#             print("No festivals mapped.")
#
#     print("\n========= END OF DEBUGGING =========\n")
#
#     # 5. Write outputs
#     os.makedirs(OUTPUT_BASE, exist_ok=True)
#     range_str = f"{START_DATE}_to_{END_DATE}"
#
#     print("type:", type(panchaanga))
#     print("daily_panchaangas:", getattr(panchaanga, "daily_panchaangas", None))
#     print("date_str_to_panchaanga:", getattr(panchaanga, "date_str_to_panchaanga", None))
#
#     print("  type:", type(panchaanga))
#     print("  has daily_panchaangas:", hasattr(panchaanga, "daily_panchaangas"))
#     print("  daily_panchaangas:", panchaanga.daily_panchaangas)
#     print("  date_str_to_panchaanga:", getattr(panchaanga, "date_str_to_panchaanga", None))
#
#     # Markdown
#     md_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.md")
#     print(f"📝 Writing Markdown to {md_path} ...")
#     try:
#         md_file = MdFile(file_path=md_path)
#         md_file.dump_to_file(
#             metadata={"title": f"Nepali Panchanga {range_str.replace('_', ' ')} - {CITY_NAME}"},
#             content=md.make_md(panchaanga=panchaanga),
#             dry_run=False
#         )
#         print(f"✅ Markdown saved at: {md_path}")
#     except Exception as e:
#         print(f"❌ Failed to write Markdown: {e}")
#
#     # ICS
#     ics_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.ics")
#     print(f"📅 Writing ICS to {ics_path} ...")
#     try:
#         ics_calendar = ics.compute_calendar(panchaanga)
#         ics.write_to_file(ics_calendar, ics_path)
#         print(f"✅ ICS saved at: {ics_path}")
#     except Exception as e:
#         print(f"❌ Failed to write ICS: {e}")
#
#     # LaTeX
#     tex_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.tex")
#     print(f"📜 Writing LaTeX to {tex_path} ...")
#     try:
#         with open(tex_path, 'w', encoding='utf-8') as tex_file:
#             emit(
#                 panchaanga,
#                 output_stream=tex_file,
#                 languages=["sa", "ne"],
#                 scripts=[sanscript.DEVANAGARI, sanscript.DEVANAGARI]
#             )
#         print(f"✅ LaTeX saved at: {tex_path}")
#     except Exception as e:
#         print(f"❌ Failed to write LaTeX: {e}")
#
#     print("\n🎉 Panchanga generation for the selected week completed.\n")
#
# if __name__ == "__main__":
#     main()


# import os
# import logging
# from datetime import datetime, date
# import swisseph as swe
# from doc_curation.md.file import MdFile
# from indic_transliteration import sanscript
#
# from jyotisha.panchaanga.writer import md, ics
# from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
# from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
# from jyotisha.panchaanga.temporal.festival import rules
# from jyotisha.panchaanga.spatio_temporal import City, annual
#
# SWE_EPHE_PATH = "/home/lokraj/PycharmProjects/panchanga/ephe"
# CITY_NAME = "Kathmandu"
# CITY_LAT = "27:42:00"
# CITY_LON = "85:18:00"
# CITY_TZ = "Asia/Kathmandu"
# FESTIVAL_REPO = "/home/lokraj/PycharmProjects/panchanga/adyatithi/nepali/festivals"
#
# START_DATE = "2025-01-06"
# END_DATE = "2025-01-12"
# OUTPUT_BASE = "./output_kathmandu"
#
# def parse_date(date_str):
#     return datetime.strptime(date_str, "%Y-%m-%d").date()
#
# def extract_date(dp):
#     d = getattr(dp, "date", None)
#     if d is None:
#         return None
#     if hasattr(d, "get_date_obj") and callable(d.get_date_obj):
#         try:
#             result = d.get_date_obj()
#             if isinstance(result, date):
#                 return result
#         except Exception:
#             return None
#     if isinstance(d, date):
#         return d
#     if isinstance(d, datetime):
#         return d.date()
#     if all(hasattr(d, attr) for attr in ("year", "month", "day")):
#         try:
#             return date(d.year, d.month, d.day)
#         except Exception:
#             return None
#     return None
#
# def print_day_intervals(panchaanga):
#     # Prints what intervals exist on each day, for debugging festival mapping
#     print("\n--- Checking available intervals for all days ---")
#     if hasattr(panchaanga, "daily_panchaangas") and panchaanga.daily_panchaangas:
#         for dp in panchaanga.daily_panchaangas:
#             date_str = dp.date.get_date_str() if hasattr(dp.date, "get_date_str") else str(extract_date(dp))
#             day_periods = getattr(dp, "day_length_based_periods", None)
#             print(f"{date_str} intervals: {list(day_periods.keys()) if day_periods else 'None'}")
#     print("--- End intervals check ---\n")
#
#
# import toml
#
# def write_dummy_festival_toml(dp, base_repo_dir):
#     tithi = getattr(dp, 'tithi', None)
#     lunar_month = getattr(dp, 'lunar_month', None)
#     date_str = dp.date.get_date_str() if hasattr(dp.date, "get_date_str") else str(extract_date(dp))
#
#     if tithi is None or lunar_month is None:
#         print(f"Skipping TOML for {date_str} - tithi/lunar_month missing.")
#         return
#
#     try:
#         tithi_number = int(tithi)
#         month_number = int(lunar_month)
#     except Exception:
#         print(f"⚠️ Could not parse tithi/month for {date_str} (tithi={tithi}, lunar_month={lunar_month})")
#         return
#
#     subdir = os.path.join(base_repo_dir, "lunar_month", "tithi", f"{month_number}", f"{tithi_number}")
#     os.makedirs(subdir, exist_ok=True)
#
#     file_path = os.path.join(subdir, f"dummy_{date_str}.toml")
#
#     toml_dict = {
#         "type": "HinduCalendarEvent",
#         "jsonClass": "HinduCalendarEvent",
#         "name": f"Dummy Festival for Month {month_number} Tithi {tithi_number}",
#         "description": f"Auto-generated dummy festival for month {month_number}, tithi {tithi_number}, date {date_str}",
#         "observed_on": "tithi",
#         "tags": ["Dummy", "Autogen", "Nepali"],
#         "rules": {
#             "tithi": tithi_number,
#             "month": month_number
#         },
#         "timing": {
#             "type": "HinduCalendarEventTiming",
#             "jsonClass": "HinduCalendarEventTiming",
#             "month_type": "lunar_month",
#             "month_number": month_number,
#             "anga_type": "tithi",
#             "anga_number": tithi_number
#         },
#         "details": {
#             "en": f"Dummy festival on tithi {tithi_number}, month {month_number}, date {date_str}",
#             "ne": f"डमी पर्व: महिना {month_number}, तिथि {tithi_number}, मिति {date_str}"
#         }
#     }
#
#     with open(file_path, "w", encoding="utf-8") as f:
#         toml.dump(toml_dict, f)
#     print(f"✅ Written dummy festival TOML: {file_path}")
#
#
# def main():
#     print(f"🚀 Starting Panchanga Generation for {CITY_NAME} ({START_DATE} to {END_DATE})")
#     swe.set_ephe_path(SWE_EPHE_PATH)
#     logging.getLogger("jyotisha").setLevel(logging.INFO)
#
#     print("🏙️ Initializing city object...")
#     city = City(CITY_NAME, CITY_LAT, CITY_LON, CITY_TZ)
#
#     print(f"🛕 Setting up computation system with custom festival repo: {FESTIVAL_REPO}")
#     computation_system = ComputationSystem(
#         lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
#         ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
#         short_id="नेपा॰",
#         festival_options=FestivalOptions(
#             fest_repos=[
#                 rules.RulesRepo("nepali", FESTIVAL_REPO)
#             ]
#         )
#     )
#
#     year = parse_date(START_DATE).year
#     print(f"📅 Generating annual Panchanga for year: {year}")
#     # Run once without festival repo to check if core jyotisha works:
#     try:
#         panchaanga = annual.get_panchaanga_for_civil_year(
#             city=city,
#             year=year,
#             computation_system=computation_system,
#             allow_precomputed=False
#         )
#     except AttributeError as e:
#         print(f"💥 CRASH! Jyotisha panchaanga computation failed. Error:\n{e}")
#         print("👉 This likely means your festival TOML expects a time interval not present on this day.")
#         print("👉 Try removing or adjusting 'kaala' in your festival TOML, or check available intervals below.")
#         # Try to print intervals if possible
#         try:
#             print_day_intervals(panchaanga)
#         except Exception:
#             pass
#         return
#
#     print_day_intervals(panchaanga)
#
#     # 4. Filter for selected week
#     print(f"🔍 Filtering daily Panchanga for dates {START_DATE} to {END_DATE}...")
#     start = parse_date(START_DATE)
#     end = parse_date(END_DATE)
#     daily_panchaangas = []
#     for dp in panchaanga.date_str_to_panchaanga.values():
#         if dp is None:
#             continue
#         day_obj = extract_date(dp)
#         if day_obj is None:
#             print(f"⚠️ Skipping entry with unrecognized date: {getattr(dp, 'date', None)}")
#             continue
#         if start <= day_obj <= end:
#             daily_panchaangas.append(dp)
#
#     if not daily_panchaangas:
#         print(f"❌ No Panchanga found for range {START_DATE} to {END_DATE}")
#         return
#
#     # Sort by date
#     daily_panchaangas = sorted(daily_panchaangas, key=lambda dp: extract_date(dp))
#     panchaanga.daily_panchaangas = daily_panchaangas
#
#     print("\n=== Generating Dummy Festival TOML files for matched days ===")
#     for dp in panchaanga.daily_panchaangas:
#         write_dummy_festival_toml(dp, FESTIVAL_REPO)
#
#     print(f"✅ Loaded {len(daily_panchaangas)} entries for {START_DATE} to {END_DATE}.")
#
#     print("\n--- Sample daily panchaanga attributes ---")
#     for dp in daily_panchaangas:
#         print("DATE:", extract_date(dp))
#         for attr in dir(dp):
#             if not attr.startswith("_"):
#                 try:
#                     val = getattr(dp, attr)
#                     if callable(val): continue
#                     print(f"{attr}: {val}")
#                 except Exception:
#                     continue
#         break  # Print only one day for brevity
#     print("--- End sample ---\n")
#
#     # ========== DEBUGGING LOOP ==========
#     print("\n========= DETAILED DAYWISE DEBUGGING =========")
#     for idx, dp in enumerate(daily_panchaangas, 1):
#         date_str = ""
#         if hasattr(dp.date, "get_date_str"):
#             date_str = dp.date.get_date_str()
#         else:
#             date_str = str(extract_date(dp))
#         print(f"\n--- [{idx}] --- {date_str} ---")
#         summary = ""
#         if hasattr(dp, "get_summary_text") and callable(dp.get_summary_text):
#             try:
#                 summary = dp.get_summary_text()
#             except Exception as e:
#                 summary = f"(Error getting summary: {e})"
#         else:
#             summary = str(dp)
#         print("Summary:", summary)
#
#         festivals_found = False
#         if hasattr(dp, "festival_summary") and dp.festival_summary:
#             festivals_found = True
#             print("उत्सवाः (festival_summary):")
#             for fest in dp.festival_summary:
#                 print("  -", fest)
#         if hasattr(dp, "festivals") and dp.festivals:
#             festivals_found = True
#             print("उत्सवाः (festivals):")
#             for fest in dp.festivals:
#                 if isinstance(fest, dict):
#                     print(f"  - {fest.get('name','')} :: {fest.get('en','')}")
#                 else:
#                     print("  -", fest)
#         if not festivals_found:
#             print("No festivals mapped.")
#
#     print("\n========= END OF DEBUGGING =========\n")
#
#     # 5. Write outputs
#     os.makedirs(OUTPUT_BASE, exist_ok=True)
#     range_str = f"{START_DATE}_to_{END_DATE}"
#
#     # Markdown
#     md_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.md")
#     print(f"📝 Writing Markdown to {md_path} ...")
#     try:
#         md_file = MdFile(file_path=md_path)
#         md_file.dump_to_file(
#             metadata={"title": f"Nepali Panchanga {range_str.replace('_', ' ')} - {CITY_NAME}"},
#             content=md.make_md(panchaanga=panchaanga),
#             dry_run=False
#         )
#         print(f"✅ Markdown saved at: {md_path}")
#     except Exception as e:
#         print(f"❌ Failed to write Markdown: {e}")
#
#     # ICS
#     ics_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.ics")
#     print(f"📅 Writing ICS to {ics_path} ...")
#     try:
#         ics_calendar = ics.compute_calendar(panchaanga)
#         ics.write_to_file(ics_calendar, ics_path)
#         print(f"✅ ICS saved at: {ics_path}")
#     except Exception as e:
#         print(f"❌ Failed to write ICS: {e}")
#
#     # LaTeX
#     tex_path = os.path.join(OUTPUT_BASE, f"panchanga_{CITY_NAME.lower()}_{range_str}.tex")
#     print(f"📜 Writing LaTeX to {tex_path} ...")
#     try:
#         with open(tex_path, 'w', encoding='utf-8') as tex_file:
#             emit(
#                 panchaanga,
#                 output_stream=tex_file,
#                 languages=["sa", "ne"],
#                 scripts=[sanscript.DEVANAGARI, sanscript.DEVANAGARI]
#             )
#         print(f"✅ LaTeX saved at: {tex_path}")
#     except Exception as e:
#         print(f"❌ Failed to write LaTeX: {e}")
#
#     print("\n🎉 Panchanga generation for the selected week completed.\n")
#
# if __name__ == "__main__":
#     main()
