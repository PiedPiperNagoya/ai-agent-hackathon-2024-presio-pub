import uuid
import time
from collections import Counter

from google.cloud.firestore_v1.base_query import FieldFilter
from services import firestore as firestore_service

def exec(project_info: dict, reference_files_name: list, video_file_name, generated_markdown: str):
    """
    生成したMDを、コレクションに登録する
    """
    markdown_info = {}
    # すでに登録されているものがある確認
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
        markdown_info = {
            "id": markdown_target["id"],
            "project_id": markdown_target["project_id"],
            "reference_files_name": markdown_target["reference_files_name"],
            "video_file_name": markdown_target["video_file_name"],
            "created_at": markdown_target["created_at"],
            "updated_at": int(time.time()),
        }
        markdown_info["generated_markdown"] = generated_markdown
        firestore_service.update_data(
            collection="markdowns", document=markdown_target["id"], data=markdown_info
        )
    else:
        # 新規登録のためのデータ作成
        markdown_id = str(uuid.uuid4())
        created_at = int(time.time())
        updated_at = int(time.time())
        markdown_info = {
            "id": markdown_id,
            "project_id": project_info["id"],
            "reference_files_name": reference_files_name,
            "video_file_name": video_file_name,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        markdown_info["generated_markdown"] = generated_markdown
        firestore_service.create_data(
            collection="markdowns", document=markdown_id, data=markdown_info
        )