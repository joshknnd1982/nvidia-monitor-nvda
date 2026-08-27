# NVIDIA Monitor — NVDA add-on

Read the temperature, memory use, clock speeds, power draw and other live
statistics of an NVIDIA graphics card from anywhere in Windows, using a single
keystroke. Built for [NVDA](https://www.nvaccess.org/), the free open-source
screen reader.

Every reading is announced by NVDA and, if you press the same shortcut twice,
copied to the clipboard.

> **This is a downstream build.** The add-on is written and maintained by
> **José Pérez** and **ayoub** at
> [JosePerezHuanca/NVIDIAMonitor](https://github.com/JosePerezHuanca/NVIDIAMonitor).
> This repository tracks their source and adds a Russian translation.
> See [Relationship to upstream](#relationship-to-upstream).

## Requirements

- NVDA 2024.1 or later (tested up to 2026.1)
- An NVIDIA GPU with a working driver, on 64-bit x86 Windows

## Installing

Download the `.nvda-addon` file from the
[Releases page](https://github.com/joshknnd1982/nvidia-monitor-nvda/releases)
and press Enter on it, or use *Tools → Add-on store → Install from external
source* in NVDA.

## Shortcuts

All shortcuts can be reassigned under *Preferences → Input gestures →
NVIDIAMonitor*. Press twice to copy the value to the clipboard.

| Shortcut | Reports |
| --- | --- |
| `NVDA+alt+G` | GPU name / model |
| `NVDA+alt+U` | GPU UUID |
| `NVDA+alt+V` | Driver version |
| `NVDA+ctrl+alt+V` | BIOS version |
| `NVDA+alt+1` | GPU load |
| `NVDA+alt+2` | Memory load |
| `NVDA+alt+3` | Free memory |
| `NVDA+alt+4` | Used memory |
| `NVDA+alt+5` | Total memory |
| `NVDA+alt+6` | GPU temperature |
| `NVDA+alt+7` | Power consumption |
| `NVDA+alt+8` | Power limit |
| `NVDA+alt+9` | Number of CUDA processes |
| `NVDA+alt+0` | Memory used by processes |
| `NVDA+ctrl+alt+1` | Fan speed |
| `NVDA+ctrl+alt+2` | GPU clock frequency |
| `NVDA+ctrl+alt+3` | Maximum GPU clock frequency |
| `NVDA+ctrl+alt+4` | SM clock frequency |
| `NVDA+ctrl+alt+5` | Maximum SM clock frequency |
| `NVDA+ctrl+alt+6` | Memory clock frequency |
| `NVDA+ctrl+alt+7` | Maximum memory clock frequency |
| `NVDA+ctrl+alt+8` | TX throughput |
| `NVDA+ctrl+alt+9` | RX throughput |
| `NVDA+ctrl+alt+0` | Power state |

Not every card exposes every value. Where the driver reports a reading as
unsupported — fan speed and power limit are the usual ones on laptop GPUs — the
add-on says so rather than staying silent.

## How it works

The add-on talks to NVIDIA's management library (NVML) through
[pynvml](https://github.com/gpuopenanalytics/pynvml), and picks its backend
from the NVDA version it is running under:

| NVDA | Backend |
| --- | --- |
| 2026.1 and later (64-bit) | `pynvml` imported directly into the NVDA process |
| 2024.1 – 2025.x (32-bit) | bundled `NVIDIAScript.exe` helper, driven over a pipe |

NVDA 2026.1 moved to 64-bit Python 3.13, which is what makes the in-process
path possible; on older 32-bit builds the add-on shells out to a 64-bit helper
instead. Readings are cached for one second, so holding a key down does not
hammer the driver.

Errors are appended to `NVIDIAMonitor.log` in your NVDA configuration folder.

## Languages

The add-on is written in English. It also ships:

- **Español** — by the original authors
- **Русский** — added in this repository, based on the nvda.ru translation of
  version 1.0

Translations live in `addon/locale/<lang>/LC_MESSAGES/nvda.po`, and the user
documentation in `addon/doc/<lang>/readme.md`.

## Building from source

Upstream builds with [SCons](https://scons.org/) and the standard NVDA add-on
template, which needs the GNU gettext binaries (`msgfmt`, `xgettext`) on your
`PATH`:

```bash
pip install scons markdown && scons
```

If you do not have the gettext binaries — they are not part of a normal Windows
Python install — `build.py` produces the same `.nvda-addon` using only Python's
bundled `msgfmt.py`:

```bash
pip install markdown && python build.py
```

Both write `NVIDIAMonitor-<version>.nvda-addon` to the repository root.

## Relationship to upstream

This repository is a fork of
[JosePerezHuanca/NVIDIAMonitor](https://github.com/JosePerezHuanca/NVIDIAMonitor),
with full commit history preserved. The add-on itself — including the English
base language and the NVDA 2026.1 pynvml backend — is the original authors'
work.

Changes made here, on top of upstream `2.1`:

- Added the Russian translation (`addon/locale/ru`, `addon/doc/ru`), including
  the two `buildVars.py` strings upstream's catalogues omit, so the add-on's
  name and description are translated in NVDA's Add-on Manager too.
  The catalogue is generated from strings extracted out of the sources rather
  than copied from upstream's Spanish catalogue, which is stale for six unit
  strings (`{label}: {bytes:.2f} GB` and friends gained a space that the
  translations never picked up, so those units show untranslated).
- Fixed `write_log` opening its log file without an encoding. Because it is
  called before the callback that speaks the message, a translated error whose
  characters the system code page cannot represent raised `UnicodeEncodeError`
  and the user heard nothing at all. Not yet reported upstream; the fix and the
  stale catalogue entries above are both worth sending back.
- Added `build.py`, so the add-on can be built without the GNU gettext binaries.
- Guarded the root-readme copy in `sconstruct` so a repo-level `README.md`
  cannot overwrite the English add-on documentation on case-insensitive file
  systems.
- Version set to `2.1.1` to distinguish this build from upstream's own `2.1`.

If you want the add-on itself, prefer
[upstream's releases](https://github.com/JosePerezHuanca/NVIDIAMonitor/releases)
unless you specifically want the Russian translation. Bug reports about the
add-on's behaviour belong upstream; report packaging or translation problems
here.

## Licence

GPL-2.0, the same as upstream — see [LICENSE](LICENSE) and
[COPYING.txt](COPYING.txt). Copyright © 2024 José Pérez and ayoub.
