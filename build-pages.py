# -*- coding: utf-8 -*-
"""
Gera as páginas internas e as landing pages a partir de um shell compartilhado.
A saída são arquivos .html estáticos comuns — o site não depende deste script
para funcionar; ele existe para manter cabeçalho, rodapé e metadados iguais
em todas as páginas.

Uso:  python build-pages.py
"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

WA = "https://wa.me/5562982102480"
def wa(msg):
    from urllib.parse import quote
    return WA + "?text=" + quote(msg)

WA_HOME = wa("Olá! Vim pelo site e gostaria de informações sobre consulta com a Dra. Lanna.")
WA_EMAG = wa("Olá! Vim pelo site e gostaria de informações sobre o acompanhamento de emagrecimento.")
WA_CLIM = wa("Olá! Vim pelo site e gostaria de informações sobre avaliação de climatério e menopausa.")

ARROW = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

NAV_ITEMS = [
    ("index.html", "Início"),
    ("emagrecimento.html", "Emagrecimento"),
    ("climaterio-menopausa.html", "Climatério e menopausa"),
    ("a-medica.html", "A médica"),
    ("instituto.html", "O instituto"),
]

def header(current, lp=False):
    """lp=True → cabeçalho enxuto, sem navegação, para não vazar tráfego pago."""
    if lp:
        return f'''<header class="topbar">
  <div class="wrap topbar__in">
    <a class="brand" href="index.html">
      <span class="brand__name">Dra. Lanna Gomes</span>
      <span class="brand__tag">Endocrinologista e Metabologista</span>
    </a>
    <nav class="nav" aria-label="Principal">
      <a class="btn" href="{WA_HOME}" target="_blank" rel="noopener">Agendar consulta</a>
    </nav>
  </div>
</header>'''
    CUR = ' aria-current="page"'
    links = "\n".join(
        '        <a href="%s"%s>%s</a>' % (h, CUR if h == current else "", t)
        for h, t in NAV_ITEMS
    )
    return f'''<header class="topbar">
  <div class="wrap topbar__in">
    <a class="brand" href="index.html">
      <span class="brand__name">Dra. Lanna Gomes</span>
      <span class="brand__tag">Endocrinologista e Metabologista</span>
    </a>
    <nav class="nav" aria-label="Principal">
      <div class="nav__links">
{links}
      </div>
      <a class="btn btn--nav" href="{WA_HOME}" target="_blank" rel="noopener">Agendar consulta</a>
      <button class="navtoggle" aria-label="Abrir menu" aria-expanded="false">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </nav>
  </div>
</header>'''

CREDBAR = '''<div class="credbar">
  <div class="wrap">
    <ul>
      <li><strong>Dra. Lanna Gomes</strong></li>
      <li>Médica · CRM-GO 19.507</li>
      <li><strong>Endocrinologista e Metabologista · RQE 9.755</strong></li>
      <li>Mestra pela UNIFESP</li>
      <li>Membro titular da SBEM</li>
      <li>20 anos de formação médica</li>
      <li>Vosso Instituto · Órion Business &amp; Health Complex</li>
    </ul>
  </div>
</div>'''

CTA_NOTE = ("Nossa equipe informa valores, horários disponíveis e orientações "
            "para a consulta pelo WhatsApp.")


def leadform(origem):
    '''Formulário de contato. O destino fica em FORM_ENDPOINT (assets/site.js);
    enquanto ele estiver vazio, o envio abre o WhatsApp já preenchido, de modo
    que nenhum contato se perde. Sem JS o formulário não aparece — o botão do
    WhatsApp logo acima continua sendo o caminho.'''
    return f'''<form class="leadform" data-origem="{origem}" novalidate>
      <p class="leadform__intro">Prefere receber o contato da nossa equipe? Deixe seu WhatsApp.</p>
      <div class="leadform__row">
        <label class="leadform__field">
          <span>Nome</span>
          <input type="text" name="nome" autocomplete="name" placeholder="Como podemos te chamar" required>
        </label>
        <label class="leadform__field">
          <span>WhatsApp</span>
          <input type="tel" name="whatsapp" autocomplete="tel" inputmode="tel" placeholder="(62) 90000-0000" required>
        </label>
      </div>
      <button class="btn btn--light leadform__send" type="submit">Falar com a equipe</button>
      <p class="leadform__msg" role="status" aria-live="polite" hidden></p>
    </form>'''


def cta(title, text, link, note=CTA_NOTE, origem="site"):
    return f'''<section class="section cta">
  <div class="wrap cta__in reveal">
    <p class="eyebrow eyebrow--center">Primeiro passo</p>
    <h2 class="h-lg split">{title}</h2>
    <p class="lede">{text}</p>
    <a class="btn btn--light" href="{link}" target="_blank" rel="noopener">Quero agendar minha consulta {ARROW}</a>
    <p class="cta__note">{note}</p>
    {leadform(origem)}
  </div>
</section>'''

FOOTER = f'''<footer class="footer">
  <div class="wrap footer__grid">
    <div>
      <h4>Identificação</h4>
      <div class="crm">
        <b>Dra. Lanna Gomes</b>
        <span class="role">Médica</span>
        CRM-GO 19.507<br>
        Endocrinologista e Metabologista — RQE 9.755
      </div>
    </div>
    <div>
      <h4>Atendimento</h4>
      <ul>
        <li>Vosso Instituto</li>
        <li>Órion Business &amp; Health Complex</li>
        <li>Av. Portugal, 1148 — Salas 2407/2409</li>
        <li>Setor Marista, Goiânia/GO · 74150-030</li>
        <li style="margin-top:1rem"><a href="{WA}" target="_blank" rel="noopener">WhatsApp (62) 98210-2480</a></li>
      </ul>
    </div>
    <div>
      <h4>Navegação</h4>
      <ul>
        <li><a href="emagrecimento.html">Emagrecimento e saúde metabólica</a></li>
        <li><a href="climaterio-menopausa.html">Climatério e menopausa</a></li>
        <li><a href="a-medica.html">A médica</a></li>
        <li><a href="instituto.html">O instituto e o acompanhamento</a></li>
        <li><a href="tecnologias.html">Tecnologias integradas</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer__legal">
    <p>
      Este site tem caráter informativo e segue as normas de publicidade médica do Conselho Federal de Medicina
      (Res. CFM nº 2.336/2023). Não divulgamos promessas de resultado nem imagens de antes e depois.
      Nenhuma informação aqui substitui a consulta médica.
    </p>
    <p>© 2026 Dra. Lanna Gomes</p>
  </div>
</footer>'''

def wa_float(link):
    return f'''<a class="wa" href="{link}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">
  <svg width="27" height="27" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.7 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.6-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.2-.6-.4M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2m0 18.2c-1.6 0-3.2-.4-4.5-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2"/></svg>
</a>'''

def page(fname, title, desc, body, current=None, lp=False, walink=WA_HOME):
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=Karla:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<noscript><style>.leadform{{display:none}}</style></noscript>
</head>
<body>

{header(current, lp)}

{body}

{FOOTER}

{wa_float(walink)}

<script src="assets/site.js"></script>
</body>
</html>
'''
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("gerado:", fname)


def lp_hero(kicker, h1, sub, place, link, label="Quero agendar minha consulta"):
    return f'''<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__text">
      <p class="hero__kicker">{kicker}</p>
      <h1 class="h-xl h-xl--long split">{h1}</h1>
      <p class="lede hero__sub reveal">{sub}</p>
      <div class="hero__actions reveal" data-d="1">
        <a class="btn" href="{link}" target="_blank" rel="noopener">{label} {ARROW}</a>
      </div>
      <p class="hero__place reveal" data-d="2">{place}</p>
    </div>
    <div class="portrait reveal" data-d="1">
      <div class="portrait__frame">
        <img src="assets/img/lanna-hero.jpg" alt="Dra. Lanna Gomes, endocrinologista e metabologista em Goiânia" width="1080" height="1350">
      </div>
      <div class="portrait__badge">
        <b class="counter" data-count="20">20</b>
        <span>anos de formação médica</span>
      </div>
    </div>
  </div>
</section>'''


AUTORIDADE = '''<section class="section section--tight">
  <div class="wrap grid-2--even">
    <div class="portrait portrait--plain reveal">
      <div class="portrait__frame">
        <img src="assets/img/lanna-portrait.jpg" alt="Dra. Lanna Gomes" width="1080" height="1350" style="object-position:50% 18%">
      </div>
    </div>
    <div class="reveal" data-d="1">
      <p class="eyebrow">Quem conduz</p>
      <h2 class="h-md split">Dra. Lanna Gomes</h2>
      <div class="stack-lg" style="margin-top:1.3rem">
        <p>Com 20 anos de formação médica, a trajetória da Dra. Lanna Gomes foi construída sobre uma base sólida em Clínica Médica, Endocrinologia e Metabologia: dois anos de Residência Médica em Clínica Médica e, na sequência, dois anos de Residência Médica em Endocrinologia e Metabologia, depois da graduação pela Faculdade de Medicina de Marília (FAMEMA).</p>
        <p>É Endocrinologista e Metabologista, com RQE 9.755, Mestra em Ciências pela UNIFESP e membro titular da Sociedade Brasileira de Endocrinologia e Metabologia.</p>
        <p>Atendimento no Vosso Instituto, localizado no Órion Business &amp; Health Complex, no Setor Marista, em Goiânia.</p>
        <p style="margin-top:1.4rem"><a class="link-arrow" href="a-medica.html">Conhecer a trajetória completa</a></p>
      </div>
    </div>
  </div>
</section>'''


def steps_block(title, items, eyebrow="Como começa"):
    lis = "\n".join(f'''      <div class="step reveal">
        <div>
          <h3 class="h-sm">{t}</h3>
          <p>{d}</p>
        </div>
      </div>''' for t, d in items)
    return f'''<section class="section section--tight">
  <div class="wrap">
    <div class="reveal" style="max-width:44rem;margin-bottom:clamp(30px,3.5vw,48px)">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="h-lg split">{title}</h2>
    </div>
    <div class="steps">
{lis}
    </div>
  </div>
</section>'''


def faq_block(items, title="Dúvidas frequentes", eyebrow="Antes de agendar"):
    ds = "\n".join(f'''      <details{" open" if i == 0 else ""}>
        <summary>{q}</summary>
        <div class="faq__a"><p>{a}</p></div>
      </details>''' for i, (q, a) in enumerate(items))
    return f'''<section class="section section--tight">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="h-lg split">{title}</h2>
    </div>
    <div class="faq reveal" data-d="1">
{ds}
    </div>
  </div>
</section>'''


def checks(items):
    return "\n".join(f"      <li>{i}</li>" for i in items)


PASSOS = [
    ("Contato com a equipe", "Você fala com nossa equipe pelo WhatsApp e recebe todas as informações sobre a consulta."),
    ("Consulta médica", "Avaliação aprofundada com a Dra. Lanna Gomes, considerando sua história clínica, exame físico, composição corporal e exames disponíveis."),
    ("Definição da conduta", "A partir da avaliação, são definidos os próximos passos e, quando necessário, exames complementares, tratamento e estratégia de acompanhamento."),
    ("Acompanhamento quando indicado", "A frequência das consultas e reavaliações é individualizada de acordo com o diagnóstico, o tratamento e a necessidade de cada paciente."),
]

# =====================================================================
# 1. LP EMAGRECIMENTO
# =====================================================================
emag = f'''{lp_hero(
  'Emagrecimento e saúde metabólica <span>·</span> Goiânia/GO',
  'Emagrecimento com acompanhamento médico em Goiânia',
  'Avaliação do seu metabolismo, dos seus hormônios e da sua composição corporal, conduta individualizada e acompanhamento quando indicado, com a Dra. Lanna Gomes — Médica, CRM-GO 19.507, Endocrinologista e Metabologista, RQE 9.755, mestra pela UNIFESP e 20 anos de formação médica.',
  '<strong>Vosso Instituto</strong> <span class="dot">·</span> Órion Business &amp; Health Complex <span class="dot">·</span> Setor Marista, Goiânia — casos selecionados também online',
  WA_EMAG)}

{CREDBAR}

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Para quem é</p>
      <h2 class="h-lg split">Se você se reconhece aqui, a conversa é&nbsp;essa</h2>
    </div>
    <div class="reveal" data-d="1">
      <ul class="checks">
{checks([
  "Ganhou peso depois dos 35 sem ter mudado a alimentação",
  "Já fez dieta e acompanhamento nutricional, e o peso volta",
  "Sente cansaço constante, mesmo dormindo bem",
  "Percebeu a composição do corpo mudar — mais gordura abdominal, menos massa muscular",
  "Perdeu peso em algum momento, mas não conseguiu manter",
  "Desconfia que exista algo hormonal ou metabólico envolvido, mas nunca investigou a fundo",
])}
      </ul>
      <p class="pullquote">Antes de mudar a dieta, entender o que mudou no seu corpo.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="panel grid-2--even spot reveal">
      <div>
        <p class="eyebrow">O que é</p>
        <h2 class="h-md split">Emagrecimento médico não é dieta com receita</h2>
      </div>
      <div>
        <p>É um tratamento clínico conduzido por médica: avaliação da composição corporal, do perfil hormonal e metabólico e leitura dos seus exames antes de qualquer prescrição.</p>
        <p>A conduta é individualizada e pode incluir tratamento medicamentoso, estratégia nutricional, terapias nutricionais injetáveis por via endovenosa ou intramuscular e outros recursos terapêuticos, quando indicados.</p>
        <p style="margin-bottom:0"><strong>O que define o tratamento é o seu caso. Não um pacote.</strong></p>
      </div>
    </div>
  </div>
</section>

<section class="section dark spot">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Composição corporal</p>
      <h2 class="h-lg split">O número da balança não conta a história toda</h2>
    </div>
    <div class="reveal stack-lg" data-d="1">
      <p class="lede">Duas pessoas podem perder o mesmo peso e ter resultados clinicamente opostos: uma preservando massa muscular, outra perdendo músculo e piorando o próprio metabolismo.</p>
      <p>Por isso o tratamento acompanha mais do que o peso: composição corporal, massa muscular, parâmetros metabólicos e risco cardiometabólico. É esse conjunto que ajuda a entender como o seu corpo está respondendo — e o que torna possível sustentar o resultado ao longo do tempo.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">A investigação</p>
      <h2 class="h-lg split">Fatores que podem interferir no peso e na composição corporal</h2>
    </div>
    <div class="reveal" data-d="1">
      <ul class="checks">
{checks([
  "<strong>Resistência à insulina e alterações glicêmicas</strong>",
  "<strong>Função tireoidiana</strong> e outras alterações endócrinas, quando clinicamente indicadas",
  "<strong>Alterações hormonais do climatério e da pós-menopausa</strong>",
  "<strong>Deficiências de vitaminas e minerais</strong> que afetam energia e metabolismo",
  "<strong>Perda de massa muscular</strong> e mudanças na composição corporal",
  "<strong>Saúde intestinal e perfil alimentar individual</strong>, avaliados por testes funcionais e genéticos quando indicado",
  "<strong>Padrão de sono, rotina e histórico de tratamentos anteriores</strong>",
])}
      </ul>
      <p class="pullquote">Cada um desses fatores muda a conduta. Por isso a investigação vem antes da prescrição.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="panel spot reveal" style="text-align:center;max-width:52rem;margin-inline:auto">
      <p class="eyebrow eyebrow--center">Manutenção</p>
      <h2 class="h-md split">O tratamento não termina quando o peso muda</h2>
      <p style="margin:1.2rem auto 0;max-width:44rem">Por isso, acompanhar a evolução da composição corporal e, quando indicado, dos exames complementares ajuda a orientar decisões e ajustes de conduta ao longo do tratamento e também na fase de manutenção.</p>
    </div>
  </div>
</section>

{AUTORIDADE}

{steps_block("Como começa seu cuidado", PASSOS)}

{faq_block([
  ("Vocês prescrevem medicação para emagrecer?",
   "Medicação é uma das possibilidades, decidida caso a caso, com indicação, dose e monitoramento definidos em consulta. Ela entra dentro de um plano que inclui investigação, conduta nutricional e acompanhamento — nunca isolada e nunca sem avaliação."),
  ("Quanto custa o tratamento?",
   "A consulta é particular e o valor é informado pela nossa equipe antes do agendamento. O tratamento varia conforme o plano definido para o seu caso, e você decide depois de saber exatamente o que está sendo proposto."),
  ("Preciso levar exames?",
   "Se você tiver exames dos últimos 12 meses, leve — eles ajudam a montar o histórico. O que faltar, a Dra. Lanna solicita na consulta."),
  ("Vocês fazem avaliação de composição corporal?",
   "Sim. A avaliação da composição corporal faz parte do acompanhamento, porque acompanhar apenas o peso não mostra o que está acontecendo com massa muscular e gordura."),
  ("E se eu não puder ir presencialmente?",
   "Alguns casos podem ser acompanhados online, conforme critério médico. Fale com a equipe e avaliamos."),
])}

{cta("Comece pela avaliação médica",
     "A conduta só é definida depois de entender o que está acontecendo com o seu metabolismo, os seus hormônios e a sua composição corporal.",
     WA_EMAG, origem="emagrecimento")}'''

page("emagrecimento.html",
     "Emagrecimento com Acompanhamento Médico em Goiânia | Dra. Lanna Gomes",
     "Tratamento médico do emagrecimento com avaliação de metabolismo, hormônios e composição corporal, plano individualizado e acompanhamento. Setor Marista, Goiânia.",
     emag, lp=True, walink=WA_EMAG)

# =====================================================================
# 2. LP CLIMATÉRIO E MENOPAUSA
# =====================================================================
clim = f'''{lp_hero(
  'Climatério e menopausa <span>·</span> Goiânia/GO',
  'Climatério e menopausa: tratamento médico individualizado em Goiânia',
  'Avaliação hormonal e metabólica integrada, conduta individualizada e acompanhamento quando indicado, com a Dra. Lanna Gomes — Médica, CRM-GO 19.507, Endocrinologista e Metabologista, RQE 9.755, mestra pela UNIFESP e 20 anos de formação médica.',
  '<strong>Vosso Instituto</strong> <span class="dot">·</span> Órion Business &amp; Health Complex <span class="dot">·</span> Setor Marista, Goiânia',
  WA_CLIM)}

{CREDBAR}

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Para quem é</p>
      <h2 class="h-lg split">O que costuma trazer nossas pacientes até&nbsp;aqui</h2>
    </div>
    <div class="reveal" data-d="1">
      <ul class="checks">
{checks([
  "Ondas de calor e suor noturno atrapalhando o sono",
  "Ganho de peso, principalmente na região abdominal, e perda de massa muscular",
  "Queda de energia e de disposição",
  "Alterações de humor, ansiedade e irritabilidade",
  "Ciclo irregular ou já em pós-menopausa",
  "Queda de libido, ressecamento e desconforto na relação",
  "Sono fragmentado",
  "Preocupação com a saúde dos ossos e com o risco cardiovascular",
])}
      </ul>
      <p class="pullquote">Não é preciso conviver com isso como se fosse inevitável. E não existe uma resposta única — existe a sua.</p>
    </div>
  </div>
</section>

<section class="section dark spot">
  <div class="wrap">
    <div class="reveal" style="max-width:52rem">
      <p class="eyebrow">O critério médico</p>
      <h2 class="h-lg split">Reposição hormonal não é para todo mundo. E é justamente isso que torna a avaliação necessária.</h2>
    </div>
    <div class="grid-2--even" style="margin-top:clamp(30px,4vw,52px)">
      <div class="reveal stack-lg">
        <p class="lede">Você provavelmente já ouviu as duas versões: que hormônio resolve tudo e que hormônio faz mal. As duas ignoram o que determina a conduta — o seu caso.</p>
        <p>A decisão depende da sua história clínica, dos seus exames, dos seus fatores de risco e dos seus sintomas. Quando há indicação, a terapia hormonal é conduzida com dose individualizada e monitoramento periódico. Quando não há, existem outras condutas para tratar os sintomas e proteger a sua saúde metabólica, muscular e óssea.</p>
      </div>
      <div class="reveal" data-d="1">
        <p class="pullquote" style="margin-top:0">A avaliação existe para definir qual dos caminhos é o seu.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Além dos sintomas</p>
      <h2 class="h-lg split">O que muda nessa fase vai além do que se sente</h2>
    </div>
    <div class="reveal stack-lg" data-d="1">
      <p class="lede">Ao longo da transição menopausal, podem ocorrer mudanças no metabolismo, na composição corporal, na massa muscular, na saúde óssea e no perfil cardiometabólico. Parte delas pode acontecer em silêncio, antes de qualquer sintoma.</p>
      <p>Por isso a avaliação não olha só para os hormônios. Ela olha para o conjunto: glicemia, tireoide, colesterol, vitaminas, composição corporal e saúde óssea.</p>
      <p class="pullquote">Tratar essa fase é cuidar de como você vai chegar aos próximos vinte anos.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="reveal" style="max-width:44rem;margin-bottom:clamp(30px,3.5vw,48px)">
      <p class="eyebrow">O acompanhamento</p>
      <h2 class="h-lg split">O cuidado nessa fase, por inteiro</h2>
    </div>
    <div class="reveal" data-d="1">
      <ul class="checks checks--2">
{checks([
  "<strong>Sintomas do climatério</strong> — calor, sono, humor, energia",
  "<strong>Saúde hormonal e metabólica</strong> — avaliação integrada, com terapia hormonal quando indicada",
  "<strong>Composição corporal e massa muscular</strong> — avaliação das mudanças que podem ocorrer ao longo dessa fase",
  "<strong>Saúde óssea</strong> — avaliação e prevenção",
  "<strong>Risco cardiometabólico</strong> — glicemia, colesterol e pressão dentro do plano",
  "<strong>Sexualidade</strong> — libido, ressecamento e desconforto, tratados como parte do cuidado",
  "<strong>Envelhecimento saudável</strong> — autonomia, força e qualidade de vida a longo prazo",
])}
      </ul>
    </div>
  </div>
</section>

{AUTORIDADE}

{steps_block("Como começa seu cuidado", PASSOS)}

{faq_block([
  ("Como vocês decidem se a terapia hormonal é indicada para mim?",
   "A partir da sua história clínica, dos seus antecedentes pessoais e familiares, do exame físico e dos seus exames — hormonais, metabólicos e de rastreio. A indicação, a via e a dose são definidas caso a caso, com monitoramento periódico ao longo do tratamento."),
  ("E os implantes hormonais?",
   "São uma das vias possíveis de terapia hormonal, indicadas apenas quando fazem sentido para o caso, com acompanhamento. Não são oferecidos como produto nem como solução padrão."),
  ("Vocês atendem por convênio?",
   "As consultas são no formato particular. Exames solicitados podem, em muitos casos, ser realizados pelo seu plano de saúde. Nossa equipe explica tudo antes do agendamento."),
  ("Em quanto tempo os sintomas melhoram?",
   "Depende do quadro e da conduta definida. Existem parâmetros clínicos acompanhados ao longo do tratamento — sintomas, exames, composição corporal — e é a partir deles que o plano é ajustado. Por isso o ritmo esperado é definido depois da avaliação."),
  ("Atende online?",
   "Sim, para casos selecionados, conforme critério médico. O atendimento presencial acontece no Vosso Instituto, no Órion Business &amp; Health Complex, no Setor Marista, em Goiânia."),
])}

{cta("Sua avaliação começa com uma conversa",
     "A decisão sobre terapia hormonal — ou sobre qualquer outra conduta — vem depois da avaliação, nunca antes dela.",
     WA_CLIM, origem="climaterio")}'''

page("climaterio-menopausa.html",
     "Climatério e Menopausa: Tratamento Médico em Goiânia | Dra. Lanna Gomes",
     "Avaliação hormonal e metabólica integrada para climatério e menopausa, com conduta individualizada e acompanhamento quando indicado. Endocrinologista em Goiânia.",
     clim, lp=True, walink=WA_CLIM)

# =====================================================================
# 3. A MÉDICA
# =====================================================================
medica = f'''<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__text">
      <p class="hero__kicker">Médica <span>·</span> CRM-GO 19.507 <span>·</span> Endocrinologista e Metabologista <span>·</span> RQE 9.755</p>
      <h1 class="h-xl split">Dra. Lanna Gomes</h1>
      <p class="lede hero__sub reveal">Com 20 anos de formação médica e uma trajetória construída sobre uma base sólida em Clínica Médica, Endocrinologia e Metabologia.</p>
      <div class="hero__actions reveal" data-d="1">
        <a class="btn" href="{WA_HOME}" target="_blank" rel="noopener">Quero agendar minha consulta {ARROW}</a>
      </div>
      <p class="hero__place reveal" data-d="2"><strong>Vosso Instituto</strong> <span class="dot">·</span> Órion Business &amp; Health Complex <span class="dot">·</span> Setor Marista, Goiânia</p>
    </div>
    <div class="portrait reveal" data-d="1">
      <div class="portrait__frame">
        <img src="assets/img/lanna-portrait.jpg" alt="Dra. Lanna Gomes" width="1080" height="1350" style="object-position:50% 16%">
      </div>
      <div class="portrait__badge">
        <b class="counter" data-count="20">20</b>
        <span>anos de formação médica</span>
      </div>
    </div>
  </div>
</section>

{CREDBAR}

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Formação</p>
      <h2 class="h-lg split">Uma base construída em Clínica Médica, Endocrinologia e Metabologia</h2>
    </div>
    <div class="reveal stack-lg" data-d="1">
      <p class="lede">Com 20 anos de formação médica, a trajetória da Dra. Lanna Gomes foi construída sobre uma base sólida em Clínica Médica, Endocrinologia e Metabologia. Após a graduação em Medicina pela Faculdade de Medicina de Marília (FAMEMA), realizou dois anos de Residência Médica em Clínica Médica e, na sequência, dois anos de Residência Médica em Endocrinologia e Metabologia. É Endocrinologista e Metabologista, com RQE 9.755, e Mestra em Ciências pelo programa de pós-graduação em Endocrinologia e Metabologia da UNIFESP.</p>
      <p>Ao longo da carreira, acumulou experiência clínica ambulatorial e hospitalar e atuou na indústria farmacêutica como gerente médica científica nas áreas de diabetes e obesidade — experiência que ampliou sua atuação em leitura crítica da evidência científica e atualização terapêutica.</p>
    </div>
  </div>
</section>

<section class="section dark spot">
  <div class="wrap">
    <div class="reveal" style="max-width:46rem;margin-bottom:clamp(34px,4vw,56px)">
      <p class="eyebrow">Titulação e formação complementar</p>
      <h2 class="h-lg split">O que sustenta a conduta clínica</h2>
    </div>
    <div class="method">
      <div class="method__item reveal">
        <span class="method__n">01</span>
        <div>
          <h3 class="h-sm">Residência Médica em Clínica Médica</h3>
          <p>Dois anos de residência em Clínica Médica — a base clínica que antecedeu a especialização.</p>
        </div>
      </div>
      <div class="method__item reveal" data-d="1">
        <span class="method__n">02</span>
        <div>
          <h3 class="h-sm">Residência Médica em Endocrinologia e Metabologia</h3>
          <p>Dois anos de residência na especialidade, com título reconhecido pela AMB/SBEM. Endocrinologista e Metabologista, RQE 9.755.</p>
        </div>
      </div>
      <div class="method__item reveal" data-d="2">
        <span class="method__n">03</span>
        <div>
          <h3 class="h-sm">Mestrado pela UNIFESP</h3>
          <p>Mestra em Ciências pelo programa de pós-graduação em Endocrinologia e Metabologia da UNIFESP.</p>
        </div>
      </div>
      <div class="method__item reveal" data-d="3">
        <span class="method__n">04</span>
        <div>
          <h3 class="h-sm">Membro titular da SBEM</h3>
          <p>Sociedade Brasileira de Endocrinologia e Metabologia.</p>
        </div>
      </div>
      <div class="method__item reveal" data-d="4">
        <span class="method__n">05</span>
        <div>
          <h3 class="h-sm">Formação complementar</h3>
          <p>Pós-graduação em Nutrologia Esportiva e formação complementar em Medicina Funcional.</p>
        </div>
      </div>
      <div class="method__item reveal" data-d="5">
        <span class="method__n">06</span>
        <div>
          <h3 class="h-sm">Membro da Sottopelle</h3>
          <p>Participação em programa de educação continuada em terapia hormonal e implantes absorvíveis.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Prática clínica</p>
      <h2 class="h-lg split">Investigar antes de tratar. Acompanhar depois de tratar.</h2>
    </div>
    <div class="reveal stack-lg" data-d="1">
      <p class="lede">Sua prática é direcionada à investigação e ao cuidado integrado da saúde hormonal e metabólica, com atenção especial a emagrecimento, composição corporal, climatério, menopausa e saúde da mulher.</p>
      <p>Medicina baseada em evidências, experiência clínica e individualização sustentando cada conduta — sem protocolos prontos.</p>
      <p class="pullquote">Atendimento no Vosso Instituto, localizado no Órion Business &amp; Health Complex, no Setor Marista, em Goiânia.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="panel spot reveal idcard">
      <p class="eyebrow eyebrow--center">Identificação profissional</p>
      <p class="idcard__name">Dra. Lanna Gomes</p>
      <p class="idcard__line">Médica <span class="dot">·</span> CRM-GO 19.507</p>
      <p class="idcard__line">Endocrinologista e Metabologista <span class="dot">·</span> RQE 9.755</p>
    </div>
  </div>
</section>

{cta("Agendar consulta com a Dra. Lanna Gomes",
     "A consulta é o ponto em que a sua história clínica, o seu exame físico e os seus exames passam a ser lidos em conjunto.",
     WA_HOME, origem="a-medica")}'''

page("a-medica.html",
     "Dra. Lanna Gomes — Endocrinologista e Metabologista | CRM-GO 19.507",
     "Endocrinologista e Metabologista em Goiânia, RQE 9.755. Residência em Clínica Médica e em Endocrinologia e Metabologia, mestrado pela UNIFESP e 20 anos de formação médica.",
     medica, current="a-medica.html")

# =====================================================================
# 4. INSTITUTO
# =====================================================================
inst = f'''<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__text">
      <p class="hero__kicker">Vosso Instituto <span>·</span> Órion Business &amp; Health Complex</p>
      <h1 class="h-xl split">A avaliação médica define o que vem depois</h1>
      <p class="lede hero__sub reveal">Condições hormonais e metabólicas mudam ao longo do tempo. Por isso, para parte dos casos, uma avaliação isolada não é suficiente: acompanhar significa revisar exames, sintomas, composição corporal e resposta ao tratamento, e ajustar a conduta quando necessário.</p>
      <div class="hero__actions reveal" data-d="1">
        <a class="btn" href="{WA_HOME}" target="_blank" rel="noopener">Quero agendar minha consulta {ARROW}</a>
      </div>
      <p class="hero__place reveal" data-d="2"><strong>Av. Portugal, 1148</strong> <span class="dot">·</span> Salas 2407/2409 <span class="dot">·</span> Setor Marista, Goiânia/GO</p>
    </div>
    <div class="portrait portrait--plain reveal" data-d="1">
      <div class="portrait__frame">
        <img src="assets/img/lanna-hero.jpg" alt="Atendimento no Vosso Instituto, Órion Business &amp; Health Complex" width="1080" height="1350">
      </div>
    </div>
  </div>
</section>

{CREDBAR}

<section class="section">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">O acompanhamento</p>
      <h2 class="h-lg split">Primeiro a avaliação. Depois, o que cada paciente precisa.</h2>
    </div>
    <div class="reveal stack-lg" data-d="1">
      <p class="lede">Para pacientes que se beneficiam de acompanhamento longitudinal, a frequência e a estrutura são definidas após a avaliação médica. O objetivo é permitir revisão clínica, acompanhamento da composição corporal e, quando indicado, de exames complementares, além de ajustes da conduta ao longo do tratamento.</p>
      <p>Quando houver indicação, o plano também pode integrar acompanhamento multidisciplinar, terapias nutricionais injetáveis, testes complementares e outros recursos terapêuticos.</p>
    </div>
  </div>
</section>

<section class="section dark spot">
  <div class="wrap grid-2">
    <div class="reveal">
      <p class="eyebrow">Medicina de precisão</p>
      <h2 class="h-lg split">Ferramentas complementares, usadas quando acrescentam informação</h2>
    </div>
    <div class="reveal stack-lg" data-d="1">
      <p class="lede">Perfil alimentar genético, microbioma intestinal, teste nutrigenético e outros exames complementares estão disponíveis e são utilizados quando há indicação clínica.</p>
      <p>O que sustenta a conduta não é o acesso aos testes, e sim a leitura médica: investigar, interpretar os resultados e decidir quando essas ferramentas realmente acrescentam informação relevante para o caso de cada paciente.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cards">
      <article class="card spot reveal">
        <span class="card__num">01</span>
        <h3 class="h-sm">A estrutura</h3>
        <p>O atendimento presencial acontece no Vosso Instituto, no Órion Business &amp; Health Complex, no Setor Marista — uma das regiões mais centrais de Goiânia, com fácil acesso e estacionamento no local. Casos selecionados também podem ser acompanhados online, conforme critério médico.</p>
      </article>
      <article class="card spot reveal" data-d="1">
        <span class="card__num">02</span>
        <h3 class="h-sm">A equipe</h3>
        <p>Uma equipe preparada acompanha cada paciente ao longo do processo, do agendamento ao acompanhamento.</p>
      </article>
      <article class="card spot reveal" data-d="2">
        <span class="card__num">03</span>
        <h3 class="h-sm">Quem é atendido</h3>
        <p>O consultório atende mulheres e homens, com foco em saúde hormonal e metabólica, emagrecimento, climatério e menopausa, diabetes, tireoide e prevenção metabólica.</p>
      </article>
    </div>
  </div>
</section>

{steps_block("Como começa seu cuidado", PASSOS)}

<section class="section section--tight">
  <div class="wrap">
    <div class="panel spot reveal" style="text-align:center">
      <p class="eyebrow eyebrow--center">Endereço</p>
      <h2 class="h-md split">Vosso Instituto · Órion Business &amp; Health Complex</h2>
      <p style="margin-top:1rem">Av. Portugal, 1148 — Salas 2407/2409<br>Setor Marista, Goiânia/GO · CEP 74150-030</p>
    </div>
  </div>
</section>

{cta("O primeiro passo é a avaliação médica",
     "É a partir dela que se define o que faz sentido para o seu caso — e se há indicação de acompanhamento ao longo do tempo.",
     WA_HOME, origem="instituto")}'''

page("instituto.html",
     "Vosso Instituto — Acompanhamento médico em Goiânia | Dra. Lanna Gomes",
     "Acompanhamento longitudinal em saúde hormonal e metabólica no Vosso Instituto, Órion Business & Health Complex, Setor Marista, Goiânia.",
     inst, current="instituto.html")

# =====================================================================
# 5. TECNOLOGIAS
# =====================================================================
tec = f'''<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__text">
      <p class="hero__kicker">Recursos do tratamento <span>·</span> Goiânia/GO</p>
      <h1 class="h-xl split">Recursos tecnológicos dentro do tratamento médico</h1>
      <p class="lede hero__sub reveal">As tecnologias disponíveis no atendimento não são oferecidas como serviço isolado. São recursos complementares, utilizados quando houver indicação, dentro de uma estratégia médica individualizada — normalmente em contextos de emagrecimento, mudança de composição corporal e pós-menopausa.</p>
      <div class="hero__actions reveal" data-d="1">
        <a class="btn" href="{WA_HOME}" target="_blank" rel="noopener">Quero agendar minha consulta {ARROW}</a>
      </div>
      <p class="hero__place reveal" data-d="2"><strong>Vosso Instituto</strong> <span class="dot">·</span> Órion Business &amp; Health Complex <span class="dot">·</span> Setor Marista, Goiânia</p>
    </div>
    <div class="portrait portrait--plain reveal" data-d="1">
      <div class="portrait__frame">
        <img src="assets/img/lanna-portrait.jpg" alt="Dra. Lanna Gomes" width="1080" height="1350" style="object-position:50% 18%">
      </div>
    </div>
  </div>
</section>

{CREDBAR}

<section class="section">
  <div class="wrap">
    <div class="cards" style="grid-template-columns:repeat(2,1fr)">
      <article class="card spot reveal">
        <span class="card__num">01</span>
        <h3 class="h-sm">Laser Ultra</h3>
        <p>Recurso complementar, utilizado quando houver indicação, dentro de uma estratégia médica individualizada — em geral em contextos de mudança de composição corporal.</p>
      </article>
      <article class="card spot reveal" data-d="1">
        <span class="card__num">02</span>
        <h3 class="h-sm">Liftera — ultrassom microfocado</h3>
        <p>Recurso complementar, utilizado quando houver indicação, dentro de uma estratégia médica individualizada — em geral em contextos de emagrecimento e de pós-menopausa.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--tight dark spot">
  <div class="wrap" style="max-width:56rem">
    <p class="eyebrow">Nota de conduta</p>
    <h2 class="h-md split">A indicação e o momento de uso de cada recurso são definidos em consulta</h2>
    <p class="lede" style="margin-top:1.2rem">Nenhum deles substitui o tratamento clínico.</p>
  </div>
</section>

{cta("O primeiro passo é a avaliação médica",
     "Os recursos disponíveis entram depois, quando há indicação clínica dentro de uma estratégia individualizada.",
     WA_HOME, origem="tecnologias")}'''

page("tecnologias.html",
     "Tecnologias integradas ao tratamento médico | Dra. Lanna Gomes",
     "Laser Ultra e Liftera como recursos complementares dentro do plano médico, quando há indicação clínica. Goiânia/GO.",
     tec, current="instituto.html")

print("\nTodas as páginas geradas.")
