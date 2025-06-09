from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.temporal.time import Date
from jyotisha.panchaanga.writer import md

# --- Kathmandu settings ---
city = City('Kathmandu', "27:42:00", "85:19:00", "Asia/Kathmandu")
computation_system = ComputationSystem.MULTI_NEW_MOON_SIDEREAL_MONTH_ADHIKA_AMAANTA__CHITRA_180

target_date = Date(year=2025, month=6, day=24)

from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.temporal.time import Date
from jyotisha.panchaanga.writer import md

# Setup city and computation system to match the live site
city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
computation_system = ComputationSystem.MULTI_NEW_MOON_SIDEREAL_MONTH_ADHIKA_AMAANTA__CHITRA_180

# Use the specific date
target_date = Date(year=2025, month=6, day=20)

# Generate the panchaanga for that date (no custom festival repos, use default rules)
panchaanga = annual.get_panchaanga_for_given_dates(
    city=city,
    start_date=target_date,
    end_date=target_date,
    computation_system=computation_system,
    allow_precomputed=False
)

# Render to Markdown exactly as the live site does
md_content = md.make_md(panchaanga=panchaanga)

# Print to terminal (and/or write to file)
print(md_content)
# Optionally write to file:
# with open("Chennai_2020-01-20.md", "w", encoding="utf-8") as f:
#     f.write(md_content)






# from jyotisha.panchaanga.spatio_temporal import City, annual
# from jyotisha.panchaanga.temporal import ComputationSystem
# from jyotisha.panchaanga.temporal.time import Date
# from jyotisha.panchaanga.writer import md
#
# # Setup city and computation system to match the live site
# city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
# computation_system = ComputationSystem.MULTI_NEW_MOON_SIDEREAL_MONTH_ADHIKA_AMAANTA__CHITRA_180
#
# # Use the specific date
# target_date = Date(year=2020, month=1, day=24)
#
# # Generate the panchaanga for that date (no custom festival repos, use default rules)
# panchaanga = annual.get_panchaanga_for_given_dates(
#     city=city,
#     start_date=target_date,
#     end_date=target_date,
#     computation_system=computation_system,
#     allow_precomputed=False
# )
#
# # Render to Markdown exactly as the live site does
# md_content = md.make_md(panchaanga=panchaanga)
#
# # Print to terminal (and/or write to file)
# print(md_content)
# Optionally write to file:
# with open("Chennai_2020-01-20.md", "w", encoding="utf-8") as f:
#     f.write(md_content)



