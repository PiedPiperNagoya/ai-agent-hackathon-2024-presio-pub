import uuid

from google.cloud.firestore_v1.base_query import FieldFilter

from services import firestore as firestore_service


def exec(project_name: str, password: str):
    """
    既存プロジェクトかを確認し、プロジェクト情報を返す関数
    """
    project_info = {}
    projects_ref = firestore_service.read_data_where2(
        collection="projects",
        field_filter1=FieldFilter("name", "==", project_name),
        field_filter2=FieldFilter("password", "==", password),
    )
    for project in projects_ref:
        if project_name == project["name"] and password == project["password"]:
            project_info = {
                "id": project["id"],
                "name": project["name"],
                "password": project["password"],
                "reference_file_path": f"{project['id']}/reference-file",
                "video_path": f"{project['id']}/video",
            }
            break
    if not project_info:
        project_id = str(uuid.uuid4())
        project_info = {
            "id": project_id,
            "name": project_name,
            "password": password,
            "reference_file_path": f"{project_id}/reference-file",
            "video_path": f"{project_id}/video",
        }
        firestore_service.create_data(
            collection="projects", document=project_id, data=project_info
        )
    return project_info
