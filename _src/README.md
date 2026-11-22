# Site sources

The HTML pages in the repository root and in `fr/` are **generated**. Edit the sources here, then rebuild.

- `parts/` English page bodies, `parts_fr/` French page bodies (each starts with a small metadata block)
- `tpl/` shared header, footer and structured data
- `build.py` assembles everything: `python3 _src/build.py`

Always edit the part file, never the generated page, or the next rebuild overwrites your change.
Change the English and French parts together so the two languages stay in step.

## Live open-source numbers

`scripts/update_stats.py` refreshes `data/opensource.json` from GitHub's public API.
The workflow `.github/workflows/update-stats.yml` runs it daily and can be started by hand
from the Actions tab. Elements marked `data-stat`, `data-pr` or `data-updated` read that file.

Private repositories (for example aces/CBIGR) are invisible to the public API, so their counts
come from `data/private_offsets.json`. Update that file by hand when your private contributions change.
