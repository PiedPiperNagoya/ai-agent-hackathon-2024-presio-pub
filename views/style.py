import os


def load_styles(file_path: str):
    """スタイルのカスタムファイル読み込み

    Args:
        file_path (str): 読み込み対象のファイルパス

    Returns:
        読み込み結果（True/False）
        読み込み内容
    """
    if not os.path.exists(file_path):
        return {"status": False, "result": None}
    content = None
    with open(file_path, encoding="utf-8", mode="r") as f:
        content = f.read()
    return {"status": True, "result": content}


# CSS読み込み
custom_css = load_styles("views/custom.css")["result"]
