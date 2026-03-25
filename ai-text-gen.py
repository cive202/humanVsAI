import json
import subprocess

def generate(text):
    prompt = f"""Rewrite the following sentence in an AI-generated style.

Make it:
- slightly more formal
- structured and precise
- less conversational
- grammatically perfect

Do NOT change the meaning.
Keep the length similar.

Sentence:
"{text}"

Output only the rewritten sentence."""

    result = subprocess.run(
        ["ollama", "run", "gemma:2b-instruct"],
        input=prompt,
        text=True,
        capture_output=True
    )
    
    return result.stdout.strip()


with open("input.jsonl") as fin, open("output.jsonl", "a") as fout:
    for i, line in enumerate(fin):
        data = json.loads(line)
        
        ai_text = generate(data["human"])
        
        fout.write(json.dumps({
            "human": data["human"],
            "ai": ai_text
        }) + "\n")

        if i % 100 == 0:
            print(i)
