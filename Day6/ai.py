from openai import OpenAI

# 1. DELETE THE OLD KEY AND PASTE YOUR REAL API KEY HERE
key = "e055b7a1f83946da8fbc619eb5887ef3.bOrTjki1mc1OQbmBsNwyk9IM"

model = "gpt-oss:20b"

ai = OpenAI(
    base_url="https://ollama.com/v1", # Make sure this matches your key's provider!
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
        "Fix the spelling and grammar. "
        "Return only the fixed text:\n\n" + note
    )

    print("\n" + note)


def generate():
    global note

    prompt = input("\nWhat should I write? ")

    result = ask(
        "Write this for me. "
        "Return only the text:\n\n" + prompt
    )

    note += "\n" + result
    print("\n" + result)


while True:

    try:
        print("\n--- AI NOTEPAD ---")
        print("Model:", model)
        print()

        note = input("Write here: ")

        while True:

            print("\n--- MENU ---")
            print("1. AI Fix")
            print("2. AI Generate")
            print("3. Clear")
            print("4. Write Again")

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
        print("\nGoodbye!")
        break