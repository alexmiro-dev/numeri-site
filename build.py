# Gera index.html (pt) e es.html a partir de docs/politica-de-privacidade.md do repositório numeri.
import re, html, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else '../numeri/docs/politica-de-privacidade.md'
src = open(SRC, encoding='utf8').read()
# Versão pública: sem afirmar o que ainda não é verdade (hospedagem e bloqueio no AdMob); ver backlog.
for a, b in [
    (r' (?:e bloqueamos categorias sensíveis|y bloqueamos categorías sensibles) \[PEND[^\]]*\]', ''),
    (r'Os servidores ficam em \[PEND[^\]]*\]\. ', ''),
    (r'Los servidores están en \[PEND[^\]]*\]\. ', ''),
    (r' \[PEND[^\]]*\]', ''),
]:
    src = re.sub(a, b, src)
date = re.search(r'Última atualização: (.*)', src).group(1)
pt = src.split('## Português')[1].split('\n---\n')[0]
es = src.split('## Español')[1]
assert not re.search(r'PEND|CONFERIR', pt + es), 'ainda há trecho pendente'
def inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(https?://[^\s<]+)', r'<a href="\1">\1</a>', t)
    return re.sub(r'\[(?:CONFERIR|PENDENTE|PENDIENTE)[^\]]*\]', lambda m: '<mark>' + m.group(0) + '</mark>', t)
CSS = '''body{font:16px/1.6 system-ui,sans-serif;max-width:42rem;margin:0 auto;padding:1rem 16px;color:#1b1b1b;background:#fff}
h1{font-size:1.5rem}h2{font-size:1.1rem;margin-top:1.6rem}.d{color:#555}mark{background:#ffe08a;color:#000}
@media(prefers-color-scheme:dark){body{background:#121212;color:#e8e8e8}.d{color:#aaa}a{color:#8ab4f8}}'''
def conv(md, title, lang, upd):
    out = [f'<p class="d">{upd}</p>']; para = []; li = []
    def fp():
        nonlocal para
        if para: out.append('<p>' + inline(' '.join(para)) + '</p>'); para = []
    def fl():
        nonlocal li
        if li: out.append('<ul>' + ''.join('<li>' + inline(' '.join(x)) + '</li>' for x in li) + '</ul>'); li = []
    for l in md.split('\n'):
        if l.startswith('### '): fp(); fl(); out.append('<h2>' + inline(l[4:]) + '</h2>')
        elif l.startswith('- '): fp(); li.append([l[2:]])
        elif l.startswith('  ') and li: li[-1].append(l.strip())
        elif not l.strip(): fp(); fl()
        elif l.startswith('Última a'): fp(); fl()
        else: fl(); para.append(l.strip())
    fp(); fl()
    return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>\n'
            f'<style>{CSS}</style></head>\n<body><h1>{title}</h1>{"".join(out)}'
            '<p><a href="./">Português</a> · <a href="es.html">Español</a></p></body></html>')
open('public/index.html', 'w', encoding='utf8').write(conv(pt, 'Política de privacidade do Numeri', 'pt-BR', f'Última atualização: {date}'))
open('public/es.html', 'w', encoding='utf8').write(conv(es, 'Política de privacidad de Numeri', 'es', f'Última actualización: {date}'))
