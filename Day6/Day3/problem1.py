from openai import OpenAI
import json
import os

# ----------------------------------------
# Create a client to communicate with
# Ollama Cloud
# ----------------------------------------

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.environ["OLLAMA_API_KEY"]
)

# ----------------------------------------
# Collect school information from the user
# ----------------------------------------

print("Welcome to PackPal!\n")

classes = input("Enter tomorrow's classes: ").strip()

assignments = input("Enter assignments/tests: ").strip()

activities = input("Enter extracurricular activities: ").strip()

special_notes = input("Enter special notes: ").strip()

# Check that the user entered some information

if not classes and not assignments and not activities and not special_notes:

    print("Please enter some school information.")

else:

    # Combine all information into one formatted string

    student_info = f"""
Classes:
{classes}

Assignments:
{assignments}

Activities:
{activities}

Special Notes:
{special_notes}
"""

    print("\nStudent Information")
    print(student_info)

    # ----------------------------------------
    # Prompt sent to the AI
    # ----------------------------------------

    prompt = f"""
You are PackPal, an intelligent backpack assistant.

Your job is to help students prepare for school tomorrow.

Analyze the student's schedule and think like an organized student.

Infer reasonable school supplies.

Do NOT simply repeat the input.

If something is uncertain, place it under "items_to_confirm".

Return ONLY valid JSON.

Use exactly this format:

{{
    "must_pack": [],
    "to_complete": [],
    "activity_items": [],
    "prepare_tonight": [],
    "items_to_confirm": []
}}

Student Information:

{student_info}
"""

    try:

        # ----------------------------------------
        # Send the prompt to Ollama Cloud
        # ----------------------------------------

        response = client.chat.completions.create(
            model="gpt-oss:120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are PackPal, an AI backpack organizer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # ----------------------------------------
        # Extract AI response
        # ----------------------------------------

        result = response.choices[0].message.content

        print("\nPACKPAL RESULT\n", result)

        # ----------------------------------------
        # Convert JSON string into Python dictionary
        # ----------------------------------------

        checklist = json.loads(result)

        print("\nPACKPAL CHECKLIST\n", checklist)

        # ----------------------------------------
        # Display each section nicely
        # ----------------------------------------

        print("\nMust Pack")
        for item in checklist["must_pack"]:
            print(f"• {item}")

        print("\nTo Complete")
        for item in checklist["to_complete"]:
            print(f"• {item}")

        print("\nActivity Items")
        for item in checklist["activity_items"]:
            print(f"• {item}")

        print("\nPrepare Tonight")
        for item in checklist["prepare_tonight"]:
            print(f"• {item}")

        print("\nItems to Confirm")
        for item in checklist["items_to_confirm"]:
            print(f"• {item}")

        # ----------------------------------------
        # Print the full JSON
        # ----------------------------------------

        print("\nRaw JSON")
        print(json.dumps(checklist, indent=4))

    except json.JSONDecodeError:

        print("The AI did not return valid JSON.")

        print("\nAI Response:")
        print(result)

    except Exception as e:

        print("Sorry, we couldn't reach the AI service.")

        print(e)
