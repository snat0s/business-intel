from pathlib import Path
import datetime

ROOT = Path(__file__).parent
RAW = ROOT / "raw"
OUT = ROOT / "atoms" / "auto"

ATOM_TEMPLATE = """---
id: {id}
type: {type}
topic: "{topic}"
source: "{source}"
created_at: {created_at}
confidence: {confidence}
---
{body}
"""

def fake_llm_extract_insights(text: str):
    # placeholder: split by double newlines
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    insights = []
    for i, c in enumerate(chunks, 1):
        insights.append({
            "id": f"auto.{i}",
            "type": "unsorted",
            "topic": "unsorted",
            "body": c
        })
    return insights

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for raw_file in RAW.glob("*.md"):
        raw_text = raw_file.read_text()
        insights = fake_llm_extract_insights(raw_text)
        for ins in insights:
            fname = f"{raw_file.stem}-{ins['id']}.md"
            out_path = OUT / fname
            out_path.write_text(ATOM_TEMPLATE.format(
                id=f"{raw_file.stem}-{ins['id']}",
                type=ins["type"],
                topic=ins["topic"],
                source=str(raw_file),
                created_at=datetime.date.today().isoformat(),
                confidence=0.5,
                body=ins["body"]
            ))
            print("wrote", out_path)

if __name__ == "__main__":
    main()

