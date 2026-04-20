import json
from datetime import datetime
from typing import Any, Dict, List, Optional

HistoryRecord = Dict[str, Any]


def make_record(expression: str, result: Any, timestamp: Optional[str] = None) -> HistoryRecord:
    return {
        "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expression": expression,
        "result": result,
    }


class HistoryManager:
    def __init__(self):
        self.records: List[HistoryRecord] = []

    def clear(self):
        self.records = []

    def add(self, expression: str, result: Any, timestamp: Optional[str] = None) -> HistoryRecord:
        record = make_record(expression, result, timestamp)
        self.records.append(record)
        return record

    def import_records(self, imported: List[HistoryRecord], replace: bool = False) -> List[HistoryRecord]:
        if replace:
            self.clear()
        self.records.extend(imported)
        return imported

    def load_json_file(self, path: str) -> List[HistoryRecord]:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return self.normalize_json(data)

    def save_json_file(self, path: str, records: List[HistoryRecord]) -> None:
        payload = {"history": records}
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

    def normalize_json(self, data: Any) -> List[HistoryRecord]:
        if isinstance(data, dict) and "history" in data:
            data = data["history"]

        if not isinstance(data, list):
            raise ValueError("JSON має містити список історії або об'єкт з полем 'history'.")

        records: List[HistoryRecord] = []
        for item in data:
            if isinstance(item, dict) and "expression" in item and "result" in item:
                record = {
                    "expression": item["expression"],
                    "result": item["result"],
                    "timestamp": item.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                }
                records.append(record)
            elif isinstance(item, str):
                records.append(make_record(item, "імпортовано"))

        if not records:
            raise ValueError("У файлі JSON не знайдено жодного дійсного запису історії.")

        return records
