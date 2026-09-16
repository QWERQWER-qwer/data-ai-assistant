from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL
from app.services.data_service import get_summary
from app.services.conversation_service import create_conversation

# base URL이 있으면 그걸로(코디세이), 없으면 기본 OpenAI로 연결
if OPENAI_BASE_URL:
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
else:
    client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-5-mini"  # 코디세이 제공 모델


def build_system_prompt(summary: dict) -> str:
    """데이터 요약을 시스템 프롬프트로 만든다 (컨텍스트 주입)"""
    metrics = summary.get("metrics", {})
    return (
        "당신은 사용자의 데이터를 분석해주는 친절한 AI 비서입니다.\n\n"
        "[사용자 데이터 요약]\n"
        f"- 데이터 기간: {summary.get('period')}\n"
        f"- 총 레코드: {summary.get('count')}개\n"
        f"- 주요 지표: {metrics}\n"
        f"- 최근 트렌드: {summary.get('trend')}\n\n"
        "위 데이터를 근거로 사용자 질문에 맞춤형으로 답하세요. "
        "숫자를 말할 때는 위 요약 값을 사용하세요."
    )


def chat(user_message: str, history: list) -> dict:
    # 1) 데이터 요약 조회
    summary = get_summary()
    # 2) 요약을 시스템 프롬프트에 삽입
    system_prompt = build_system_prompt(summary)

    messages = [{"role": "system", "content": system_prompt}]
    messages += history                                    # 이전 대화 이어붙이기
    messages.append({"role": "user", "content": user_message})

    # 3) GPT 호출
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_completion_tokens=2000,   # 응답 길이 제한 (비용/토큰 절약)
    )
    answer = response.choices[0].message.content

    # 4) 대화 자동 저장 (system 프롬프트는 빼고 저장)
    saved_messages = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": answer},
    ]
    conv = create_conversation({
        "title": user_message[:20],
        "messages": saved_messages,
    })

    return {"answer": answer, "conversation_id": conv["id"]}