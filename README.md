# Site — Dra. Lanna Gomes

Site institucional e landing pages da Dra. Lanna Gomes — endocrinologista e
metabologista em Goiânia/GO. HTML e CSS estáticos, sem framework e sem build.

**Versão 1 para aprovação da cliente.**

## Páginas

| Arquivo | Página |
|---|---|
| `index.html` | Home |
| `emagrecimento.html` | Landing page — Emagrecimento e saúde metabólica |
| `climaterio-menopausa.html` | Landing page — Climatério e menopausa |
| `a-medica.html` | A médica |
| `instituto.html` | Vosso Instituto e o acompanhamento |
| `tecnologias.html` | Tecnologias integradas |

As duas landing pages são os destinos do Google Ads (uma campanha, dois grupos
de anúncios) e por isso têm cabeçalho enxuto, sem navegação.

## Estrutura

```
assets/site.css     sistema visual completo (tokens, componentes, interação)
assets/site.js      menu, reveal, contador, progresso — progressive enhancement
assets/img/         fotos
build-pages.py      gera as 5 páginas internas a partir de um shell comum
```

O site **não depende** do `build-pages.py` para funcionar: a saída são arquivos
`.html` comuns. O script existe para manter cabeçalho, rodapé e metadados
iguais em todas as páginas. Para regerar: `python build-pages.py`.

O `index.html` é editado à mão.

## Pendências antes de publicar em domínio próprio

- [ ] Depoimentos: selecionar avaliações do Google que atendam ao critério de
      sobriedade do art. 14, II, "g" da Res. CFM nº 2.336/2023 (há placeholders
      marcados no `index.html`)
- [ ] Formulário de contato: ainda não tem destino
- [ ] Confirmar o WhatsApp (62) 98210-2480
- [ ] Rodapé: registro do Vosso Instituto no CRM e diretor técnico-médico
      (exigidos pelo art. 5º da mesma resolução)
- [ ] Tag do Google Ads e conversão de WhatsApp
- [ ] Fotos novas em alta resolução

## Conformidade

Todo o texto segue a Resolução CFM nº 2.336/2023. Sem promessa de resultado,
sem antes e depois, com identificação médica completa no rodapé.

---

Desenvolvido pela 4R Mídia.
