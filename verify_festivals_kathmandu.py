import os
import json
from jyotisha.panchaanga.temporal import ComputationSystem, FestivalOptions
from jyotisha.panchaanga.temporal.festival.rules import RulesRepo, HinduCalendarEvent
from jyotisha.panchaanga.spatio_temporal import City, annual
from sanskrit_data.schema import common


# Register festival class for deserialization
common.json_class_index["HinduCalendarEvent"] = HinduCalendarEvent


def load_nepali_festival_options():
    from jyotisha.panchaanga.temporal.festival.rules import RulesRepo, HinduCalendarEvent
    from sanskrit_data.schema import common

    # Register class
    common.json_class_index["HinduCalendarEvent"] = HinduCalendarEvent

    """
    Loads Nepali festival definitions from a JSONL file and returns a FestivalOptions object.
    """
    jsonl_path = os.path.join(
        os.path.dirname(__file__),
        "jyotisha/panchaanga/temporal/festival/data/nepali/nepali.jsonl"
    )

    events = []

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                event = common.JsonObject.make_from_dict(data)
                events.append(event)
                print(f"✅ Loaded festival: {event.id}")
            except Exception as e:
                print(f"❌ Failed to parse line {line_num}: {e}\n🔹 Content: {line}")
                print(f"❌ Line {i}: Failed to load event — {e}")
                print(line)
    if not events:
        print("⚠️ No valid festival events loaded! Defaulting to empty repo.")

    print(f"✅ Loaded {len(events)} events")


    repo = RulesRepo(name="nepali", path=jsonl_path, base_url="file://local")
    repo.festival_rules = {e.id: e for e in events}


    return FestivalOptions(fest_repos=[repo])

from jyotisha.panchaanga.temporal import ComputationSystem

def generate_festival_list(city_name, latitude_str, longitude_str, timezone_str, year):
    city = City(city_name, latitude_str, longitude_str, timezone_str)

    ComputationSystem.NEPAL = ComputationSystem(
        lunar_month_assigner_type=ComputationSystem.DEFAULT.lunar_month_assigner_type,
        ayanaamsha_id=ComputationSystem.DEFAULT.ayanaamsha_id,
        short_id="नेपा॰",
        festival_options=load_nepali_festival_options()
    )

    print(f"📅 Loading Panchanga for {city_name}, {year}...\n")
    print("📦 Festival repos loaded:")
    for repo in ComputationSystem.NEPAL.festival_options.repos:
        print(" -", repo.name, f"({len(repo.festival_rules)} rules)")

    panchaanga = annual.get_panchaanga_for_civil_year(
        city=city,
        year=year,
        computation_system=ComputationSystem.NEPAL,
        allow_precomputed=False
    )

    # ✅ Defensive check
    if not hasattr(panchaanga, 'daily_panchaangas') or not panchaanga.daily_panchaangas:
        print("❌ ERROR: Panchaanga generation failed — 'daily_panchaangas' is missing or empty.")
        return

    # Continue with processing
    for dp in panchaanga.daily_panchaangas:
        if dp.festival_id_to_instance:
            print(f"📅 {dp.date.get_date_str()} — {[fest.id for fest in dp.festival_id_to_instance.values()]}")

    all_festivals = []
    for dp in panchaanga.daily_panchaangas:
        if dp.festival_day:
            for fest in dp.festival_day.festivals:
                all_festivals.append({
                    "date": dp.date.to_string(format="yyyy-MM-dd"),
                    "festival": fest.name
                })

    all_festivals.sort(key=lambda x: x["date"])

    print("\n🎉 Festivals Found:\n")
    for item in all_festivals:
        print(f"{item['date']} — {item['festival']}")

    print(f"\n✅ Total: {len(all_festivals)} festivals found.\n")


if __name__ == "__main__":
    generate_festival_list(
        city_name="Kathmandu",
        latitude_str="27:42:00",
        longitude_str="85:18:00",
        timezone_str="Asia/Kathmandu",
        year=2025
    )
