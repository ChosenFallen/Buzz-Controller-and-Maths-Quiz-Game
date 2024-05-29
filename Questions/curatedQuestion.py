import json
from os.path import join

from constants import *
from questions.baseQuestion import BaseQuestion, BaseQuestionSet

question_sets = {
    "template": join("questions", "curated_questions", "template.json"),
    "bodmas": join("questions", "curated_questions", "bodmasQuestions.json"),
}


class CuratedQuestion(BaseQuestion):
    def __init__(self, question_data, sprite_groups) -> None:
        used_tags: list[Tags] = [
            Tags(tag) for tag in question_data["tags"] if tag in Tags
        ]
        super().__init__(
            question=question_data["question"],
            answer=question_data["answer"],
            wrong_answers=question_data["wrong_answers"],
            sprite_groups=sprite_groups,
            tags=used_tags,
        )

    @staticmethod
    def load_question_data(JSON_File: str, index: int):
        with open(JSON_File) as f:
            data = json.load(f)
            # print(data[index])
        return data[index]


class CuratedQuestionSet(BaseQuestionSet):
    def __init__(self, JSON_File: str, sprite_groups) -> None:
        self.load_question_data(JSON_File, sprite_groups)
        self.index = 0

    def load_question_data(self, JSON_File: str, sprite_groups) -> None:
        with open(JSON_File) as f:
            data = json.load(f)
            self.questions = [
                CuratedQuestion(question_data, sprite_groups=sprite_groups)
                for question_data in data
            ]


# if __name__ == "__main__":
#     print(os.getcwd())
#     question_set = CuratedQuestionSet(question_sets["bodmas"])
#     # question_data = CuratedQuestion.load_question_data(question_sets["bodmas"], 0)
#     # testing = CuratedQuestion(question_data)
#     print(question_set.get_current_question_data())
