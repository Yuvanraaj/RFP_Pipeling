from pathlib import Path

def append_parsed_text(docs, source_pdf):
    output_file = Path("parsed/all_parsed_output.txt")
    output_file.parent.mkdir(exist_ok=True)

    content = f"\n\n===== 📄 {source_pdf} =====\n\n"
    content += "\n\n".join([doc.page_content for doc in docs])

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(content)

    return str(output_file)
