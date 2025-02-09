import os

import gradio as gr

from controllers import get_video_names as get_video_names_controller
from services import cloud_storage as cloud_storage_services

BUCKET_NAME = os.environ["BUCKET_NAME"]


def exec(file_path: str, project_info: dict):
    """ファイルのアップロード（複数可）

    Args:
        file_path (str): アップロードした一時ファイルパス
        project_info (dict): プロジェクト情報

    Returns:
        gradio.Dropdown (ファイルリスト更新)
    """
    # Cloud Storageのフォルダパスを指定
    dir_path = project_info["video_path"]
    file_content = None
    with open(file_path, "rb") as f:
        file_content = f.read()
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(dir_path, file_name)
    # Cloud Storageにアップロード
    cloud_storage_services.upload_bytes_to_gcs(
        BUCKET_NAME, file_content, dest_path, "video/mp4"
    )
    choices = get_video_names_controller.get_list(project_info=project_info)
    value = file_name
    return gr.Dropdown(choices=choices, value=value)
