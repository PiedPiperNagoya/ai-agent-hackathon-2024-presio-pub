import os

import gradio as gr

from controllers import get_reference_file_names as get_reference_file_names_controller
from services import cloud_storage as cloud_storage_services

BUCKET_NAME = os.environ["BUCKET_NAME"]


def exec(file_path_list: list, select_reference_files: list, project_info: dict):
    """ファイルのアップロード（複数可）

    Args:
        file_path_list (list): アップロードした一時ファイルパスリスト
        select_reference_files (list): 選択済みファイルリスト
        project_info (dict): プロジェクト情報

    Returns:
        gradio.Dropdown (ファイルリスト更新)
    """
    # Cloud Storageのフォルダパスを指定
    dir_path = project_info["reference_file_path"]
    file_names = []
    for file_path in file_path_list:
        file_content = None
        with open(file_path, "rb") as f:
            file_content = f.read()
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(dir_path, file_name)
        # Cloud Storageにアップロード
        cloud_storage_services.upload_bytes_to_gcs(
            BUCKET_NAME, file_content, dest_path, "application/pdf"
        )
        file_names.append(file_name)
    choices = get_reference_file_names_controller.get_list(project_info=project_info)
    value = select_reference_files + file_names
    return gr.Dropdown(choices=choices, value=value)
