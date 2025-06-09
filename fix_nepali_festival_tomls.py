import os
import glob
import shutil
import toml

NEPALI_FESTIVALS_ROOT = "jyotisha/panchaanga/temporal/festival/data/nepali"

def fix_festival_toml_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            original_content = f.read()
        parsed = toml.loads(original_content)
    except Exception as e:
        print(f"❌ Failed to parse TOML in {path}: {e}")
        return

    # Skip files that were wrongly structured as a list
    if isinstance(parsed, list):
        print(f"⚠️ Skipping {path} — TOML file is a list instead of a dict.")
        return

    # Check and fix the [timing] type field
    timing = parsed.get("timing", {})
    if timing.get("type") == "FestivalTiming":
        print(f"🔧 Fixing 'FestivalTiming' type in: {path}")
        parsed["timing"]["type"] = "HinduCalendarEventTiming"
    else:
        return  # No fix needed, skip file

    # Backup original
    backup_path = path + ".bak"
    try:
        shutil.copy2(path, backup_path)
    except Exception as e:
        print(f"❌ Failed to backup {path}: {e}")
        return

    # Write back fixed TOML
    try:
        with open(path, "w", encoding="utf-8") as f:
            toml.dump(parsed, f)
        print(f"✅ Cleaned: {path}")
    except Exception as e:
        print(f"❌ Failed to write cleaned content to {path}: {e}")


def walk_and_fix_all():
    toml_paths = glob.glob(f"{NEPALI_FESTIVALS_ROOT}/**/*.toml", recursive=True)
    if not toml_paths:
        print("⚠️ No TOML files found.")
        return

    print(f"🔍 Found {len(toml_paths)} TOML files. Starting cleanup...\n")
    for path in toml_paths:
        fix_festival_toml_file(path)
    print("\n✅ All festival files checked and cleaned.")


if __name__ == "__main__":
    walk_and_fix_all()
