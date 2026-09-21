# Mystilink 자미두수 계산기

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 개요

로컬 민간 일시, 타임존, 성별로부터 삼합파 자미두수 본명반을 계산합니다. 출력은 14주성, 보성, 십이신, 대한 구간, 선택적 유년, 사주, 그리고 궁 귀속이 포함된 선택적 사화를 포함합니다. 결과는 JSON 으로 출력됩니다.

## 플랫폼 및 언어

| 대상 | 제공물 |
|------|--------|
| Python | 설치 가능 패키지 `mystilink-ziwei-calculator` 및 CLI `ziwei` |
| C | CLI 를 실행하고 JSON 을 반환하는 헤더 + 라이브러리 |
| C++ | C API 위의 얇은 래퍼 |
| C# | CLI 프로세스 래퍼 |
| Java | CLI ProcessBuilder 래퍼 |
| JavaScript / Node | 동일 npm 패키지; Node 는 기본으로 CLI spawn; 브라우저는 `runCli` 주입 |

비 Python 바인딩 계약: 실행 파일 `ziwei`(또는 환경 변수 `MYSTILINK_ZIWEI_CLI` 경로)를 호출하고 stdout JSON 을 파싱. 별칭 `mystilink-ziwei` 도 설치됩니다.

## 요구 사항

- Python 3.9+
- 의존성: `zhdate`(`pyproject.toml` 에 선언)

## 설치

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
# optional lunar engine (Python 3.10+)
python3 -m pip install -e '.[lunar]'
```

확인:

```bash
ziwei version
```

## CLI

성공 시 항상 stdout 에 JSON 을 출력합니다.

### Chart

```bash
ziwei chart \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender male \
  --midnight-zi same-day \
  --si-hua \
  --year 2026 \
  --longitude 121.5

ziwei chart --birth-json tests/fixtures/birth.profile.v0.json
```

| 플래그 | 필수 | 설명 |
|--------|------|------|
| `--datetime` | `--birth-json` 제외 | 로컬 민간 시각 `YYYY-MM-DD HH:MM` |
| `--timezone` | `--birth-json` 제외 | IANA 타임존 이름 |
| `--gender` | BirthProfile 제외 | `male` 또는 `female` |
| `--birth-json` | 아니요 | BirthProfile(`mystilink.birth/0.1`): 파일, `-`, 또는 인라인 JSON |
| `--midnight-zi` | 아니요 | 늦은 자시의 음력일 규칙: `same-day`(기본) 또는 `next-day` |
| `--si-hua` | 아니요 | 생년간 사화와 궁 포함 |
| `--year` | 아니요 | 유년 라벨용 그레고리력 연도 |
| `--longitude` | 아니요 | 동경 양수 도수; 진태양시 보정 활성화 |
| `--calendar-engine` | 아니요 | `builtin`(zhdate, 기본), `lunar`(선택 extra), 또는 `external_basis` |
| `--calendar-basis` | 아니요 | 외부 calendar-basis / lunar convert JSON(파일, `-`, 또는 인라인) |
| `--envelope` | 아니요 | `mystilink.envelope/0.1` 로 감쌈(기본: 원시 차트) |
| `--locale` | 아니요 | 엔벨로프용 BCP 47 로케일 |

차트 JSON 에는 `schema_version`: `mystilink.ziwei.chart/0.1` 및 `calendar_engine` 이 포함됩니다.
lunar/external 엔진은 `calendar_basis` 를 임베드할 수 있습니다.

### Version

```bash
ziwei version
```

또한: `python -m mystilink_ziwei …`

## Python API

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from mystilink_ziwei import ChartInput, compute_chart

chart = compute_chart(
    ChartInput(
        local_dt=datetime(1990, 5, 15, 14, 30, tzinfo=ZoneInfo("Asia/Shanghai")),
        midnight_zi="same-day",
        gender="male",
        include_si_hua=True,
        target_year=2026,
        longitude=121.5,
    )
)
```

## 예제

최소 실행 샘플은 `examples/` 에 있습니다:

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

모든 예제는 가상 일시만 사용합니다.

## Schema

CLI 입출력 형태의 JSON Schema 초안은 `schema/` 에 있습니다.

## 바인딩

소스는 `bindings/{c,cpp,csharp,java,js,python}/` 에 있습니다. 실행 파일이 `PATH` 에 없으면 `MYSTILINK_ZIWEI_CLI` 를 설정하세요.

## 라이선스

MIT. [LICENSE](../../LICENSE) 참조.
