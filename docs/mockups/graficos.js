// Gráficas SVG estáticas para los mockups (sin dependencias).
// En la aplicación real se reemplazan por Chart.js / componentes React con el mismo diseño.

(function () {
  const RAMPA = ["#cce3fd", "#b6d5f8", "#9dc8f7", "#84b9f3", "#6aabf1", "#519ced", "#338ced",
    "#257de0", "#2370cd", "#1b64be", "#1757ac", "#0f4a96", "#0e3d7e"];
  const TINTA = "#191919", TINTA2 = "#5c6670", REJILLA = "#e7e7e7", EJE = "#c2c2c2";

  const fmt = (v, d = 2) => Number(v).toLocaleString("es-CO", { minimumFractionDigits: d, maximumFractionDigits: d });
  const sup = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
  const potencia = (e) => "10" + String(e).split("").map((c) => sup[c]).join("");

  function colorRampa(t) {
    const i = Math.max(0, Math.min(RAMPA.length - 1, Math.round(t * (RAMPA.length - 1))));
    return RAMPA[i];
  }

  // Gráfica de líneas. y logarítmica opcional. Un solo eje y.
  function lineas(o) {
    const W = o.ancho, H = o.alto, m = { l: 64, r: o.margenDer ?? 24, t: 16, b: 44 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const [x0, x1] = o.dominioX, [y0, y1] = o.dominioY;
    const fy = o.logY ? (v) => Math.log10(Math.max(v, 1e-300)) : (v) => v;
    const X = (x) => m.l + ((x - x0) / (x1 - x0)) * iw;
    const Y = (y) => m.t + ih - ((fy(y) - fy(y0)) / (fy(y1) - fy(y0))) * ih;
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.titulo || ""}">`;

    // rejilla y ticks Y
    for (const t of o.ticksY) {
      const y = Y(t);
      s += `<line x1="${m.l}" x2="${W - m.r}" y1="${y}" y2="${y}" stroke="${REJILLA}"/>`;
      const txt = o.logY ? potencia(Math.round(Math.log10(t))) : fmt(t, 0);
      s += `<text x="${m.l - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="${TINTA2}">${txt}</text>`;
    }
    // eje X
    s += `<line x1="${m.l}" x2="${W - m.r}" y1="${m.t + ih}" y2="${m.t + ih}" stroke="${EJE}"/>`;
    for (const t of o.ticksX) {
      const x = X(t);
      s += `<text x="${x}" y="${m.t + ih + 18}" text-anchor="middle" font-size="11" fill="${TINTA2}">${o.fmtX ? o.fmtX(t) : t}</text>`;
    }
    s += `<text x="${m.l + iw / 2}" y="${H - 4}" text-anchor="middle" font-size="12" fill="${TINTA2}">${o.tituloX}</text>`;
    s += `<text transform="translate(14 ${m.t + ih / 2}) rotate(-90)" text-anchor="middle" font-size="12" fill="${TINTA2}">${o.tituloY}</text>`;

    // líneas de referencia (tolerancia, óptimo)
    for (const r of o.referencias || []) {
      if (r.y !== undefined) {
        const y = Y(r.y);
        s += `<line x1="${m.l}" x2="${W - m.r}" y1="${y}" y2="${y}" stroke="${TINTA2}" stroke-dasharray="4 4"/>`;
        const xt = r.xTexto !== undefined ? X(r.xTexto) : W - m.r - 4;
        s += `<text x="${xt}" y="${r.debajo ? y + 15 : y - 6}" text-anchor="${r.xTexto !== undefined ? "start" : "end"}" font-size="11" fill="${TINTA2}">${r.texto}</text>`;
      } else {
        const x = X(r.x);
        s += `<line x1="${x}" x2="${x}" y1="${m.t}" y2="${m.t + ih}" stroke="${TINTA2}" stroke-dasharray="4 4"/>`;
        s += `<text x="${x + 6}" y="${m.t + 12}" font-size="11" fill="${TINTA2}">${r.texto}</text>`;
      }
    }

    // series
    for (const se of o.series) {
      const pts = se.puntos.map(([x, y]) => `${X(x).toFixed(1)},${Y(y).toFixed(1)}`).join(" ");
      s += `<polyline points="${pts}" fill="none" stroke="${se.color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
      for (const [x, y] of se.marcadores || []) {
        s += `<circle cx="${X(x)}" cy="${Y(y)}" r="4.5" fill="${se.color}" stroke="#fff" stroke-width="2"/>`;
      }
      if (se.etiqueta) {
        const [x, y] = se.etiqueta.en;
        s += `<text x="${X(x) + (se.etiqueta.dx || 8)}" y="${Y(y) + (se.etiqueta.dy || 4)}" text-anchor="${se.etiqueta.ancla || "start"}" font-size="12" font-weight="600" fill="${TINTA}">${se.etiqueta.texto}</text>`;
      }
    }

    // tooltip de ejemplo (estado "hover" del boceto)
    if (o.tooltip) {
      const tx = X(o.tooltip.x);
      s += `<line x1="${tx}" x2="${tx}" y1="${m.t}" y2="${m.t + ih}" stroke="${TINTA2}" stroke-width="1"/>`;
      const filas = o.tooltip.filas, bw = 178, bh = 26 + filas.length * 19;
      const bx = Math.min(tx + 12, W - m.r - bw), by = m.t + 8;
      s += `<g><rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="8" fill="#fff" stroke="${EJE}"/>`;
      s += `<text x="${bx + 12}" y="${by + 18}" font-size="12" font-weight="700" fill="${TINTA}">${o.tooltip.titulo}</text>`;
      filas.forEach((f, i) => {
        const yy = by + 38 + i * 19;
        if (f.y !== undefined) s += `<circle cx="${tx}" cy="${Y(f.y)}" r="4.5" fill="${f.color}" stroke="#fff" stroke-width="2"/>`;
        s += `<rect x="${bx + 12}" y="${yy - 9}" width="10" height="10" rx="2" fill="${f.color}"/>`;
        s += `<text x="${bx + 28}" y="${yy}" font-size="12" fill="${TINTA2}">${f.nombre}</text>`;
        s += `<text x="${bx + bw - 12}" y="${yy}" text-anchor="end" font-size="12" fill="${TINTA}" font-weight="600">${f.valor}</text>`;
      });
      s += `</g>`;
    }
    return s + `</svg>`;
  }

  // Mapa de calor de potenciales (rampa secuencial azul). zonas opcional para contornos.
  function mapaCalor(grilla, o) {
    const n = grilla.length, c = o.celda, gap = 2, W = n * c, pad = 2;
    const plano = grilla.flat(), min = Math.min(...plano), max = Math.max(...plano);
    let s = `<svg width="${W + pad * 2}" height="${W + pad * 2}" viewBox="0 0 ${W + pad * 2} ${W + pad * 2}" role="img" aria-label="${o.titulo || "Mapa de calor"}">`;
    grilla.forEach((fila, f) => fila.forEach((v, k) => {
      const t = (v - min) / (max - min || 1);
      s += `<rect x="${pad + k * c}" y="${pad + f * c}" width="${c - gap}" height="${c - gap}" rx="2" fill="${colorRampa(t)}"/>`;
    }));
    if (o.falla) {
      const [f, k] = o.falla;
      s += `<rect x="${pad + k * c - 1}" y="${pad + f * c - 1}" width="${c}" height="${c}" rx="3" fill="none" stroke="#191919" stroke-width="2"/>`;
      s += `<text x="${pad + k * c + (c - gap) / 2}" y="${pad + f * c + (c - gap) / 2 + 5}" text-anchor="middle" font-size="${Math.max(10, c * 0.6)}" fill="#fff">⚡</text>`;
    }
    if (o.hover) {
      const [f, k] = o.hover;
      s += `<rect x="${pad + k * c - 1}" y="${pad + f * c - 1}" width="${c}" height="${c}" rx="3" fill="none" stroke="#fff" stroke-width="2"/>`;
      s += `<rect x="${pad + k * c - 3}" y="${pad + f * c - 3}" width="${c + 4}" height="${c + 4}" rx="4" fill="none" stroke="#191919" stroke-width="1.5"/>`;
    }
    return { svg: s + `</svg>`, min, max };
  }

  // Mapa de zonas de riesgo: 0 = verde, 1 = amarilla, 2 = roja. Siempre con icono, nunca solo color.
  function mapaZonas(zonas, o) {
    const n = zonas.length, c = o.celda, gap = 2, W = n * c, pad = 2;
    const col = ["#c8eccd", "#fbb315", "#dc3c3d"], ico = ["", "!", "✕"], tinta = ["", "#0b0b0b", "#fff"];
    let s = `<svg width="${W + pad * 2}" height="${W + pad * 2}" viewBox="0 0 ${W + pad * 2} ${W + pad * 2}" role="img" aria-label="${o.titulo || "Zonas de riesgo"}">`;
    zonas.forEach((fila, f) => fila.forEach((z, k) => {
      s += `<rect x="${pad + k * c}" y="${pad + f * c}" width="${c - gap}" height="${c - gap}" rx="2" fill="${col[z]}"/>`;
      if (z) s += `<text x="${pad + k * c + (c - gap) / 2}" y="${pad + f * c + (c - gap) / 2 + 4}" text-anchor="middle" font-size="${c * 0.5}" font-weight="700" fill="${tinta[z]}">${ico[z]}</text>`;
    }));
    if (o.falla) {
      const [f, k] = o.falla;
      s += `<rect x="${pad + k * c - 1}" y="${pad + f * c - 1}" width="${c}" height="${c}" rx="3" fill="none" stroke="#191919" stroke-width="2"/>`;
    }
    return s + `</svg>`;
  }

  // Barras verticales con signo (error relativo por nodo) y banda de tolerancia.
  function barras(o) {
    const W = o.ancho, H = o.alto, m = { l: 56, r: 16, t: 16, b: 40 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const [y0, y1] = o.dominioY;
    const Y = (v) => m.t + ih - ((v - y0) / (y1 - y0)) * ih;
    const bw = iw / o.valores.length;
    let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.titulo || ""}">`;
    s += `<rect x="${m.l}" y="${Y(o.banda)}" width="${iw}" height="${Y(-o.banda) - Y(o.banda)}" fill="#eef5ec"/>`;
    s += `<text x="${W - m.r - 4}" y="${Y(o.banda) - 6}" text-anchor="end" font-size="11" fill="${TINTA2}">banda aceptable ±${o.banda} %</text>`;
    for (const t of o.ticksY) {
      s += `<line x1="${m.l}" x2="${W - m.r}" y1="${Y(t)}" y2="${Y(t)}" stroke="${t === 0 ? EJE : REJILLA}"/>`;
      s += `<text x="${m.l - 8}" y="${Y(t) + 4}" text-anchor="end" font-size="11" fill="${TINTA2}">${t > 0 ? "+" : ""}${t} %</text>`;
    }
    o.valores.forEach((v, i) => {
      const x = m.l + i * bw + bw * 0.25, w = bw * 0.5, ya = Y(Math.max(v, 0)), yb = Y(Math.min(v, 0));
      s += `<rect x="${x}" y="${ya}" width="${w}" height="${Math.max(1, yb - ya)}" rx="3" fill="${o.color}"/>`;
      s += `<text x="${x + w / 2}" y="${m.t + ih + 18}" text-anchor="middle" font-size="11" fill="${TINTA2}">${o.etiquetas[i]}</text>`;
      if (o.rotular && o.rotular.includes(i)) s += `<text x="${x + w / 2}" y="${v >= 0 ? ya - 6 : yb + 14}" text-anchor="middle" font-size="11" font-weight="600" fill="${TINTA}">${v > 0 ? "+" : ""}${fmt(v, 1)} %</text>`;
    });
    s += `<text x="${m.l + iw / 2}" y="${H - 4}" text-anchor="middle" font-size="12" fill="${TINTA2}">${o.tituloX}</text>`;
    s += `<text transform="translate(14 ${m.t + ih / 2}) rotate(-90)" text-anchor="middle" font-size="12" fill="${TINTA2}">${o.tituloY}</text>`;
    return s + `</svg>`;
  }

  // Diagrama de la malla pequeña: nodos coloreados por potencial, enlaces, nodo de falla.
  function diagramaMalla(valores, o) {
    const n = Math.round(Math.sqrt(valores.length)), paso = o.paso, pad = 48, W = pad * 2 + paso * (n - 1);
    const min = Math.min(...valores), max = Math.max(...valores);
    let s = `<svg width="${W}" height="${W}" viewBox="0 0 ${W} ${W}" role="img" aria-label="Malla ${n}x${n}">`;
    const P = (i) => [pad + (i % n) * paso, pad + Math.floor(i / n) * paso];
    for (let i = 0; i < valores.length; i++) {
      const [x, y] = P(i);
      if (i % n < n - 1) s += `<line x1="${x}" y1="${y}" x2="${x + paso}" y2="${y}" stroke="${EJE}" stroke-width="3"/>`;
      if (i + n < valores.length) s += `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + paso}" stroke="${EJE}" stroke-width="3"/>`;
    }
    valores.forEach((v, i) => {
      const [x, y] = P(i), t = (v - min) / (max - min || 1), falla = i + 1 === o.falla;
      s += `<circle cx="${x}" cy="${y}" r="27" fill="${colorRampa(0.15 + t * 0.85)}" stroke="${falla ? "#191919" : "#fff"}" stroke-width="${falla ? 3 : 2}"/>`;
      s += `<text x="${x}" y="${y - 3}" text-anchor="middle" font-size="13" font-weight="700" fill="${t > 0.45 ? "#fff" : TINTA}">${fmt(v, 3)}</text>`;
      s += `<text x="${x}" y="${y + 13}" text-anchor="middle" font-size="10" fill="${t > 0.45 ? "#e6f0f8" : TINTA2}">nodo ${i + 1}</text>`;
      if (falla) s += `<text x="${x + 22}" y="${y - 20}" font-size="18">⚡</text>`;
    });
    return s + `</svg>`;
  }

  function leyendaRampa(min, max, unidad, ancho) {
    let s = `<svg width="${ancho}" height="38" viewBox="0 0 ${ancho} 38">`;
    const w = ancho / RAMPA.length;
    RAMPA.forEach((c, i) => { s += `<rect x="${i * w}" y="0" width="${w}" height="12" fill="${c}"/>`; });
    s += `<text x="0" y="30" font-size="11" fill="${TINTA2}">${fmt(min, 0)} ${unidad}</text>`;
    s += `<text x="${ancho}" y="30" text-anchor="end" font-size="11" fill="${TINTA2}">${fmt(max, 0)} ${unidad}</text>`;
    return s + `</svg>`;
  }

  window.G = { lineas, mapaCalor, mapaZonas, barras, diagramaMalla, leyendaRampa, colorRampa, fmt, potencia };
})();
