import yaml
from pathlib import Path

ROOT = Path(__file__).parent

def load_texts(patterns):
    texts = []
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file():
                texts.append((path, path.read_text()))
    return texts

def main(target: str):
    deps = yaml.safe_load((ROOT / "deps.yaml").read_text())
    cfg = deps[target]
    sources = load_texts(cfg["sources"])
    prompt_parts = []
    for path, text in sources:
        prompt_parts.append(f"\n---FILE:{path}---\n{text}")
    full_prompt = "\n".join(prompt_parts)

    # TODO: call LLM here. For now, just dump the prompt so we see it works.
    output = f"# GENERATED {target}\n\nThis is where LLM output will go.\n"
    out_path = ROOT / cfg["outputs"][0]
    out_path.write_text(output)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    import sys
    target = sys.argv[1]
    main(target)

