import grequests
import json

class Question(object):
    def __init__(self, question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answer1 = incorrect_answer1
        self.incorrect_answer2 = incorrect_answer2
        self.incorrect_answer3 = incorrect_answer3


def exception_handler(request, exception):
    print('Request failed')

NUMBER_OF_QUIZZES = 100
QUESTIONS_PER_QUIZ = 10
QUESTIONS_PER_REQUEST = 50
QUIZ_DATA_API = 'https://opentdb.com/api.php?amount=50&type=multiple'

times = int((NUMBER_OF_QUIZZES * QUESTIONS_PER_QUIZ) / QUESTIONS_PER_REQUEST)

rs = (grequests.get(QUIZ_DATA_API) for t in range(0,  times))

responses = grequests.map(rs, exception_handler)

quizzes = []
quiz = []

for response in responses:
    data = json.loads(response.content)
    if data['response_code'] == 0:
        results = data['results']
   
        for result in results:
            
            question = Question(result['question'], result['correct_answer'], 
            result['incorrect_answers'][0],  result['incorrect_answers'][1],
            result['incorrect_answers'][2])

            quiz.append(question)
            if quiz.__len__() == 10:
                quizzes.append(quiz)
                quiz = []

print(quizzes)
    
    