from markitdown import MarkItDown

md = MarkItDown()


def convert_to_md(file_path: str):
    result = md.convert(file_path)
    return result.text_content
