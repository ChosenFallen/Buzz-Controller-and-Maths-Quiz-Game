import json
import os

from tags import Tags
from baseQuestion import BaseQuestion

question_sets = {
    "template": "C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/template.json",
    "bodmas": "C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/bodmasQuestions.json",
}


class ReadCuratedQuestion(BaseQuestion):
    def __init__(self, question_data) -> None:
        used_tags: list[Tags] = [
            Tags(tag) for tag in question_data['tags'] if tag in Tags
        ]
        super().__init__(question=question_data['question'], answer=question_data['answer'], wrong_answers=question_data['wrong_answers'], tags=used_tags)

    @staticmethod
    def load_question_data(JSON_File: str, index: int):
        with open(JSON_File) as f:
            data = json.load(f)
            # print(data[index])
        return data[index]


if __name__ == "__main__":
    print(os.getcwd())
    question_data = ReadCuratedQuestion.load_question_data(question_sets["bodmas"], 0)
    testing = ReadCuratedQuestion(question_data)
    print(testing)