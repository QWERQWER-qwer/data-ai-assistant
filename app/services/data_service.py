from app.database import db
from analyze import make_summary  # 2단계에서 만든 요약 함수 재사용

COLLECTION = "data"


def create_data(item: dict) -> dict:
    """새 데이터 추가 (자동 ID 생성)"""
    doc_ref = db.collection(COLLECTION).document()
    doc_ref.set(item)
    return {"id": doc_ref.id, **item}


def get_all_data() -> list:
    """전체 데이터 목록 조회 (날짜순 정렬)"""
    docs = db.collection(COLLECTION).order_by("date").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def update_data(doc_id: str, fields: dict):
    """데이터 수정 (없으면 None 반환)"""
    doc_ref = db.collection(COLLECTION).document(doc_id)
    if not doc_ref.get().exists:
        return None
    doc_ref.update(fields)
    updated = doc_ref.get()
    return {"id": updated.id, **updated.to_dict()}


def delete_data(doc_id: str) -> bool:
    """데이터 삭제 (없으면 False 반환)"""
    doc_ref = db.collection(COLLECTION).document(doc_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True


def get_summary() -> dict:
    """전체 데이터를 요약해서 반환"""
    data = get_all_data()
    return make_summary(data)