# 🐍 Panchanga Generator with Enhanced Debugging and Festival Matching
# import os
# import logging
# import swisseph as swe
# from doc_curation.md.file import MdFile
# from indic_transliteration import sanscript
# import traceback
# from datetime import datetime
#
# from jyotisha.panchaanga.writer import md, ics
# from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
# from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
# from jyotisha.panchaanga.spatio_temporal import City, annual
# from jyotisha.panchaanga.temporal.festival import rules
#
# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# def debug_print(message, level="info"):
#     """Helper function for consistent debug output"""
#     if level == "info":
#         logger.info(f"ℹ️ {message}")
#     elif level == "error":
#         logger.error(f"❌ {message}")
#     elif level == "warning":
#         logger.warning(f"⚠️ {message}")
#     else:
#         logger.debug(f"🔍 {message}")
#
#
# def validate_directory(path, description):
#     """Validate directory exists and show contents"""
#     debug_print(f"Validating {description} directory: {path}")
#     if not os.path.exists(path):
#         debug_print(f"Directory does not exist: {path}", "error")
#         return False
#
#     contents = os.listdir(path)
#     debug_print(f"Contents ({len(contents)} items): {contents[:5]}{'...' if len(contents) > 5 else ''}")
#     return True
#
#
# def main():
#     try:
#         debug_print("Starting Panchanga Generation for Kathmandu, 2025")
#
#         # Initialize City
#         debug_print("Initializing Kathmandu city parameters")
#         city = City("Kathmandu", "27:42:00", "85:18:00", "Asia/Kathmandu")
#
#         # Setup paths - CORRECTED based on your directory structure
#         BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#         debug_print(f"Base directory: {BASE_DIR}")
#
#         # Use only Adyatithi repo since Nepali repo path doesn't exist
#         ADYATITHI_REPO_PATH = os.path.join(BASE_DIR, "adyatithi", "nepali", "festivals")
#         debug_print(f"Using festival rules from: {ADYATITHI_REPO_PATH}")
#
#         if not validate_directory(ADYATITHI_REPO_PATH, "Adyatithi festival rules"):
#             raise FileNotFoundError("Festival rules directory not found")
#
#         # Load festival repository
#         debug_print("Loading festival repository...")
#         try:
#             festival_repo = rules.RulesRepo(name="nepali", path=ADYATITHI_REPO_PATH)
#             debug_print("Successfully loaded festival repository")
#
#             # Debugging: Inspect the festival_repo object
#             debug_print(f"Festival repo type: {type(festival_repo)}")
#             debug_print(f"Festival repo attributes: {dir(festival_repo)}")
#
#             # Load festival rules using get_festival_rules_map
#             festival_rules_map = rules.get_festival_rules_map(
#                 dir_path=festival_repo.get_path(),
#                 julian_handling=rules.RulesCollection.JULIAN_TO_GREGORIAN,
#                 repo=festival_repo
#             )
#
#             if not festival_rules_map:
#                 debug_print("No festival rules loaded!", "error")
#                 raise ValueError("Failed to load festival rules")
#
#             debug_print(f"Loaded {len(festival_rules_map)} festival rules")
#             if festival_rules_map:
#                 sample_rule_id = next(iter(festival_rules_map))
#                 debug_print(f"Sample rule ID: {sample_rule_id}")
#         except Exception as e:
#             debug_print(f"Error loading festival rules: {str(e)}", "error")
#             logger.debug(traceback.format_exc())
#             raise
#
#         # Initialize computation system with festival options
#         debug_print("Initializing computation system with festivals")
#         festival_options = FestivalOptions(fest_repos=[festival_repo])
#         computation_system = ComputationSystem(
#             lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
#             ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
#             short_id="नेपा॰",
#             festival_options=festival_options
#         )
#
#         # Generate panchaanga
#         debug_print("Generating annual panchaanga for 2025...")
#         panchaanga = annual.get_panchaanga_for_civil_year(
#             city=city, year=2025, computation_system=computation_system, allow_precomputed=False
#         )
#         debug_print("Successfully generated panchaanga")
#
#         # Process daily entries with proper error handling
#         debug_print("Processing daily entries with festival assignments...")
#         if not hasattr(panchaanga, 'daily_panchaangas') or not panchaanga.daily_panchaangas:
#             debug_print("No daily panchaangas found in the result!", "error")
#             return
#
#         # Prepare festival data structure
#         festival_data = []
#         empty_days = 0
#
#         for dp in panchaanga.daily_panchaangas:
#             date_str = dp.date.get_date_str() if hasattr(dp, 'date') else "Unknown date"
#
#             # Safely get festivals
#             festivals = getattr(dp, 'festival_id_list', []) or []
#             if not festivals:
#                 empty_days += 1
#
#             festival_data.append({
#                 "date": date_str,
#                 "festivals": festivals,
#                 "panchaanga_data": dp
#             })
#
#         debug_print(f"Processed {len(festival_data)} days, {empty_days} without festivals")
#
#         # Generate outputs with festival data
#         output_base = os.path.join(BASE_DIR, "output_kathmandu")
#         os.makedirs(output_base, exist_ok=True)
#         debug_print(f"Output will be saved to: {output_base}")
#
#         # 1. Markdown output with festivals
#         debug_print("Generating Markdown with festivals...")
#         try:
#             md_path = os.path.join(output_base, "panchanga_kathmandu_2025.md")
#             with open(md_path, 'w', encoding='utf-8') as f:
#                 f.write("# Nepali Panchanga 2025 - Kathmandu\n\n")
#                 f.write("## Daily Panchanga with Festivals\n\n")
#
#                 for day in festival_data:
#                     f.write(f"### {day['date']}\n")
#                     f.write(f"{day['panchaanga_data'].get_summary_text()}\n")
#
#                     if day['festivals']:
#                         f.write("**Festivals:**\n")
#                         for fest in day['festivals']:
#                             f.write(f"- {fest}\n")
#                     else:
#                         f.write("No festivals today\n")
#                     f.write("\n")
#
#             debug_print(f"Markdown saved to: {md_path}")
#         except Exception as e:
#             debug_print(f"Markdown generation failed: {str(e)}", "error")
#
#         # 2. ICS output
#         debug_print("Generating ICS file...")
#         try:
#             ics_path = os.path.join(output_base, "panchanga_kathmandu_2025.ics")
#             ics.write_to_file(ics.compute_calendar(panchaanga), ics_path)
#             debug_print(f"ICS saved to: {ics_path}")
#         except Exception as e:
#             debug_print(f"ICS generation failed: {str(e)}", "error")
#
#         # 3. LaTeX output
#         debug_print("Generating LaTeX...")
#         try:
#             tex_path = os.path.join(output_base, "panchanga_kathmandu_2025.tex")
#             with open(tex_path, 'w', encoding='utf-8') as tex_file:
#                 emit(panchaanga, output_stream=tex_file,
#                      languages=["sa", "ne"],
#                      scripts=[sanscript.DEVANAGARI] * 2)
#             debug_print(f"LaTeX saved to: {tex_path}")
#         except Exception as e:
#             debug_print(f"LaTeX generation failed: {str(e)}", "error")
#
#         debug_print("Panchanga generation completed successfully!", "info")
#
#     except Exception as e:
#         debug_print(f"Fatal error in main execution: {str(e)}", "error")
#         traceback.print_exc()
#
#
# if __name__ == "__main__":
#     main()




