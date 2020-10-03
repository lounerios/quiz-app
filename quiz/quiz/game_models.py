class GameQuestion(object):
    def __init__(self, id, question, answers):
        self.id = id
        self.question = question
        self.answers = answers

class GameQuiz(object):
    def __init__(self, id, name, questions):
        self.id = id
        self.name = name
        self.questions = questions


class GameAnswer(object):
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class GameResult(object):
    def __init__(self, correct_answers):
        self.correct_answers = correct_answers