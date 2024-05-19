import os
from enum import Enum, auto
from random import shuffle

from Questions.utilities import ALL_COLOURS, ANSWER_COLOURS, latex2image


class Tags(Enum):
    EQUATION = "equation"


class BaseQuestion:
    def __init__(self, question: str, answer: str, wrong_answers: list[str], tags: list[Tags] | None = None, id: str | None = None, latex_form: str | None = None) -> None:
        self.question: str = question
        self.answer: str = answer
        self.wrong_answers: list[str] = wrong_answers
        assert len(self.wrong_answers) == 3
        self.answer_colour: str = ""
        self.answer_dict: dict[str, str] = {}
        self.create_answer_dict()
        self.tags: list[Tags] = tags or []
        self.id: str = id or self.create_id(question)
        self.latex_form: str | None = latex_form
        

    def create_id(self, question: str) -> str:
        max_length = 20        

        count = sum(ord(letter) for letter in question) % 10000
        string = question.lower()
        
        for char in [" ", "?", "!", ",", "'", '"', "\\", "%", "[", "]", "{", "}", "|"]:
            string = string.replace(char, "")
        invalid_chars = {
            "*": "X",
            "/": "D",
            "-": "M",
            "+": "A",
            "^": "P",
            "&": "N",
            "<": "LT",
            ">": "GT",
            ".": "_",
            "=": "EQ",
        }
        for key, val in invalid_chars.items():
            string = string.replace(key, val)
        if len(string) > max_length:
            string = string[:max_length]
        return f"{string}-{count}"

    def create_answer_dict(self) -> None:
        colours = ANSWER_COLOURS
        shuffle(colours)
        for index, colour in enumerate(colours):
            self.answer_dict[colour] = [*self.wrong_answers, self.answer][index]
            if index == 3:
                self.answer_colour = colour
                
    @property
    def image_path(self) -> str:
        return os.path.join(os.getcwd(), "Questions", "Images", f"{self.id}.png")
         
         
    def create_latex_form(self) -> None:
        self.latex_form = f"${self.question}$".replace("*", "\\times").replace("/", "\\div")
                
    def create_image(self) -> None:
        if os.path.isfile(self.image_path):
            return
        
        if not self.latex_form:
            self.create_latex_form()
        latex2image(self.latex_form, self.id)

    def __repr__(self) -> str:
        return (
            f"{self.terminal_question()}"
            f"Tags: {self.tags}\n"
            f"ID: {self.id}"
        )
        
    def terminal_question(self) -> str:
        return (
            f"Question:  {self.question}\n"
            "-------------------------\n"
            f"Blue:   {self.answer_dict["blue"]}\n"
            f"Orange: {self.answer_dict["orange"]}\n"
            f"Green:  {self.answer_dict["green"]}\n"
            f"Yellow: {self.answer_dict["yellow"]}\n"
            "-------------------------\n"
        )
        
    def print_question(self) -> None:
        print(self)
        
    def display_question(self) -> None:
        print(
            self.terminal_question()
            )
        
    def check_answer(self, guess_colour: str) -> bool:
        return self.answer_colour == guess_colour


class BaseQuestionSet:
    def __init__(self, questions: list[BaseQuestion] | None = None, shuffle_order: bool = False) -> None:
        self.questions: list[BaseQuestion] = [] if questions is None else questions
        if shuffle_order: 
            shuffle(self.questions)
        self.index = 0
        
    def add_questions(self, questions: list[BaseQuestion]) -> None:
        self.questions.extend(questions)
        
    def create_question_images(self) -> None:
        for question in self.questions:
            if Tags.EQUATION in question.tags:
                question.create_image()
        
    def next_index_valid(self) -> bool:
        if self.index + 1 >= len(self.questions):
            return False
        self.index += 1
        return True

    def get_next_question_data(self) -> BaseQuestion | None:
        return self.questions[self.index] if self.next_index_valid() else None
    
    def load_next_question(self) -> bool:
        return self.next_index_valid()
    
    def reset_index(self) -> None:
        self.index = 0
        
    def get_current_question_data(self) -> BaseQuestion:
        return self.questions[self.index]
    
    def get_question_data(self, index: int) -> BaseQuestion:
        return self.questions[index]
    
    def check_answer(self, guess_colour: str) -> bool:
        return self.get_current_question_data().check_answer(guess_colour)
    
             
if __name__ == "__main__":
    testing = BaseQuestion("The Question", "Answer", ["Wrong1", "Wrong2", "Wrong3"])

    print(testing)
    
    testing2 = BaseQuestion("1 + 5 * 2^2", "Answer 2", ["Wrong1 2", "Wrong2 2", "Wrong3 2"], [Tags.EQUATION])
    testing2.create_image()
    print(testing2)
