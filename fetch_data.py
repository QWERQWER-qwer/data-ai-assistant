import yfinance as yf
import json

TICKER = "NVDA"  # 원하는 종목으로 변경 가능 (예: TSLA, AAPL, BTC-USD)


def fetch_prices(ticker: str):
    """yfinance로 최근 1년 일별 시세를 받아 (date, value, memo) 리스트로 변환"""
    df = yf.Ticker(ticker).history(period="1y")
    records = []
    for date, row in df.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d"),        # 날짜 (예: 2026-09-15)
            "value": round(float(row["Close"]), 2),   # 종가
            "memo": f"거래량 {int(row['Volume']):,}"   # 그날의 거래량 메모
        })
    return records


def main():
    data = fetch_prices(TICKER)
    print(f"수집된 데이터 개수: {len(data)}개")
    print("최근 3개 미리보기:")
    for item in data[-3:]:
        print(item)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("data.json 저장 완료")


if __name__ == "__main__":
    main()