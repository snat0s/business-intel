import os
import yaml
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).parent
client = OpenAI()

# hard limits
MAX_CHARS_TOTAL = 120_000   # below model limit
MAX_CHARS_PER_FILE = 12_000 # big enough for atoms + prompt

def load_texts(patterns):
    texts = []
    total = 0
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            text = path.read_text()
            if len(text) > MAX_CHARS_PER_FILE:
                text = text[:MAX_CHARS_PER_FILE]
            if total + len(text) > MAX_CHARS_TOTAL:
                # stop adding more files
                return texts
            texts.append((path, text))
            total += len(text)
    return texts

def build_prompt(target_name: str, sources):
    parts = [
        f"You are generating: {target_name}",
        "You will receive several files. Use only their content.",
        "If information is missing because of truncation, say so in a 'Gaps' section."
    ]
    for path, text in sources:
        parts.append(f"\nFILE: {path}\n{text}")
    return "\n\n".join(parts)

def call_llm(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise business document generator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content

def main(target: str):
    deps = yaml.safe_load((ROOT / "deps.yaml").read_text())
    cfg = deps[target]
    sources = load_texts(cfg["sources"])
    prompt = build_prompt(target, sources)
    output = call_llm(prompt)
    out_path = ROOT / cfg["outputs"][0]
    out_path.write_text(output)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
