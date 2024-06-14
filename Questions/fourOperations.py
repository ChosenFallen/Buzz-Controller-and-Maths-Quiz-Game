import random

from constants import *
from questions.baseQuestion import BaseQuestion


class FourOperationsQuestion(BaseQuestion):
    def __init__(
        self,
        sprite_groups,
        *,
        operators=None,
        include_negatives=False,
        integer_answer=True,
        difficulty=DIFFICULTY.EASY,
    ) -> None:
        if operators is None:
            operators = ["+", "-", "*", "/"]
        while True:
            chosen_operator = random.choice(operators)
            match difficulty:
                case DIFFICULTY.EASY:
                    max_number = 10
                case DIFFICULTY.MEDIUM:
                    max_number = 25
                case DIFFICULTY.HARD:
                    max_number = 100

            if chosen_operator in ["+", "-"]:
                max_number *= max_number

            min_number = -max_number if include_negatives else 0

            first_number = random.randint(min_number, max_number)
            second_number = random.randint(min_number, max_number)

            match chosen_operator:
                case "+" | "-" | "*":
                    question = f"{first_number} {chosen_operator} {second_number}"
                    answer = str(eval(question))
                case "/":
                    if first_number == 0:
                        continue
                    question = f"{first_number * second_number} / {first_number}"
                    answer = str(second_number)

            wrong_answers = self.create_wrong_answers(
                chosen_operator, answer, first_number, second_number
            )

            break

        super().__init__(
            question=question,
            answer=str(answer),
            wrong_answers=wrong_answers,
            sprite_groups=sprite_groups,
        )

    def create_wrong_answers(
        self, operator: str, correct_answer: str, first_number: int, second_number: int
    ) -> list[str]:
        pass
