/* ==========================================================================
   Dra. Lanna Gomes — comportamento
   Progressive enhancement: se este arquivo não carregar, o site continua
   inteiro e legível. Nada aqui é requisito para ler o conteúdo.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canFx = "IntersectionObserver" in window && !reduced;
  if (canFx) root.classList.add("js");

  /* ---------------------------------------------------- topo e progresso */
  var bar = document.querySelector(".topbar");
  function setBarH() {
    if (bar) root.style.setProperty("--topbar-h", bar.offsetHeight + "px");
  }
  setBarH();
  window.addEventListener("resize", setBarH);

  var progress = null;
  if (bar) {
    progress = document.createElement("div");
    progress.className = "progress";
    bar.appendChild(progress);
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY;
      if (bar) bar.classList.toggle("is-stuck", y > 8);
      if (progress) {
        var max = document.body.scrollHeight - window.innerHeight;
        progress.style.setProperty("--p", max > 0 ? Math.min(y / max, 1) : 0);
      }
      ticking = false;
    });
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ------------------------------------------------------- menu mobile */
  var toggle = document.querySelector(".navtoggle");
  var links = document.querySelector(".nav__links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* --------------------------------------------------- fita de avaliações
     Duplica os cartões uma vez para o loop fechar sem salto — a animação anda
     até -50% da fita. Só duplica onde a fita de fato anda: com hover
     disponível e sem preferência por menos movimento. No toque ela vira
     rolagem nativa, e aí a cópia só repetiria conteúdo à toa. */
  var fita = document.querySelector("[data-revs] .revs__track");
  if (fita && window.matchMedia("(hover: hover)").matches && !reduced) {
    Array.prototype.slice.call(fita.children).forEach(function (li) {
      var copia = li.cloneNode(true);
      copia.setAttribute("aria-hidden", "true");
      fita.appendChild(copia);
    });
    fita.classList.add("is-looping");
  }

  /* ------------------------------------------------ formulário de contato
     Destino dos envios. Enquanto FORM_ENDPOINT estiver vazio, o envio abre o
     WhatsApp com os dados já preenchidos — nenhum contato se perde e nenhuma
     confirmação falsa é exibida. Basta colar aqui a URL do endpoint (um Apps
     Script, por exemplo) para que os dados passem a ser recebidos por lá e a
     mensagem de confirmação combinada com a médica apareça. */
  var FORM_ENDPOINT = "";
  var WA_NUMERO = "5562982102480";

  document.querySelectorAll(".leadform").forEach(function (form) {
    var msg = form.querySelector(".leadform__msg");
    var send = form.querySelector(".leadform__send");
    var rotulo = send ? send.textContent : "";

    function aviso(texto) {
      if (!msg) return;
      msg.textContent = texto;
      msg.hidden = false;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var campoNome = form.elements.nome;
      var campoZap = form.elements.whatsapp;
      var nome = (campoNome.value || "").trim();
      var zap = (campoZap.value || "").trim();
      var digitos = zap.replace(/\D/g, "");

      campoNome.setAttribute("aria-invalid", nome ? "false" : "true");
      campoZap.setAttribute("aria-invalid", digitos.length >= 10 ? "false" : "true");

      if (!nome) {
        aviso("Escreva o seu nome para continuar.");
        campoNome.focus();
        return;
      }
      if (digitos.length < 10) {
        aviso("Confira o seu WhatsApp com o DDD, por favor.");
        campoZap.focus();
        return;
      }

      var origem = form.getAttribute("data-origem") || "site";

      if (!FORM_ENDPOINT) {
        var texto = "Olá! Vim pelo site. Meu nome é " + nome + " e o meu WhatsApp é " +
                    zap + ". Gostaria de informações sobre a consulta.";
        window.open("https://wa.me/" + WA_NUMERO + "?text=" + encodeURIComponent(texto),
                    "_blank", "noopener");
        form.classList.add("is-sent");
        aviso("Abrimos o WhatsApp com os seus dados. É só enviar a mensagem para a nossa equipe.");
        return;
      }

      if (send) { send.disabled = true; send.textContent = "Enviando…"; }

      fetch(FORM_ENDPOINT, {
        method: "POST",
        mode: "no-cors",
        body: new URLSearchParams({
          nome: nome, whatsapp: zap, origem: origem, pagina: location.pathname
        })
      }).then(function () {
        form.classList.add("is-sent");
        aviso("Recebemos seus dados. Nossa equipe entrará em contato pelo WhatsApp em horário comercial.");
      }).catch(function () {
        if (send) { send.disabled = false; send.textContent = rotulo; }
        aviso("Não conseguimos enviar agora. Fale com a nossa equipe pelo WhatsApp, logo acima.");
      });
    });
  });

  if (!canFx) return;

  /* ---------------------------------------- títulos palavra a palavra */
  document.querySelectorAll(".split").forEach(function (el) {
    var parts = el.innerHTML.split(/(\s+)/);
    var out = "";
    var i = 0;
    parts.forEach(function (chunk) {
      if (!chunk.trim()) { out += chunk; return; }
      out += '<span class="w" style="--i:' + i + '">' + chunk + "</span>";
      i++;
    });
    el.innerHTML = out;
  });

  /* -------------------------------------- índice para escalonar listas */
  document.querySelectorAll(".checks, .credbar ul").forEach(function (list) {
    Array.prototype.forEach.call(list.children, function (li, i) {
      li.style.setProperty("--i", i);
    });
  });

  /* --------------------------------------------- contador que acende */
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count") || el.textContent, 10);
    if (isNaN(target)) return;
    var dur = 1100, t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = "0";
    requestAnimationFrame(step);
  }

  /* --------------------------------------------------- reveal on scroll */
  var fired = false;
  var io = new IntersectionObserver(function (entries) {
    fired = true;
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el.classList.add("is-in");

      if (el.classList.contains("portrait__badge")) {
        el.classList.add("is-lit");
        var n = el.querySelector(".counter");
        if (n) countUp(n);
      }
      var c = el.querySelector && el.querySelector(".counter:not(.done)");
      if (c && !el.classList.contains("portrait__badge")) {
        c.classList.add("done");
        countUp(c);
      }
      io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

  document
    .querySelectorAll(".reveal, .split, .checks, .credbar, .portrait__badge")
    .forEach(function (el) { io.observe(el); });

  /* Failsafe: se o observer não disparar em 1,8s (aba em segundo plano, motor
     que não pinta, extensão bloqueando), desliga o efeito e mostra tudo.
     O conteúdo nunca pode depender da animação para existir. */
  setTimeout(function () {
    if (!fired) root.classList.remove("js");
  }, 1800);

  /* ------------------------------------------- holofote seguindo o mouse */
  if (window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll(".spot").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
        el.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
      });
    });
  }
})();
