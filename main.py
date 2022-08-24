import json
import random

import PySimpleGUI as sg


def update_answer_buttons():
    for letter in letter_list:
        window["QUESTION_" + letter.upper()].Update(
            questions[i]["answer_" + letter])
        window["QUESTION_" + letter.upper()].Update(
            visible=True if questions[i]["answer_" + letter] != "" else False)
        window["QUESTION_" + letter.upper()].Update(button_color="gray")


if __name__ == '__main__':
    letter_list = ["a", "b", "c", "d", "e"]
    good = 0
    wrong = 0
    with open('questions.json') as q:
        questions = json.load(q)
        i = 0
        question = questions[i]
        layout = [[sg.Text(text=str(i+1) + ". question: \n" + question["question"], size=(80, None), key="QUESTION_TEXT", visible=True)]]
        for letter in letter_list:
            layout.append(
                [sg.Button(
                    question["answer_" + letter],
                    key="QUESTION_" + letter.upper(),
                    visible=True if question["answer_" + letter] != "" else False,
                    button_color="gray")]
            )
        layout.append([sg.Button("Previous", key="PREV_QUESTION", visible=True),
                       (sg.Button("Next one", key="NEXT_QUESTION", visible=True))])
        layout.append([sg.Button("Random question", key="RAND_QUESTION", visible=True)])
        layout.append([sg.Input(key="SCORES", readonly=True, size=20, default_text="Good 0/0 Wrong",
                                justification="center"),
                       sg.Button("Reset score", key="RESET_SCORE", visible=True)])

        window = sg.Window("ISTQB TAE Preparation", layout, resizable=False, auto_size_buttons=True, auto_size_text=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            for letter in letter_list:
                if "QUESTION_" + letter.upper() in event:
                    if letter in questions[i]["solution"]:
                        good += 1
                    else:
                        wrong += 1
                    for l in letter_list:
                        if l in questions[i]["solution"]:
                            window["QUESTION_" + l.upper()].Update(button_color="green")
                        else:
                            window["QUESTION_" + l.upper()].Update(button_color="red")
                    window["SCORES"].Update(f"Good {good}/{wrong} Wrong")

            if "PREV_QUESTION" in event:
                i = i - 1
                if i < 0:
                    i = len(questions) - 1

                window["QUESTION_TEXT"].Update(str(i+1) + ". question: \n" + questions[i]["question"])
                update_answer_buttons()

            if "NEXT_QUESTION" in event:
                i += 1
                if i >= len(questions):
                    i = 0
                window["QUESTION_TEXT"].Update(str(i+1) + ". question: \n" + questions[i]["question"])
                update_answer_buttons()
            if "RAND_QUESTION" in event:
                i = random.randint(0, 40)
                if i >= len(questions):
                    i = 0
                window["QUESTION_TEXT"].Update(str(i+1) + ". question: \n" + questions[i]["question"])
                update_answer_buttons()
            if "RESET_SCORE" in event:
                good = 0
                wrong = 0
                window["SCORES"].Update(f"Good {good}/{wrong} Wrong")

        window.close()
