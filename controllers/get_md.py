import os
from collections import Counter

from services import vertex_ai as vertex_ai_service
from google.cloud.firestore_v1.base_query import FieldFilter
from services import firestore as firestore_service

BUCKET_NAME = os.environ["BUCKET_NAME"]


def exec(project_info: dict, reference_files_name: list[str], video_file_name: str):
    """Markdown取得

    Args:
        reference_files_name (str): 選択された参考資料のファイル名
        video_file_name (str): 選択されたビデオのファイル名

    Returns:
        Markdown
    """
    if not video_file_name:
        return ""
    # firebaseのmarkdownコレクションを検索し、参照ファイル・動画が一致するmdがあれば、そのmdを返却する。
    registered_markdowns = firestore_service.read_data_where3(
        collection="markdowns",
        field_filter1=FieldFilter("project_id", "==", project_info["id"]),
        field_filter2=FieldFilter("reference_files_name", "array_contains_any", reference_files_name),
        field_filter3=FieldFilter("video_file_name", "==", video_file_name),
    )
    # 参照ファイルが配列なので、要素が一致するかは以下で確認する。
    markdown_target = {}
    for ref in registered_markdowns:
        if Counter(ref["reference_files_name"]) == Counter(reference_files_name):
            # 同じ参照ファイル・動画の場合は1つしかレコードがないはずだが、念のため先頭のデータを使用する。
            markdown_target = ref
            break

    if markdown_target:
        generate_markdown = markdown_target["generated_markdown"]
    else:
        # project情報よりフォルダの情報を取得し、生成AIに投げる
        storage_refs_full_path = []
        storage_video_full_path = ""
        # Todo: Cloud storegeのフォルダパスによっては処理を修正する
        ref_prefix = project_info["reference_file_path"]
        video_prefix = project_info["video_path"]
        if reference_files_name:
            for reference_file_name in reference_files_name:
                storage_refs_full_path.append(f"{ref_prefix}/{reference_file_name}")
        storage_video_full_path = f"{video_prefix}/{video_file_name}"

        # 生成AI呼び出し
        generate_markdown = vertex_ai_service.generate_markdown(
            storage_refs_full_path, storage_video_full_path
        )
    return generate_markdown
