import re
JUNK = [r'READ MORE', r'RELATED ARTICLES', r'ADVERTISEMENT', r'SIGN UP TO NEWSLETTER', r'Join our channel']

def clean_html_text(text):
    if not text: return ''
    s = text
    for p in JUNK:
        s = re.sub(p, '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s+', ' ', s).strip()
    lines = [ln.strip() for ln in s.split('\n') if len(ln.strip())>40]
    return '\n'.join(lines)
