import base64
import os
import subprocess
import tempfile


def exec(marp_md: str):
    """受け取ったMarkdown文字列をテンポラリファイルに書き込み、Marp CLIでPDFスライドに変換して、HTMLとして返す。

    Args:
        marp_md (str): Marpによる変換対象のMarkdown

    Returns:
        HTML（PDFスライド）
    """
    # 一時的にMarkdownファイルを作成
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp_md:
        tmp_md_path = tmp_md.name
        tmp_md.write(marp_md.encode("utf-8"))

    # Marp CLI を使って PDF に変換
    pdf_path = tmp_md_path.replace(".md", ".pdf")
    cmd = ["marp", tmp_md_path, "--pdf", "-o", pdf_path]
    ## 画像ファイルを利用する場合は以下のように --allow-local-files を追加
    ## cmd = ["marp", tmp_md_path, "--pdf", "--allow-local-files", "-o", pdf_path]
    subprocess.run(cmd, check=True)

    # 生成されたPDFを読み込み
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # 不要ファイルを削除
    os.remove(tmp_md_path)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # Base64にエンコード
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # `<iframe>` タグに埋め込む
    # TODO: UIの調整
    iframe_html = f"""
    <iframe
        src="data:application/pdf;base64,{b64_pdf}"
        width="100%"
        height="480px"
        style="border:none;"
    ></iframe>
    """
    return iframe_html
