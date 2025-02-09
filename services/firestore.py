import os

import google.auth
from google.cloud import firestore

creds, project_id = google.auth.load_credentials_from_file(
    "/app/configs/ai-agent-hackathon-2024.json"
)

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
db = firestore.Client(credentials=creds, project=GCP_PROJECT_ID)


# データを追加する関数
def create_data(collection: str, document: str, data):
    ## ID自動生成の場合
    if document == "":
        ref = db.collection(collection).add(data)
    ## ID指定の場合
    else:
        ref = db.collection(collection).document(document).set(data, merge=True)
    return ref


# データを取得する関数
def read_data(collection: str, document: str):
    ref = db.collection(collection).document(document).get()
    return ref.to_dict()


# Where句を利用して複数データをリストで取得する関数
def read_data_where(collection: str, field_filter):
    docs = db.collection(collection).where(filter=field_filter).stream()
    ref_list = []
    for doc in docs:
        ref_list.append(doc.to_dict())
    return ref_list


# Where句を2つ利用して複数データをリストで取得する関数
def read_data_where2(collection: str, field_filter1, field_filter2):
    docs = (
        db.collection(collection)
        .where(filter=field_filter1)
        .where(filter=field_filter2)
        .stream()
    )
    ref_list = []
    for doc in docs:
        ref_list.append(doc.to_dict())
    return ref_list

# Where句を3つ利用して複数データをリストで取得する関数
def read_data_where3(collection: str, field_filter1, field_filter2, field_filter3):
    docs = (
        db.collection(collection)
        .where(filter=field_filter1)
        .where(filter=field_filter2)
        .where(filter=field_filter3)
        .stream()
    )
    ref_list = []
    for doc in docs:
        ref_list.append(doc.to_dict())
    return ref_list


# 全てのデータをリストで取得する関数
def read_all_data(collection: str):
    docs = db.collection(collection).stream()
    ref_list = []
    for doc in docs:
        ref_list.append(doc.to_dict())
    return ref_list


# データを更新する関数
def update_data(collection: str, document: str, data):
    ref = db.collection(collection).document(document).update(data)
    return ref


# データを削除する関数
def delete_data(collection: str, document: str):
    ref = db.collection(collection).document(document).delete()
    return ref
