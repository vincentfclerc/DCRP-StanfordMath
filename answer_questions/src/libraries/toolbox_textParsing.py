import re

def extract_final_bit(answer: str):
    """
    Utility function to extract the text between <A> and <\A>.
    Returns the content inside <A> ... <\A>, or an empty string if not found.
    """
    pattern = r"<A>(.*?)<\\A>"
    match = re.search(pattern, answer, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""