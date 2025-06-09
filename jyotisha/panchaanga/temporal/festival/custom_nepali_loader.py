import os
import toml
from jyotisha.panchaanga.temporal.festival.rules import RulesRepo, HinduCalendarEvent



def load_nepali_festival_options():
    repo_path = os.path.join(os.path.dirname(__file__), "data/nepali")

    events = []
    for filename in os.listdir(repo_path):
        if filename.endswith(".toml"):
            file_path = os.path.join(repo_path, filename)
            rule_dict = toml.load(file_path)
            event = HinduCalendarEvent.make_from_dict(rule_dict)
            events.append(event)

    repo = RulesRepo(name="nepali", path=repo_path)
    repo.festival_rules = {e.id: e for e in events}

    return FestivalOptions(fest_repos=[repo])
