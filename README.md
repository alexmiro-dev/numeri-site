# numeri-site

Páginas estáticas da política de privacidade do Numeri (pt em `public/index.html`, es em `public/es.html`), publicadas em
https://mirostudio.app pelo Cloudflare (Workers Builds, `npx wrangler deploy`, configuração em `wrangler.jsonc`).
Geradas por `python3 build.py [caminho do .md]` a partir de `docs/politica-de-privacidade.md` do repositório `numeri`;
o script aborta se sobrar trecho `PENDENTE`/`CONFERIR` e remove do texto público o que ainda não é verdade.
