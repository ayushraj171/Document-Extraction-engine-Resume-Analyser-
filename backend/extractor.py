import fitz


def extract_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""

        for page in doc:
            t = page.get_text()
            if t:
                text += t

        doc.close()
        return text

    except Exception as e:
        return f"ERROR: {str(e)}"
