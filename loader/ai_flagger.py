import json
from dataclasses import asdict
from pathlib import Path
import logging


def init_ai_tracking(obj):
    """Initializes a list of fields filled using AI (e.g. GPT)."""
    setattr(obj, "_ai_fields", [])


def assign_if_valid(obj, attr_path: str, value, expected_type=None):
    """
    Assigns a value to a nested attribute and records that it came from AI.

    :param obj: Main object (e.g., a PacientTemplate instance)
    :param attr_path: Dot-separated path to the attribute, like 'M_B1.M_B_1.M_B_1_2_1'
    :param value: Value to assign
    :param expected_type: Optional type check
    """
    try:
        if expected_type and not isinstance(value, expected_type):
            return

        parts = attr_path.split(".")
        target = obj
        for part in parts[:-1]:
            target = getattr(target, part)
        setattr(target, parts[-1], value)

        if not hasattr(obj, "_ai_fields"):
            setattr(obj, "_ai_fields", [])

        obj._ai_fields.append(parts[-1])
    except Exception as e:
        logging.warning(f"AI assignment error at {attr_path}: {e}")


def extract_ai_filled_fields(obj, output_path="output/ai_only.json"):
    """
    Extracts only the fields filled by AI and saves them as a flat JSON.

    :param obj: Object with _ai_fields (e.g., PacientTemplate)
    :param output_path: Output file path
    """
    all_data = asdict(obj)
    ai_fields = getattr(obj, "_ai_fields", [])

    ai_only = {}

    def extract_by_key(d, key):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == key:
                    return v
                elif isinstance(v, dict):
                    result = extract_by_key(v, key)
                    if result is not None:
                        return result
        return None

    for field in ai_fields:
        value = extract_by_key(all_data, field)
        if value is not None:
            ai_only[field] = value

    Path("output").mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ai_only, f, ensure_ascii=False, indent=2)
