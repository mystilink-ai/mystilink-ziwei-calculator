# Mystilink 紫微斗数計算機

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

ローカル民用日時、タイムゾーン、性別から三合派紫微斗数の本命盤を計算します。出力は十四主星、輔星、十二神、大限、任意の流年、四柱、および宮位付きの任意の四化を含みます。結果は JSON で出力されます。

## プラットフォームと言語

| 対象 | 提供物 |
|------|--------|
| Python | インストール可能なパッケージ `mystilink-ziwei-calculator` と CLI `ziwei` |
| C | CLI を実行して JSON を返すヘッダ + ライブラリ |
| C++ | C API 上の薄いラッパー |
| C# | CLI 周りのプロセスラッパー |
| Java | CLI 周りの ProcessBuilder ラッパー |
| JavaScript / Node | 同一 npm パッケージ；Node はデフォルトで CLI を spawn；ブラウザは `runCli` を注入 |

非 Python バインディングの契約：実行ファイル `ziwei`（または環境変数 `MYSTILINK_ZIWEI_CLI` のパス）を呼び出し、stdout の JSON を解析。別名 `mystilink-ziwei` もインストールされます。

## 要件

- Python 3.9+
- 依存：`zhdate`（`pyproject.toml` に宣言）

## インストール

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
# optional lunar engine (Python 3.10+)
python3 -m pip install -e '.[lunar]'
```

確認：

```bash
ziwei version
```

## CLI

成功時は常に stdout に JSON を出力します。

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

| フラグ | 必須 | 説明 |
|--------|------|------|
| `--datetime` | `--birth-json` 以外 | ローカル民用時刻 `YYYY-MM-DD HH:MM` |
| `--timezone` | `--birth-json` 以外 | IANA タイムゾーン名 |
| `--gender` | BirthProfile 以外 | `male` または `female` |
| `--birth-json` | いいえ | BirthProfile（`mystilink.birth/0.1`）：ファイル、`-`、またはインライン JSON |
| `--midnight-zi` | いいえ | 遅い子時の旧暦日規則：`same-day`（デフォルト）または `next-day` |
| `--si-hua` | いいえ | 生年干の四化と宮位を含める |
| `--year` | いいえ | 流年ラベル用のグレゴリオ年 |
| `--longitude` | いいえ | 東経を正とする度；真太陽時補正を有効化 |
| `--calendar-engine` | いいえ | `builtin`（zhdate、デフォルト）、`lunar`（任意 extra）、または `external_basis` |
| `--calendar-basis` | いいえ | 外部 calendar-basis / lunar convert JSON（ファイル、`-`、またはインライン） |
| `--envelope` | いいえ | `mystilink.envelope/0.1` で包む（デフォルト：裸の盤） |
| `--locale` | いいえ | エンベロープ用 BCP 47 ロケール |

盤 JSON には `schema_version`：`mystilink.ziwei.chart/0.1` と `calendar_engine` が含まれます。
lunar/external エンジンは `calendar_basis` を埋め込む場合があります。

### Version

```bash
ziwei version
```

また：`python -m mystilink_ziwei …`

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

## 例

最小の実行可能サンプルは `examples/` にあります：

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

すべての例は架空の日時のみを使用します。

## Schema

CLI 入出力形状の JSON Schema 草案は `schema/` にあります。

## バインディング

ソースは `bindings/{c,cpp,csharp,java,js,python}/` にあります。実行ファイルが `PATH` にない場合は `MYSTILINK_ZIWEI_CLI` を設定してください。

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。
