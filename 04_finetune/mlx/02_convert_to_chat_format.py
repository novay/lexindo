import json
import os


def convert_file(input_path, output_path):
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            try:
                entry = json.loads(line.strip())
                if "conversations" in entry and isinstance(
                    entry["conversations"], list
                ):
                    messages = []
                    for msg in entry["conversations"]:
                        role = (
                            "user"
                            if msg["from"] == "human"
                            else "assistant"
                            if msg["from"] == "gpt"
                            else msg["from"]
                        )
                        messages.append({"role": role, "content": msg["value"].strip()})
                    new_entry = {"messages": messages}
                    outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")
                else:
                    print(f"Skipping invalid entry in {input_path}")
            except json.JSONDecodeError:
                print(f"Invalid JSON line in {input_path}")


# Proses semua file
files = ["train.jsonl", "val.jsonl", "test.jsonl"]  # tambah kalau ada test.jsonl
for fname in files:
    if os.path.exists(fname):
        input_p = fname
        output_p = f"converted_{fname}"
        convert_file(input_p, output_p)
        print(f"Converted {fname} → {output_p}")

print("Selesai! Gunakan file converted_*.jsonl untuk training.")
