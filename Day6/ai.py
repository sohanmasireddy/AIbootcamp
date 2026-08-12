import streamlit as st

st.title("AIpad")
st.write("Write Here")
from openai import OpenAI

key = "df966d7c23ac4b7e9867dd556e4855e5.DEl_7lZ9KLPiVPWsGquzIHmQ"

model = "gpt-oss:20b-cloud"

ai = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=key
)

note = ""

def ask(prompt):
    r = ai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def fix():
    global note

    if not note:
        print("Nothing to fix.")
        return

    note = ask(
        "Fix the code or text. "
        "Return only the fixed text or code:\n\n" + note
    )

    print("\n" + note)

def generate():
    global note

    prompt = input("\nPrompt ")

    result = ask(
        "Generate this. "
        "Return only the text or code:\n\n" + prompt
    )

    note += "\n" + result
    print("\n" + result)


while True:

    try:
        print("\n    AI NOTEPAD    ")
        print()

        note = input("Write here: ")

        while True:

            print("\n    MENU    ")
            print("1. AI Fix")
            print("2. AI Generate")
            print("3. Clear")
            print("4. Rewrite")

            choice = input("\nChoose: ")

            if choice == "1":
                fix()

            elif choice == "2":
                generate()

            elif choice == "3":
                note = ""
                print("Cleared.")

            elif choice == "4":
                break

            else:
                print("Choose a number from 1 to 4.")

    except KeyboardInterrupt:
        print("\nEnd")
        break