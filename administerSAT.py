
import openai

import sys
import json
import time
import os

import pandas as pd

COMPLETIONS_MODEL = "text-davinci-002"
openai.api_key = os.environ['OPENAI_API_KEY']


writinganswer = "BCAACAABBDACDBBCBBAADAABCCBBDDBCCDCADCADACCDDCBBABDD"
writinganswer = [a for a in writinganswer]

readinganswer = "ABCCABADCCBACDBCCBDCDAADBADBBBDBCDBCDCCBDADD"
readinganswer = [a for a in readinganswer]

whitelist = set('abcdABCD')


COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 300,
    "model": COMPLETIONS_MODEL,
}


def test(answer, realanswer):
    right = 0
    wrong = 0
    for i in range(len(answer)):
        if answer[i] == realanswer[i]:
            right = right + 1
        else:
            wrong = wrong + 1
    return (right, wrong)

def prompt_gpt3(query):
    response = openai.Completion.create(
                    prompt=query,
                    **COMPLETIONS_API_PARAMS
            )   
    return response["choices"][0]["text"]


def prompt_chatgpt(query):
    print("TRYING")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ]
    )
    print(completion.choices[0].message)
    return (completion.choices[0].message)



def get_answers(dct, persona):
    initialPrompt = "I am going to give you an examination. Answer the following questions from the perspective of " +  persona + " with ONLY the correct letters.- do not articulate your reasoning behind the answers. I repeat, only respond with the letters \"A\", \"B\", \"C\", or \"D\""
    overarchingAnswer = ""
    for i in range(len(dct)):
        query = initialPrompt + "\n" + "\n".join(dct[str(i)])
        added = prompt_chatgpt(query)
        # added = prompt_gpt3(query)
    

        if "\n" in added:
            added = added.split("\n")
        else:
            added = added.split(")")
        for i in range(1, len(added)):
            if "Answer" in added[i]:
                added[i] = added[i][6:]
            toAdd = ''.join(filter(whitelist.__contains__, added[i]))
            if (len(toAdd) > 0):
                toAdd = toAdd[0]
            overarchingAnswer = overarchingAnswer + toAdd
            
    answer = ' '.join(filter(whitelist.__contains__, overarchingAnswer))[:87]
    answer = answer.split(" ")
    return answer

def answer_writing(
    persona: str,
    show_prompt: bool = False
) -> str:
    writing_file = open("json/writing.json", "r")
    writing_questions = json.load(writing_file)

    answer = get_answers(writing_questions, persona)
    right, wrong = test(answer, writinganswer)
    print("right: " + str(right))
    print("wrong: " + str(wrong))


def answer_reading(
    persona: str,
    show_prompt: bool = False
) -> str:
    reading_file = open("json/reading.json", "r")
    reading_questions = json.load(reading_file)   

    answer = get_answers(reading_questions, persona)
    right, wrong = test(answer, writinganswer)
    print("right: " + str(right))
    print("wrong: " + str(wrong))


def main():
    answer_writing(sys.argv[1])
    time.sleep(10)
    answer_reading(sys.argv[1])


if __name__ == "__main__":
    main()