# import os
# import logging
# import swisseph as swe
# from doc_curation.md.file import MdFile
# from indic_transliteration import sanscript
#
# from jyotisha.panchaanga.writer import md, ics
# from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
# from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
# from jyotisha.panchaanga.spatio_temporal import City, annual
#
# # Configure Swiss Ephemeris path
# swe.set_ephe_path("/home/lokraj/PycharmProjects/panchanga/ephe")
#
# # Silence excessive internal logging
# logging.getLogger("jyotisha").setLevel(logging.ERROR)
#
# def main():
#     print("🚀 Starting Panchanga Generation for Kathmandu, 2025")
#
#     # Step 1: Set up city and time zone
#     print("🏙 Configuring Kathmandu...")
#     city = City("Kathmandu", "27:42:00", "85:18:00", "Asia/Kathmandu")
#
#     # Step 2: Setup computation system
#     print("⚙️ Initializing computation system...")
#
#
#     computation_system = ComputationSystem(
#         lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
#         ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
#         short_id="नेपा॰",
#         festival_options=FestivalOptions(fest_repos=[])
#         # festival_options=FestivalOptions(
#         #     fest_repos=[
#         #         rules.RulesRepo.CORE_REPO,
#         #         rules.RulesRepo(name="nepali", rules_file_path="jyotisha/panchaanga/temporal/festival/data/nepali")
#         #     ]
#         # )
#     )
#
#     # Step 3: Generate panchaanga
#     print("📅 Generating annual panchaanga...")
#     panchaanga = annual.get_panchaanga_for_civil_year(
#         city=city,
#         year=2026,
#         computation_system=computation_system,
#         allow_precomputed=False
#     )
#
#     print("🔍 Inspecting computed panchaanga...")
#     print("📌 Keys:", panchaanga.__dict__.keys())
#     print("📌 Entries in date_str_to_panchaanga:", len(panchaanga.date_str_to_panchaanga))
#
#     # Step 4: Filter only valid DailyPanchaanga entries
#     print("🧹 Filtering valid entries...")
#     valid_entries = []
#     for k, dp in panchaanga.date_str_to_panchaanga.items():
#         if dp is None:
#             print(f"⚠️ Skipping {k}: dp is None")
#             continue
#         if not hasattr(dp, 'date') or dp.date is None:
#             print(f"⚠️ Skipping {k}: dp.date is missing")
#             continue
#         valid_entries.append(dp)
#
#     if not valid_entries:
#         print("❌ ERROR: No valid daily entries found.")
#         return
#
#     # Fallback sort by date string key if .jd is missing
#     try:
#         daily_panchaangas = sorted(valid_entries, key=lambda dp: dp.date.jd)
#     except Exception as e:
#         print(f"⚠️ .jd not usable for sorting, falling back to date object: {e}")
#         daily_panchaangas = sorted(valid_entries, key=lambda dp: str(dp.date))
#
#     panchaanga.daily_panchaangas = daily_panchaangas
#
#     print(f"✅ Loaded {len(daily_panchaangas)} daily entries.")
#
#     # Step 6: Preview
#     print("🔎 Previewing first 3 days:")
#     for dp in daily_panchaangas[:3]:
#         summary = dp.get_summary_text() if callable(dp.get_summary_text) else dp.get_summary_text
#         print(f"📅 {dp.date.get_date_str() if hasattr(dp.date, 'get_date_str') else dp.date}: {summary}")
#
#         print(f"🔍 type(dp): {type(dp)}, type(dp.date): {type(dp.date)}, summary: {dp.get_summary_text}")
#
#     # Step 7: Write outputs
#     output_base = "./output_kathmandu"
#     os.makedirs(output_base, exist_ok=True)
#
#     # Markdown
#     print("📝 Writing Markdown...")
#     md_path = os.path.join(output_base, "panchanga_kathmandu_2025.md")
#     try:
#         md_file = MdFile(file_path=md_path)
#         md_file.dump_to_file(
#             metadata={"title": "Nepali Panchanga 2025 - Kathmandu"},
#             content=md.make_md(panchaanga=panchaanga),
#             dry_run=False
#         )
#         print(f"✅ Markdown saved at: {md_path}")
#     except Exception as e:
#         print(f"❌ Failed to write Markdown: {e}")
#
#     # ICS
#     print("📅 Writing ICS...")
#     ics_path = os.path.join(output_base, "panchanga_kathmandu_2025.ics")
#     try:
#         ics_calendar = ics.compute_calendar(panchaanga)
#         ics.write_to_file(ics_calendar, ics_path)
#         print(f"✅ ICS saved at: {ics_path}")
#     except Exception as e:
#         print(f"❌ Failed to write ICS: {e}")
#
#     # LaTeX
#     print("📜 Writing LaTeX...")
#     tex_path = os.path.join(output_base, "panchanga_kathmandu_2025.tex")
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
#     print("🎉 Panchanga generation completed successfully.")
#
# if __name__ == "__main__":
#     main()
