import json
import subprocess
import os

input_file = "human_data_5k_sample.jsonl"    # your human data
output_file = "output_5k.jsonl"  # AI generated
batch_size = 50               # process 50 at a time (adjustable)

# Resume from last line if output_file exists
start_index = 0
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        start_index = sum(1 for _ in f)
    print(f"Resuming from line {start_index}")

# Function to generate AI text via Ollama
def generate_ai(text):
    prompt = f"""Rewrite the following sentence in an AI-generated style:
- slightly formal
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

# Process input file
with open(input_file, "r") as fin, open(output_file, "a") as fout:
    for i, line in enumerate(fin):
        if i < start_index:
            continue  # skip already processed lines

        data = json.loads(line)
        human_text = data["text"]
        ai_text = generate_ai(human_text)

        fout.write(json.dumps({
            "id": data["id"],
            "human": human_text,
            "ai": ai_text
        }) + "\n")

        if i % 10 == 0:
            print(f"Processed {i} rows")
