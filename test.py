from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.temporal.time import Date

city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
computation_system = ComputationSystem.MULTI_NEW_MOON_SIDEREAL_MONTH_ADHIKA_AMAANTA__CHITRA_180

# Expand the range!
start_date_str = "2025-05-08"
end_date_str   = "2025-05-10"
target_date    = "2025-05-09"

# Get the panchanga for a 3-day range
panchanga = annual.get_panchaanga_for_given_dates(
    city=city,
    start_date=start_date_str,
    end_date=end_date_str,
    computation_system=computation_system,
    allow_precomputed=False
)

# Print all available daily panchaangas (see if any are filled)
if hasattr(panchanga, "daily_panchaanga_for_date"):
    from jyotisha.panchaanga.temporal.time import Date as JDate
    for d in [JDate(2025,5,8), JDate(2025,5,9), JDate(2025,5,10)]:
        daily = panchanga.daily_panchaanga_for_date(d)
        print(f"\n=== Attempt for {d}: ===")
        if daily:
            for attr in ["date","samvatsara","tithi_data","nakshatra_data","karana_data","yoga_data","chandra_rashi_data","surya_rashi_data","sunrise","sunset"]:
                print(f"{attr}: {getattr(daily, attr, None)}")
        else:
            print("No daily panchaanga for this date.")
else:
    print("No daily_panchaanga_for_date method!")
