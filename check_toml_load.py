from sanskrit_data.schema import common
from jyotisha.panchaanga.temporal.festival.rules import HinduCalendarEvent

# ✅ Register the class so it can be deserialized
common.json_class_index["HinduCalendarEvent"] = HinduCalendarEvent

event = common.JsonObject.read_from_file("jyotisha/panchaanga/temporal/festival/data/nepali""/lunar_month/tithi/1/8/sample_festival.toml")
print("✅ Loaded event:", event.id, "| Class:", event.__class__)
