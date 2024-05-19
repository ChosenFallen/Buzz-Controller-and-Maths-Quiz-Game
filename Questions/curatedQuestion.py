import json
import os

from Questions.baseQuestion import BaseQuestion, BaseQuestionSet, Tags

question_sets = {
    "template": "C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/template.json",
    "bodmas": "C:/Users/curti/OneDrive/Python/Buzz Controllers/Quiz Game/Questions/Curated Questions/bodmasQuestions.json",
}

    
class CuratedQuestion(BaseQuestion):
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


class CuratedQuestionSet(BaseQuestionSet):
    def __init__(self, JSON_File: str) -> None:
        self.load_question_data(JSON_File)        
        self.index = 0
        
    def load_question_data(self, JSON_File: str):
        with open(JSON_File) as f:
            data = json.load(f)
            self.questions = [CuratedQuestion(question_data) for question_data in data]
        
    


if __name__ == "__main__":
    print(os.getcwd())
    question_set = CuratedQuestionSet(question_sets["bodmas"])
    # question_data = CuratedQuestion.load_question_data(question_sets["bodmas"], 0)
    # testing = CuratedQuestion(question_data)
    print(question_set.get_current_question_data())