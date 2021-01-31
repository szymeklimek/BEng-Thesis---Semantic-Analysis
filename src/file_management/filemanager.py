import json

class FileManager:
    @staticmethod
    def load_text_file(path):
        with open(path, encoding="utf-16") as file:
            data = file.read().replace("\n", ". ")
        return data

    @staticmethod
    def save_to_file(doc, path):
        with open(path, "w+") as file:
            json.dump(doc, file)