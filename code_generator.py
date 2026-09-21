def save_python_file(filename, code):

    code = code.replace("```python", "")
    code = code.replace("```", "")
    code = code.strip()

    with open(filename, "w", encoding="utf-8") as file:
        file.write(code)

    return filename