# Mystilink 紫微斗数排盘

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

根据本地民用日期时间、时区与性别，计算三合派紫微斗数本命盘。结果包含十四主星、辅星/杂曜、四组十二神、大限区间、可选流年、四柱，以及可选的生年干四化（含落宫）。输出为 JSON。

## 平台与语言

| 目标 | 交付物 |
|------|--------|
| Python | 可安装包 `mystilink-ziwei-calculator` 与 CLI `ziwei` |
| C | 头文件 + 通过 CLI 取回 JSON 的库 |
| C++ | 对 C API 的薄封装 |
| C# | 调用 CLI 的进程封装 |
| Java | ProcessBuilder 封装 |
| JavaScript / Node | 同一 npm 包；Node 默认 spawn CLI；浏览器通过注入 `runCli` |

非 Python 绑定的契约：调用可执行文件 `ziwei`（或环境变量 `MYSTILINK_ZIWEI_CLI` 指定路径），解析标准输出中的 JSON。长别名 `mystilink-ziwei` 仍会安装。

## 环境要求

- Python 3.9+
- 依赖：`zhdate`（写在 `pyproject.toml`）

## 安装

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
# 可选 lunar 引擎（Python 3.10+）
python3 -m pip install -e '.[lunar]'
```

验证：

```bash
ziwei version
```

## 命令行

成功时始终向标准输出打印 JSON。

### 排盘

```bash
ziwei chart \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender male \
  --midnight-zi same-day \
  --si-hua \
  --year 2026 \
  --longitude 121.5
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--datetime` | 是 | 本地时间 `YYYY-MM-DD HH:MM` |
| `--timezone` | 是 | IANA 时区名 |
| `--gender` | 是 | `male` 或 `female` |
| `--midnight-zi` | 否 | 晚子时换日：`same-day`（默认）或 `next-day` |
| `--si-hua` | 否 | 输出生年干四化及落宫 |
| `--year` | 否 | 流年公历年份 |
| `--longitude` | 否 | 东经为正的经度；启用真太阳时修正 |
| `--calendar-engine` | 否 | `builtin`（zhdate，默认）、`lunar`（可选 extra）或 `external_basis` |
| `--calendar-basis` | 否 | 外部 calendar-basis / lunar convert JSON |
| `--envelope` | 否 | 包装为 `mystilink.envelope/0.1`（默认裸盘 JSON） |
| `--locale` | 否 | 信封 BCP 47 语言标签 |

盘面 JSON 含 `schema_version`：`mystilink.ziwei.chart/0.1` 与 `calendar_engine`。
lunar / external_basis 可能嵌套 `calendar_basis`。

### 版本

```bash
ziwei version
```

亦可：`python -m mystilink_ziwei …`

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

## 示例

最小可运行示例位于 `examples/`：

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

示例仅使用虚构时间。

## Schema

CLI 入参/出参 JSON Schema 草稿见 `schema/`。

## 绑定

源码位于 `bindings/{c,cpp,csharp,java,js,python}/`。若可执行文件不在 `PATH`，请设置 `MYSTILINK_ZIWEI_CLI`。

## 许可

MIT。见 [LICENSE](../../LICENSE)。
