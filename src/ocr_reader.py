def ocr_extract(path):
    try:
        from PIL import Image
        import pytesseract
    except Exception as e:
        return '', ''
    try:
        img = Image.open(path).convert('L')
        text = pytesseract.image_to_string(img, lang='eng')
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not lines:
            return '', ''
        title = lines[0]
        body = '\n'.join(lines[1:]) if len(lines)>1 else ''
        return title, body
    except Exception:
        return '', ''
