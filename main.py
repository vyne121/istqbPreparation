"""
Provides some questions for TAE exam
"""
import json
import random

import PySimpleGUI as sg


def update_answer_buttons(current_question):
    """
        This function changes the text of questions based on current_question
        and resets the colour of each.
    :param current_question: is an object containing a single question
    """
    for let in letter_list:
        window["QUESTION_" + let.upper()].Update(current_question["answer_" + let])
        window["QUESTION_" + let.upper()].Update(
            visible=current_question["answer_" + let] != "")
        window["QUESTION_" + let.upper()].Update(button_color="gray")


def reveal_answer(current_question):
    """
        This function changes colours of the answer buttons based on the
        current_question's solution.
        If the answer is correct, the button will be green,
        if not the button will be red
    :param current_question: is an object containing a single question
    """
    for let in letter_list:
        window["QUESTION_" + let.upper()].Update(
            button_color="green" if let in current_question["solution"] else "red")


def toggle_answer_buttons(is_enabled=True):
    """
            This function toggles the work of the buttons' event fire on or off
        :param is_enabled: True (default) or False
        """
    for let in letter_list:
        window["QUESTION_" + let.upper()].Update(disabled=is_enabled)


if __name__ == '__main__':
    letter_list = ["a", "b", "c", "d", "e"]
    GOOD_ANSWER_COUNT = 0
    wrongs = []
    with open('questions.json', encoding="utf-8") as q:
        questions = json.load(q)
        original_questions = questions
        i = 0
        question = questions[i]
        layout = [[sg.Text(text=str(i + 1) + ". question: \n" + question["question"],
                           size=(80, None), key="QUESTION_TEXT")]]
        for letter in letter_list:
            layout.append([sg.Button(question["answer_" + letter], key="QUESTION_" + letter.upper(),
                                     visible=question["answer_" + letter] != "",
                                     button_color="gray")])
        layout.append([sg.Button("Previous", key="PREV_QUESTION"),
                       (sg.Button("Next one", key="NEXT_QUESTION"))])
        layout.append([sg.Button("Random question", key="RAND_QUESTION")])
        layout.append([sg.Input(key="SCORES", readonly=True, size=20, default_text="Good 0/0 Wrong",
                                justification="center"),
                       sg.Button("Reset score", key="RESET_SCORE")])
        layout.append([sg.Button("Review wrong answers", key="REVIEW_WRONG", visible=False)])
        layout.append([sg.Button("Previous", key="REVIEW_PREV", visible=False),
            sg.Button("Next", key="REVIEW_NEXT", visible=False),
            sg.Button("Back to questions", key="RESTORE_ORIGINAL", visible=False)])

        window = sg.Window("ISTQB TAE Preparation", layout, resizable=False, auto_size_buttons=True,
                           auto_size_text=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            for letter in letter_list:
                if "QUESTION_" + letter.upper() in event:
                    if len(questions) > 0:
                        if letter in questions[i]["solution"]:
                            GOOD_ANSWER_COUNT += 1
                        else:
                            wrongs.append(questions[i])
                            window["REVIEW_WRONG"].Update(visible=True)
                        reveal_answer(questions[i])
                        window["SCORES"].Update(f"Good {GOOD_ANSWER_COUNT}/{len(wrongs)} Wrong")
                        questions.pop(i)
            if "PREV_QUESTION" in event:
                if len(questions) > 0:
                    i = i - 1
                    if i < 0:
                        i = len(questions) - 1
                    window["QUESTION_TEXT"].Update(
                        str(i + 1) + ". question: \n" + questions[i]["question"])
                    update_answer_buttons(questions[i])
            if "NEXT_QUESTION" in event:
                if len(questions) > 0:
                    i += 1
                    if i >= len(questions):
                        i = 0
                    window["QUESTION_TEXT"].Update(
                        str(i + 1) + ". question: \n" + questions[i]["question"])
                    update_answer_buttons(questions[i])
            if "RAND_QUESTION" in event:
                if len(questions) > 0:
                    i = random.randint(0, len(questions) - 1)
                    if i >= len(questions):
                        i = 0
                    window["QUESTION_TEXT"].Update(
                        str(i + 1) + ". question: \n" + questions[i]["question"])
                    update_answer_buttons(questions[i])
            if "RESET_SCORE" in event:
                GOOD_ANSWER_COUNT = 0
                wrongs = []
                window["SCORES"].Update(f"Good {GOOD_ANSWER_COUNT}/{len(wrongs)} Wrong")
                window["REVIEW_WRONG"].Update(visible=False)
                questions = original_questions
            if "REVIEW_WRONG" in event:
                WRONG_COUNTER = 0
                window["QUESTION_TEXT"].Update(
                    str(WRONG_COUNTER + 1) + "/" + str(len(wrongs)) + "\n" + wrongs[WRONG_COUNTER][
                        "question"])
                update_answer_buttons(wrongs[WRONG_COUNTER])
                window["REVIEW_NEXT"].Update(visible=True)
                window["REVIEW_PREV"].Update(visible=True)
                window["PREV_QUESTION"].Update(visible=False)
                window["NEXT_QUESTION"].Update(visible=False)
                window["RAND_QUESTION"].Update(visible=False)
                window["RESET_SCORE"].Update(visible=False)
                window["RESTORE_ORIGINAL"].Update(visible=True)
                window["REVIEW_WRONG"].Update(visible=False)
                reveal_answer(wrongs[WRONG_COUNTER])
                toggle_answer_buttons(False)
                window.refresh()
            if "REVIEW_PREV" in event:
                WRONG_COUNTER -= 1
                if WRONG_COUNTER < 0:
                    WRONG_COUNTER = len(wrongs) - 1
                window["QUESTION_TEXT"].Update(
                    str(WRONG_COUNTER + 1) + "/" + str(len(wrongs)) + "\n" + wrongs[WRONG_COUNTER][
                        "question"])
                update_answer_buttons(wrongs[WRONG_COUNTER])
                reveal_answer(wrongs[WRONG_COUNTER])
                window.refresh()
            if "REVIEW_NEXT" in event:
                WRONG_COUNTER += 1
                if WRONG_COUNTER >= len(wrongs):
                    WRONG_COUNTER = 0
                window["QUESTION_TEXT"].Update(
                    str(WRONG_COUNTER + 1) + "/" + str(len(wrongs)) + "\n" + wrongs[WRONG_COUNTER][
                        "question"])
                update_answer_buttons(wrongs[WRONG_COUNTER])
                reveal_answer(wrongs[WRONG_COUNTER])
                window.refresh()
            if "RESTORE_ORIGINAL" in event:
                window["RESTORE_ORIGINAL"].Update(visible=False)
                window["REVIEW_NEXT"].Update(visible=False)
                window["REVIEW_PREV"].Update(visible=False)
                window["PREV_QUESTION"].Update(visible=True)
                window["NEXT_QUESTION"].Update(visible=True)
                window["RAND_QUESTION"].Update(visible=True)
                window["RESET_SCORE"].Update(visible=True)
                window["REVIEW_WRONG"].Update(visible=True)
                if len(questions) > 0:
                    window["QUESTION_TEXT"].Update(
                        str(i + 1) + ". question: \n" + questions[i]["question"])
                    update_answer_buttons(questions[i])
                window.refresh()

        window.close()
