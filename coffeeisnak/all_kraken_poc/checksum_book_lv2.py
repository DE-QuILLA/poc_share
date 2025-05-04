import zlib
from decimal import Decimal, ROUND_DOWN

def format_kraken_value(s: str) -> str:
    """Kraken 형식에 맞게 소수점 제거 및 앞자리 0 제거"""
    if not isinstance(s, str):
        s = str(Decimal(str(s)).quantize(Decimal('1.00000000'), rounding=ROUND_DOWN))
    return s.replace('.', '').lstrip('0') or '0'

def build_kraken_checksum_string(bids: list, asks: list) -> str:
    """
    상위 10개 asks (가격 오름차순) → 상위 10개 bids (가격 내림차순) 순서로 문자열 생성
    각 항목은 price + qty 문자열 (Kraken 포맷 적용)
    """
    entries = []
    for level in asks[:10]:
        entries.append(format_kraken_value(level['price']) + format_kraken_value(level['qty']))
    for level in bids[:10]:
        entries.append(format_kraken_value(level['price']) + format_kraken_value(level['qty']))
    return ''.join(entries)

def calculate_kraken_book_checksum(bids: list, asks: list) -> tuple[str, int]:
    """
    Kraken 방식으로 체크섬 문자열을 만들고 CRC32 체크섬을 계산
    반환값: (체크섬 문자열, 체크섬 정수값)
    """
    checksum_string = build_kraken_checksum_string(bids, asks)
    checksum = zlib.crc32(checksum_string.encode('utf-8')) & 0xffffffff
    return checksum



if __name__ == "__main__":
    raw_data = {
      "symbol": "DOGE/USD",
      "bids": [
        {
          "price": "0.1745618",
          "qty": "800.37130841"
        },
        {
          "price": "0.1745493",
          "qty": "10311.90000000"
        },
        {
          "price": "0.1745398",
          "qty": "19422.10055372"
        },
        {
          "price": "0.1745239",
          "qty": "21574.77174588"
        },
        {
          "price": "0.1745184",
          "qty": "3822.00000000"
        },
        {
          "price": "0.1745143",
          "qty": "1952.65758421"
        },
        {
          "price": "0.1745142",
          "qty": "7553.44059219"
        },
        {
          "price": "0.1745133",
          "qty": "31426.40228623"
        },
        {
          "price": "0.1745112",
          "qty": "69349.42438871"
        },
        {
          "price": "0.1745049",
          "qty": "5584.69792768"
        }
      ],
      "asks": [
        {
          "price": "0.1745619",
          "qty": "122.70685825"
        },
        {
          "price": "0.1745622",
          "qty": "33106.50514625"
        },
        {
          "price": "0.1745710",
          "qty": "24511.48671562"
        },
        {
          "price": "0.1745794",
          "qty": "3375.00000000"
        },
        {
          "price": "0.1745806",
          "qty": "24510.13221229"
        },
        {
          "price": "0.1745969",
          "qty": "3375.00000000"
        },
        {
          "price": "0.1746062",
          "qty": "2310.30958846"
        },
        {
          "price": "0.1746063",
          "qty": "1926.15348035"
        },
        {
          "price": "0.1746078",
          "qty": "10311.70000000"
        },
        {
          "price": "0.1746144",
          "qty": "3375.00000000"
        }
      ],
      "checksum": 1121828463
    }



    received_checksum = calculate_kraken_book_checksum(bids=raw_data["bids"], asks=raw_data["asks"])
    print("caculcated checksum: ", received_checksum)
    print("raw data's checksum: ", raw_data["checksum"])
    print("Is two hash values are same?: ", received_checksum == raw_data["checksum"])
