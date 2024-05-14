import json
import os
from random import shuffle

from baseQuestion import BaseQuestion

question_sets = {
    "template": "C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/template.json",
    "bodmas": "C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/bodmasQuestions.json",
}


class ReadCuratedQuestion(BaseQuestion):
    def __init__(self, JSON_File: str, index: int) -> None:
        # Load JSON file
        with open(JSON_File) as f:
            data = json.load(f)
            # print(data)
            question_data = data[index]
            # print(values[0]=question_data)
            question = question_data.question
            answer = question_data.answer
            wrong_answers = question_data.wrong_answers

            super().__init__(question, answer, wrong_answers)


if __name__ == "__main__":
    print(os.getcwd())
    # testing = ReadCuratedQuestion("C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/template.json", 0)
    testing = ReadCuratedQuestion(question_sets["bodmas"], 0)
