#!/usr/bin/env bash
# Изгражда EPUB и PDF в папка build/.
# Изисквания: Python 3 с pypandoc_binary; Node.js с @mermaid-js/mermaid-cli и puppeteer;
# Chromium (път в променливата CHROMIUM, по подразбиране /opt/pw-browsers/chromium).
set -euo pipefail
cd "$(dirname "$0")/.."
CHROMIUM="${CHROMIUM:-/opt/pw-browsers/chromium}"
MMDC="${MMDC:-npx mmdc}"
mkdir -p build/fig
echo "{\"executablePath\": \"$CHROMIUM\", \"args\": [\"--no-sandbox\"]}" > build/puppeteer.json
python3 - <<'PY'
import re, glob
for f in sorted(glob.glob('glavi/*.md')):
    m = re.search(r'```mermaid\n(.*?)```', open(f).read(), re.S)
    open(f'build/fig/fig{f.split("/")[-1][:2]}.mmd', 'w').write(m.group(1))
PY
for f in build/fig/*.mmd; do $MMDC -q -p build/puppeteer.json -s 2 -b white -w 1000 -i "$f" -o "${f%.mmd}.png"; done
python3 tools/assemble_book.py
python3 - <<'PY'
import pypandoc
common = ['--metadata-file=tools/meta.yaml', '--toc', '--toc-depth=1', '--resource-path=.']
pypandoc.convert_file('build/book.md', 'epub3', outputfile='build/diferencialna-diagnoza.epub',
                      extra_args=common + ['--split-level=1', '--css=tools/epub.css'])
pypandoc.convert_file('build/book.md', 'html5', outputfile='build/book.html',
                      extra_args=common + ['--standalone', '--embed-resources', '--css=tools/print.css',
                                           '--metadata=pagetitle:Диференциална диагноза'])
PY
node tools/topdf.js "$PWD/build/book.html" build/diferencialna-diagnoza.pdf
echo "Готово: build/diferencialna-diagnoza.epub и build/diferencialna-diagnoza.pdf"
