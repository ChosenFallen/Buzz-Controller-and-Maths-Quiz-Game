import random

from questions.baseQuestion import BaseQuestion, Tags


class ThreeTermBodmasQuestion(BaseQuestion):
    def __init__(self, sprite_groups) -> None:
        while True:
            operators = ["+", "-", "*", "/"]
            first_operator = random.choice(operators)
            operators.remove(first_operator)
            second_operator = random.choice(operators)
            first_number = random.randint(1, 10)
            second_number = random.randint(1, 10)
            third_number = random.randint(1, 10)

            question = f"{first_number} {first_operator} {second_number} {second_operator} {third_number}"
            answer = eval(question)
            if answer % 1 == 0:
                break

        answer = str(int(answer))
        wrong_answers: list[str] = []

        # Brackets around first step
        wrong_answer = str(
            int(
                eval(
                    f"({first_number} {first_operator} {second_number}) {second_operator} {third_number}"
                )
            )
        )
        if wrong_answer != answer:
            wrong_answers.append(wrong_answer)

        # Brackets around second step
        wrong_answer = str(
            int(
                eval(
                    f"{first_number} {first_operator} ({second_number} {second_operator} {third_number})"
                )
            )
        )
        if wrong_answer != answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

        while len(wrong_answers) < 3:
            wrong_answer = str(random.randint(1, 100))
            if wrong_answer != answer and wrong_answer not in wrong_answers:
                wrong_answers.append(wrong_answer)

        super().__init__(
            question,
            answer,
            wrong_answers,
            sprite_groups=sprite_groups,
            tags=[Tags.EQUATION],
        )


class FourTermBodmasQuestion(BaseQuestion):
    def __init__(self, sprite_groups) -> None:
        while True:
            base_operators = ["+", "-", "*", "/"]
            operators = [*base_operators]
            self.first_operator = random.choice(operators)
            operators.remove(self.first_operator)
            operators += base_operators
            self.second_operator = random.choice(operators)
            operators.remove(self.second_operator)
            operators += base_operators
            self.third_operator = random.choice(operators)
            self.first_number = random.randint(1, 10)
            self.second_number = random.randint(1, 10)
            self.third_number = random.randint(1, 10)
            self.fourth_number = random.randint(1, 10)

            question = f"{self.first_number} {self.first_operator} {self.second_number} {self.second_operator} {self.third_number} {self.third_operator} {self.fourth_number}"
            answer = eval(question)
            if answer % 1 == 0:
                break

        answer = str(int(answer))
        wrong_answers = self.calculate_wrong_answers(answer=answer)
        while len(wrong_answers) < 3:
            wrong_answer = str(random.randint(1, 100))
            if wrong_answer != answer and wrong_answer not in wrong_answers:
                wrong_answers.append(wrong_answer)

        super().__init__(question, answer, wrong_answers, sprite_groups=sprite_groups, tags=[Tags.EQUATION])

    def calculate_wrong_answers(self, answer: str = "") -> list[str]:
        wrong_answers: list[str] = []
        # Brackets around first step
        wrong_answer = str(
            int(
                eval(
                    f"({self.first_number} {self.first_operator} {self.second_number}) {self.second_operator} {self.third_number} {self.third_operator} {self.fourth_number}"
                )
            )
        )
        if wrong_answer != answer:
            wrong_answers.append(wrong_answer)

        # Brackets around second step
        wrong_answer = str(
            int(
                eval(
                    f"{self.first_number} {self.first_operator} ({self.second_number} {self.second_operator} {self.third_number}) {self.third_operator} {self.fourth_number}"
                )
            )
        )
        if wrong_answer != answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

        # Brackets around third step
        wrong_answer = str(
            int(
                eval(
                    f"{self.first_number} {self.first_operator} {self.second_number} {self.second_operator} ({self.third_number} {self.third_operator} {self.fourth_number})"
                )
            )
        )
        if wrong_answer != answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

        # Brackets around first and third step
        wrong_answer = str(
            int(
                eval(
                    f"({self.first_number} {self.first_operator} {self.second_number}) {self.second_operator} ({self.third_number} {self.third_operator} {self.fourth_number})"
                )
            )
        )
        if wrong_answer != answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

        if len(wrong_answers) > 3:
            wrong_answers = list(random.sample(wrong_answers, 3))
        return wrong_answers


# if __name__ == "__main__":
#     test1 = ThreeTermBodmasQuestion()
#     print(test1)

#     test2 = FourTermBodmasQuestion()
#     print(test2)
