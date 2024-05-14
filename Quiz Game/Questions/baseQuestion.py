from random import shuffle


class BaseQuestion:
    def __init__(self, question: str, answer: str, wrong_answers: list[str]) -> None:
        self.question: str = question
        self.answer: str = answer
        self.wrong_answers: list[str] = wrong_answers
        assert len(self.wrong_answers) == 3
        self.answer_colour: str = ""
        self.answer_dict: dict[str, str] = {}
        self.create_answer_dict()

    def create_answer_dict(self) -> None:
        colours = ["yellow", "green", "orange", "blue"]
        shuffle(colours)
        for index, colour in enumerate(colours):
            self.answer_dict[colour] = [*self.wrong_answers, self.answer][index]
            if index == 3:
                self.answer_colour = colour

    def __repr__(self) -> str:
        return (
            f"Question:  {self.question}\n"
            "-------------------------\n"
            f"Yellow: {self.answer_dict["yellow"]}\n"
            f"Green:  {self.answer_dict["green"]}\n"
            f"Orange: {self.answer_dict["orange"]}\n"
            f"Blue:   {self.answer_dict["blue"]}\n"
            "-------------------------\n"   
            f"Answer: {self.answer}\n"
            f"Colour: {self.answer_colour}"
        )
        
        
if __name__ == "__main__":
    testing = BaseQuestion("The Question", "Answer", ["Wrong1", "Wrong2", "Wrong3"])

    print(testing)
