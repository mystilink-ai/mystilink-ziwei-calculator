# Mystilink Calculateur Zi Wei

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Aperçu

Calcule une carte natale Zi Wei Dou Shu (Étoile pourpre) de style San He à partir d’une date-heure civile locale, d’un fuseau horaire et du genre. La sortie couvre quatorze étoiles majeures, étoiles auxiliaires, douze dieux, plages décennales (大限), fortune annuelle optionnelle (流年), quatre piliers, et si-hua optionnel avec attribution de palais. Les résultats sont émis en JSON.

## Plateformes et langages

| Cible | Livraison |
|-------|----------|
| Python | Paquet installable `mystilink-ziwei-calculator` et CLI `ziwei` |
| C | En-tête + bibliothèque qui exécute le CLI et renvoie du JSON |
| C++ | Enveloppe légère sur l’API C |
| C# | Enveloppe de processus autour du CLI |
| Java | Enveloppe ProcessBuilder autour du CLI |
| JavaScript / Node | Même paquet npm ; Node lance le CLI par défaut ; le navigateur injecte une fonction `runCli` |

Contrat pour les liaisons non-Python : invoquer l’exécutable `ziwei` (ou le chemin de l’env `MYSTILINK_ZIWEI_CLI`) et analyser le JSON sur stdout. L’alias `mystilink-ziwei` reste installé.

## Prérequis

- Python 3.9+
- Dépendance : `zhdate` (déclarée dans `pyproject.toml`)

## Installation

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
# optional lunar engine (Python 3.10+)
python3 -m pip install -e '.[lunar]'
```

Vérifier :

```bash
ziwei version
```

## CLI

Imprime toujours du JSON sur stdout en cas de succès.

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

| Indicateur | Obligatoire | Description |
|------------|-------------|-------------|
| `--datetime` | sauf `--birth-json` | Heure civile locale `YYYY-MM-DD HH:MM` |
| `--timezone` | sauf `--birth-json` | Nom de fuseau IANA |
| `--gender` | sauf BirthProfile | `male` ou `female` |
| `--birth-json` | non | BirthProfile (`mystilink.birth/0.1`) : fichier, `-`, ou JSON en ligne |
| `--midnight-zi` | non | `same-day` (défaut) ou `next-day` pour la règle de jour lunaire en 子时 tardif |
| `--si-hua` | non | Inclure le si-hua de l’année de naissance avec palais |
| `--year` | non | Année grégorienne pour les libellés de fortune annuelle |
| `--longitude` | non | Degrés est-positifs ; active la correction de temps solaire vrai |
| `--calendar-engine` | non | `builtin` (zhdate, défaut), `lunar` (extra optionnel), ou `external_basis` |
| `--calendar-basis` | non | JSON calendar-basis / lunar convert externe (fichier, `-`, ou en ligne) |
| `--envelope` | non | Envelopper en `mystilink.envelope/0.1` (défaut : carte nue) |
| `--locale` | non | Locale BCP 47 pour l’enveloppe |

Le JSON de carte inclut `schema_version` : `mystilink.ziwei.chart/0.1` et `calendar_engine`.
Les moteurs lunar/external peuvent intégrer `calendar_basis`.

### Version

```bash
ziwei version
```

Aussi : `python -m mystilink_ziwei …`

## API Python

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

## Exemples

Des exemples minimaux exécutables se trouvent sous `examples/` :

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

Tous les exemples n’utilisent que des date-heures fictives.

## Schema

Des brouillons JSON Schema pour les formes d’entrée/sortie CLI sont sous `schema/`.

## Liaisons

Sources sous `bindings/{c,cpp,csharp,java,js,python}/`. Définir `MYSTILINK_ZIWEI_CLI` si l’exécutable n’est pas sur `PATH`.

## Licence

MIT. Voir [LICENSE](../../LICENSE).
