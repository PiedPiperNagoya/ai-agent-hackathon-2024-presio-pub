import os

import gradio as gr

from services import cloud_storage as cloud_storage_services

BUCKET_NAME = os.environ["BUCKET_NAME"]


def exec(project_info: dict):
    """指定ディレクトリのファイルリスト取得

    Args:
        project_info (dict): プロジェクト情報

    Returns:
        結果（True/False）
        内容
    """
    # Cloud Storageのフォルダパスを指定
    dir_path = project_info["video_path"]
    # 格納されているファイル名のみを取得
    files = cloud_storage_services.get_files_name(BUCKET_NAME, dir_path)
    return gr.Dropdown(choices=files)


def get_list(project_info: dict):
    dir_path = project_info["video_path"]
    files = cloud_storage_services.get_files_name(BUCKET_NAME, dir_path)
    return files
