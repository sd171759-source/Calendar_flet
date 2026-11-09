import json
import os

from base import BaseEntity
from settings import Config


class BirthdayRecord(BaseEntity):
    def __init__(self, name, comment, date_str):
        self._name = name
        self._comment = comment
        self.date_str = date_str

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value): # чтобы имя не было пустым
        if not value.strip():
            raise ValueError()
        self._name = value.strip()

    @property
    def comment(self) :
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value.strip()

    def __str__(self) :
        return f"{self._name} [{self.date_str}]"

    def __eq__(self, other):
        if not isinstance(other, BirthdayRecord):
            return False
        return self._name.lower() == other._name.lower()

    def __lt__(self, other):
        if not isinstance(other, BirthdayRecord):
            return NotImplemented
        return self._name.lower() < other._name.lower()


class BirthdayMap:
    def __init__(self):
        self.pairs = []

    def put(self, key, record: BirthdayRecord):
        for i, (k, old_record) in enumerate(self.pairs):
            if k == key: # сравнивает старую запись с новой
                self.pairs[i] = (key, record)
                return
        self.pairs.append((key, record))

    def get(self, key) :
        for k, record in self.pairs:
            if k == key: return record
        return None

    def remove(self, key):
        self.pairs = [pair for pair in self.pairs if pair[0] != key]

    def get_all_records(self): #
        return [record for k, record in self.pairs]

    def to_raw_dict(self) :
        return {k: {"name": r.name, "comment": r.comment} for k, r in self.pairs}

    def from_raw_dict(self, data):
        self.pairs = []
        for k, v in data.items():
            self.pairs.append((k, BirthdayRecord(v["name"], v["comment"], k)))


class BirthdayStorage:
    def __init__(self):
        self.birthday_map = BirthdayMap()
        self.load_birthdays()

    def load_birthdays(self):
        if os.path.exists(Config.JSON_FILE):
            try:
                with open(Config.JSON_FILE, "r", encoding="utf-8") as f:
                    self.birthday_map.from_raw_dict(json.load(f))
            except Exception:
                pass

    def save_birthdays(self):
        with open(Config.JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.birthday_map.to_raw_dict(), f, ensure_ascii=False, indent=4)

