import json


def load_data(path="data.json"):
    """저장된 data.json을 읽어 리스트로 반환"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_summary(data):
    """데이터 리스트를 받아 요약 정보(기간/개수/통계/추세)를 만든다"""
    if not data:
        return {"period": "", "count": 0, "metrics": {}, "trend": "데이터 없음"}

    values = [d["value"] for d in data]
    dates = [d["date"] for d in data]
    count = len(data)

    average = round(sum(values) / count, 2)
    maximum = max(values)
    minimum = min(values)
    latest = values[-1]

    # 최근 추세: 최근 30거래일 전 대비 변화율로 상승/하락/유지 판단
    window = 30 if count >= 30 else count
    past = values[-window]
    change_pct = round((latest - past) / past * 100, 1)
    if change_pct > 3:
        trend = f"상승 (최근 {window}거래일 {change_pct:+}%)"
    elif change_pct < -3:
        trend = f"하락 (최근 {window}거래일 {change_pct:+}%)"
    else:
        trend = f"유지 (최근 {window}거래일 {change_pct:+}%)"

    return {
        "period": f"{dates[0]} ~ {dates[-1]}",
        "count": count,
        "metrics": {
            "average": average,
            "max": maximum,
            "min": minimum,
            "latest": latest,
        },
        "trend": trend,
    }


def main():
    data = load_data()
    summary = make_summary(data)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()