"""Сглобява всички глави и приложения в build/book.md (за EPUB и PDF)."""
import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, 'build')
def clean(s, ch=None):
    # remove navigation block
    s = re.sub(r'\n<!-- навигация -->\n(?:.|\n)*$', '\n', s)
    # mermaid -> image
    if ch:
        def img(m):
            t = re.search(r'accTitle: (.*)', m.group(0))
            alt = (t.group(1).strip() + '. Текстовото описание е под фигурата.') if t else 'Диагностичен алгоритъм'
            return f'![{alt}]({BUILD}/fig/fig{ch}.png)'
        s = re.sub(r'```mermaid\n.*?```', img, s, flags=re.S)
    # details/summary -> printable
    s = re.sub(r'<details>\s*\n?<summary>(.*?)</summary>', r'**\1**', s)
    s = s.replace('</details>', '')
    # cross-file links -> text
    s = re.sub(r'\[([^\]]+)\]\((?:\.\./)?(?:(?:glavi|prilozhenia)/)?[A-Za-z0-9_-]+\.md(?:#[^)]*)?\)', r'\1', s)
    return s.strip() + '\n'
readme = open(f'{ROOT}/README.md').read()
parts = []
# front matter from README: everything except the contents list
front = readme.split('## Съдържание')[0]
back = '## Политика за актуализация' + readme.split('## Политика за актуализация')[1]
front = re.sub(r'^# .*\n+### .*\n', '', front)  # drop title lines (metadata title used)
parts.append('# Предговор и указания {.unnumbered}\n\n' + clean(front).replace('## Предговор\n', ''))
parts.append('# За учебника {.unnumbered}\n\n' + clean(back))
for f in sorted(glob.glob(f'{ROOT}/glavi/*.md')):
    ch = os.path.basename(f)[:2]
    parts.append(clean(open(f).read(), ch))
for code in ['a', 'b', 'v', 'g', 'd', 'e', 'zh']:
    f = glob.glob(f'{ROOT}/prilozhenia/{code}-*.md')[0]
    parts.append(clean(open(f).read()))
book = '\n\n'.join(parts)
open(f'{BUILD}/book.md', 'w').write(book)
print(len(book), 'chars;', book.count('\n# '), 'H1')
