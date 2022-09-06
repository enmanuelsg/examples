import random

questions_set = {
    "prepositions": {
        "qa": [
            {"q": "Diamonds are imported____South Africa: ", "a": "from"},
            {"q": "Why is she always leaving her files lying___: ", "a": "around"},
            {"q": "He works___the center of the business district: ", "a": "in"},
            {"q": "Cairo stands___the river Nile: ", "a": "on"},
            {"q": "You can't see it___here but the theatre is just around the corner: ", "a": "from"},
            {"q": "You can't see it from here but the theatre is just___the corner: ", "a": "around"},
            {"q": "We went___Spain on our way from France to Portugal: ", "a": "to"},
            {"q": "We went to Spain on our way___France to Portugal: ", "a": "from"},
            {"q": "We went to Spain on our way from France___Portugal: ", "a": "to"},
        ],
        "choices": "FROM | IN | ON | TO | AROUND | UP | BEYOND",
    }
}

def get_question(question):
     qa = random.choice(question)
     return qa["q"], qa["a"]

def run_quiz(questions, question_qty):
     print("\n", "Choices:", questions["choices"], "\n")
     score = 0
     for i in range(question_qty):
          question, real_answer = get_question(questions["qa"])
          answer_given = input(question)
          if answer_given.lower().strip() == real_answer:
               print('CORRECT')
               score += 1
          else:
               print('ERROR. Correct answer:', real_answer)
     ratio = '{:.0%}'.format(score/question_qty)
     print("You got", score, "out of", question_qty, "\nScore:", ratio)

run_quiz(questions_set['prepositions'], 5)

