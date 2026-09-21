# Mystilink Calculadora Zi Wei

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Resumen

Calcula una carta natal Zi Wei Dou Shu (Estrella Púrpura) de estilo San He a partir de una fecha-hora civil local, zona horaria y género. La salida cubre catorce estrellas mayores, estrellas auxiliares, doce dioses, rangos decenales (大限), fortuna anual opcional (流年), cuatro pilares y si-hua opcional con atribución de palacio. Los resultados se emiten como JSON.

## Plataformas e idiomas

| Objetivo | Entrega |
|----------|----------|
| Python | Paquete instalable `mystilink-ziwei-calculator` y CLI `ziwei` |
| C | Cabecera + biblioteca que ejecuta el CLI y devuelve JSON |
| C++ | Envoltorio ligero sobre la API C |
| C# | Envoltorio de proceso alrededor del CLI |
| Java | Envoltorio ProcessBuilder alrededor del CLI |
| JavaScript / Node | Mismo paquete npm; Node lanza el CLI por defecto; el navegador inyecta una función `runCli` |

Contrato para enlaces no Python: invocar el ejecutable `ziwei` (o la ruta de la env `MYSTILINK_ZIWEI_CLI`) y analizar el JSON en stdout. El alias `mystilink-ziwei` permanece instalado.

## Requisitos

- Python 3.9+
- Dependencia: `zhdate` (declarada en `pyproject.toml`)

## Instalación

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
# optional lunar engine (Python 3.10+)
python3 -m pip install -e '.[lunar]'
```

Verificar:

```bash
ziwei version
```

## CLI

Siempre imprime JSON en stdout en caso de éxito.

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

| Indicador | Obligatorio | Descripción |
|-----------|-------------|-------------|
| `--datetime` | salvo `--birth-json` | Hora civil local `YYYY-MM-DD HH:MM` |
| `--timezone` | salvo `--birth-json` | Nombre de zona IANA |
| `--gender` | salvo BirthProfile | `male` o `female` |
| `--birth-json` | no | BirthProfile (`mystilink.birth/0.1`): archivo, `-`, o JSON en línea |
| `--midnight-zi` | no | `same-day` (predeterminado) o `next-day` para la regla de día lunar del 子时 tardío |
| `--si-hua` | no | Incluir si-hua del año de nacimiento con palacio |
| `--year` | no | Año gregoriano para etiquetas de fortuna anual |
| `--longitude` | no | Grados este-positivos; habilita corrección de tiempo solar verdadero |
| `--calendar-engine` | no | `builtin` (zhdate, predeterminado), `lunar` (extra opcional), o `external_basis` |
| `--calendar-basis` | no | JSON calendar-basis / lunar convert externo (archivo, `-`, o en línea) |
| `--envelope` | no | Envolver como `mystilink.envelope/0.1` (predeterminado: carta desnuda) |
| `--locale` | no | Configuración regional BCP 47 para el sobre |

El JSON de la carta incluye `schema_version`: `mystilink.ziwei.chart/0.1` y `calendar_engine`.
Los motores lunar/external pueden incrustar `calendar_basis`.

### Version

```bash
ziwei version
```

También: `python -m mystilink_ziwei …`

## API de Python

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

## Ejemplos

Muestras mínimas ejecutables en `examples/`:

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

Todos los ejemplos usan solo fechas-horas ficticias.

## Schema

Borradores JSON Schema para formas de entrada/salida del CLI están en `schema/`.

## Enlaces

Fuentes en `bindings/{c,cpp,csharp,java,js,python}/`. Defina `MYSTILINK_ZIWEI_CLI` si el ejecutable no está en `PATH`.

## Licencia

MIT. Véase [LICENSE](../../LICENSE).
