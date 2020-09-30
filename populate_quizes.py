import grequests
import json
import mysql.connector

cnx = mysql.connector.connect(host='localhost', user='mobile', database='quizzes')

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


cursor = cnx.cursor()
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
                quizName = 'Quiz ' + str(quizzes.__len__())
                data_quiz = (quizName,)
                add_quiz = "INSERT INTO quiz (name) VALUES(%s)"

                cursor.execute(add_quiz, data_quiz)

                quiz_id = cursor.lastrowid

                for question in quiz:

                    add_question = ("INSERT INTO questions "
                        "(question, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3) "
                        "VALUES(%s, %s, %s, %s, %s)")

                    data_question = (question.question, question.correct_answer, question.incorrect_answer1, 
                                    question.incorrect_answer2, question.incorrect_answer3)

                    cursor.execute(add_question, data_question)

                    question_id = cursor.lastrowid

                    add_quiz_question = ("INSERT INTO quiz_questions "
                                        "VALUES(%s, %s)")
                    data_quiz_questions = (quiz_id, question_id)
                    cursor.execute(add_quiz_question, data_quiz_questions)

                quiz = []

cnx.commit()

print('Quizzes are created')
    
    