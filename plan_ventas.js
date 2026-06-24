const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, LevelFormat, PageBreak
} = require('/tmp/npm/lib/node_modules/docx');
const fs = require('fs');

// ─── COLORS ──────────────────────────────────────────────────────────────────
const DARK_BLUE  = "1E3A5F";
const MID_BLUE   = "2E75B6";
const LIGHT_BLUE = "D6E4F0";
const GOLD       = "C9A84C";
const GRAY_ROW   = "F2F7FC";
const WHITE      = "FFFFFF";
const DARK_GRAY  = "333333";
const MED_GRAY   = "555555";

// ─── BORDERS ─────────────────────────────────────────────────────────────────
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "AACBE8" };
const noBorder   = { style: BorderStyle.NONE,   size: 0, color: "FFFFFF" };
const allBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorders  = { top: noBorder,  bottom: noBorder,  left: noBorder,  right: noBorder  };

// ─── HELPERS ─────────────────────────────────────────────────────────────────
const cell = (text, opts = {}) => new TableCell({
  borders: opts.borders || allBorders,
  width:   { size: opts.width || 2340, type: WidthType.DXA },
  shading: { fill: opts.fill || WHITE, type: ShadingType.CLEAR },
  margins: { top: 100, bottom: 100, left: 140, right: 140 },
  verticalAlign: VerticalAlign.CENTER,
  children: [new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    children: [new TextRun({
      text,
      font:    "Arial",
      size:    opts.size   || 20,
      bold:    opts.bold   || false,
      color:   opts.color  || DARK_GRAY,
      italics: opts.italic || false,
    })]
  })]
});

const hcell = (text, opts = {}) => cell(text, {
  fill:    opts.fill  || DARK_BLUE,
  color:   opts.color || WHITE,
  bold:    true,
  size:    opts.size  || 20,
  align:   opts.align || AlignmentType.CENTER,
  width:   opts.width,
  borders: allBorders,
});

const colored_heading = (text, color = MID_BLUE) => new Paragraph({
  spacing: { before: 240, after: 80 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color, space: 6 } },
  children: [new TextRun({ text: text.toUpperCase(), font: "Arial", size: 28, bold: true, color })]
});

const sub_heading = (text) => new Paragraph({
  spacing: { before: 160, after: 60 },
  children: [new TextRun({ text, font: "Arial", size: 24, bold: true, color: DARK_BLUE })]
});

const p = (text, opts = {}) => new Paragraph({
  alignment: opts.align || AlignmentType.LEFT,
  spacing:   { before: opts.before || 80, after: opts.after || 100 },
  children: [new TextRun({
    text,
    font:    "Arial",
    size:    opts.size   || 22,
    bold:    opts.bold   || false,
    color:   opts.color  || DARK_GRAY,
    italics: opts.italic || false,
  })]
});

const bul = (text, ref = "bullets") => new Paragraph({
  numbering: { reference: ref, level: 0 },
  spacing: { before: 60, after: 60 },
  children: [new TextRun({ text, font: "Arial", size: 20, color: DARK_GRAY })]
});

const num = (text) => bul(text, "numbers");

const note = (text) => new Paragraph({
  spacing: { before: 60, after: 60 },
  children: [new TextRun({ text, font: "Arial", size: 18, color: "777777", italics: true })]
});

const space = (n = 1) => [...Array(n)].map(() => new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 20 })] }));

// ─── COVER ───────────────────────────────────────────────────────────────────
const coverBanner = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [9360],
  rows: [
    new TableRow({ children: [new TableCell({
      borders: noBorders,
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill: DARK_BLUE, type: ShadingType.CLEAR },
      margins: { top: 480, bottom: 320, left: 600, right: 600 },
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 80 }, children: [
          new TextRun({ text: "JURIS-GESTION-PRO", font: "Arial", size: 60, bold: true, color: WHITE })
        ]}),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, children: [
          new TextRun({ text: "Sistema Integral de Gestion Legal y Protocolo Notarial", font: "Arial", size: 26, color: "A8C8E8", italics: true })
        ]}),
      ]
    })]})  ,
    new TableRow({ children: [new TableCell({
      borders: noBorders,
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill: GOLD, type: ShadingType.CLEAR },
      margins: { top: 140, bottom: 140, left: 600, right: 600 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "PLAN ESTRATEGICO DE VENTAS  -  HONDURAS  -  2026", font: "Arial", size: 24, bold: true, color: DARK_BLUE })
      ]})]
    })]})
  ]
});

const coverMeta = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [4680, 4680],
  rows: [new TableRow({ children: [
    new TableCell({
      borders: noBorders,
      width: { size: 4680, type: WidthType.DXA },
      shading: { fill: LIGHT_BLUE, type: ShadingType.CLEAR },
      margins: { top: 200, bottom: 200, left: 300, right: 200 },
      children: [
        new Paragraph({ spacing: { before: 0, after: 60 }, children: [
          new TextRun({ text: "Elaborado por", font: "Arial", size: 18, color: "777777", italics: true })
        ]}),
        new Paragraph({ spacing: { before: 0, after: 60 }, children: [
          new TextRun({ text: "Ing. FERNANDO RAFAEL ARDON RODRIGUEZ", font: "Arial", size: 20, bold: true, color: DARK_BLUE })
        ]}),
        new Paragraph({ children: [
          new TextRun({ text: "SECCION TECNICA AMBIENTAL, FISCALIA DE MEDIO AMBIENTE", font: "Arial", size: 18, color: MED_GRAY })
        ]}),
      ]
    }),
    new TableCell({
      borders: noBorders,
      width: { size: 4680, type: WidthType.DXA },
      shading: { fill: LIGHT_BLUE, type: ShadingType.CLEAR },
      margins: { top: 200, bottom: 200, left: 200, right: 300 },
      children: [
        new Paragraph({ spacing: { before: 0, after: 60 }, children: [
          new TextRun({ text: "Fecha de elaboracion", font: "Arial", size: 18, color: "777777", italics: true })
        ]}),
        new Paragraph({ spacing: { before: 0, after: 60 }, children: [
          new TextRun({ text: "Junio 2026", font: "Arial", size: 20, bold: true, color: DARK_BLUE })
        ]}),
        new Paragraph({ children: [
          new TextRun({ text: "Tipo de cambio ref.: L26.78 / USD (BCH)", font: "Arial", size: 18, color: MED_GRAY })
        ]}),
      ]
    }),
  ]})]
});

// ─── PRICING TABLE ───────────────────────────────────────────────────────────
// ColWidths: 1440 + 2760 + 1300 + 1200 + 2660 = 9360
const pricingTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1440, 2760, 1300, 1200, 2660],
  rows: [
    new TableRow({ children: [
      hcell("PLAN",             { width: 1440 }),
      hcell("DESCRIPCION",      { width: 2760 }),
      hcell("PRECIO (L.)",      { width: 1300, align: AlignmentType.CENTER }),
      hcell("PRECIO (USD)",     { width: 1200, align: AlignmentType.CENTER }),
      hcell("PUBLICO OBJETIVO", { width: 2660 }),
    ]}),
    new TableRow({ children: [
      cell("STARTER",           { width: 1440, bold: true, color: DARK_BLUE }),
      cell("Licencia permanente 1 dispositivo. Sin modulo notarial.",               { width: 2760 }),
      cell("L2,499",            { width: 1300, align: AlignmentType.CENTER, bold: true, color: MID_BLUE }),
      cell("~$93",              { width: 1200, align: AlignmentType.CENTER, color: "888888" }),
      cell("Abogados independientes, recien graduados", { width: 2660, italic: true }),
    ]}),
    new TableRow({ children: [
      cell("PROFESSIONAL",      { width: 1440, bold: true, color: DARK_BLUE, fill: GRAY_ROW }),
      cell("1 dispositivo + modulo notarial completo + JURIS-AI.",                  { width: 2760, fill: GRAY_ROW }),
      cell("L3,999",            { width: 1300, align: AlignmentType.CENTER, bold: true, color: MID_BLUE, fill: GRAY_ROW }),
      cell("~$149",             { width: 1200, align: AlignmentType.CENTER, color: "888888", fill: GRAY_ROW }),
      cell("Notarios, fiscales, abogados litigantes",   { width: 2660, italic: true, fill: GRAY_ROW }),
    ]}),
    new TableRow({ children: [
      cell("BUFETE (3 PC)",     { width: 1440, bold: true, color: DARK_BLUE }),
      cell("3 licencias permanentes + notarial + soporte prioritario.",             { width: 2760 }),
      cell("L9,499",            { width: 1300, align: AlignmentType.CENTER, bold: true, color: MID_BLUE }),
      cell("~$355",             { width: 1200, align: AlignmentType.CENTER, color: "888888" }),
      cell("Bufetes pequenos (2-5 abogados)",           { width: 2660, italic: true }),
    ]}),
    new TableRow({ children: [
      cell("BUFETE PRO (5 PC)", { width: 1440, bold: true, color: DARK_BLUE, fill: GRAY_ROW }),
      cell("5 licencias + todas las funciones + onboarding remoto incluido.",       { width: 2760, fill: GRAY_ROW }),
      cell("L14,999",           { width: 1300, align: AlignmentType.CENTER, bold: true, color: MID_BLUE, fill: GRAY_ROW }),
      cell("~$560",             { width: 1200, align: AlignmentType.CENTER, color: "888888", fill: GRAY_ROW }),
      cell("Bufetes medianos / despachos notariales",   { width: 2660, italic: true, fill: GRAY_ROW }),
    ]}),
    new TableRow({ children: [
      cell("SOPORTE ANUAL",     { width: 1440, bold: true, color: GOLD }),
      cell("Actualizaciones de version + soporte tecnico 12 meses (add-on).",       { width: 2760 }),
      cell("L799",              { width: 1300, align: AlignmentType.CENTER, bold: true, color: GOLD }),
      cell("~$30",              { width: 1200, align: AlignmentType.CENTER, color: "888888" }),
      cell("Cualquier plan activo",                     { width: 2660, italic: true }),
    ]}),
  ]
});

// ─── SUBSCRIPTION TABLE ──────────────────────────────────────────────────────
// ColWidths: 2340 + 1800 + 1800 + 1440 + 1980 = 9360
const subscriptionTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2340, 1800, 1800, 1440, 1980],
  rows: [
    new TableRow({ children: [
      hcell("MODALIDAD",      { width: 2340, fill: GOLD, color: DARK_BLUE }),
      hcell("MENSUAL (L.)",   { width: 1800, fill: GOLD, color: DARK_BLUE }),
      hcell("ANUAL (L.)",     { width: 1800, fill: GOLD, color: DARK_BLUE }),
      hcell("AHORRO",         { width: 1440, fill: GOLD, color: DARK_BLUE }),
      hcell("USD / MES REF.", { width: 1980, fill: GOLD, color: DARK_BLUE }),
    ]}),
    new TableRow({ children: [
      cell("Individual (1 PC)",   { width: 2340, bold: true }),
      cell("L399/mes",            { width: 1800, align: AlignmentType.CENTER }),
      cell("L3,999/ano",          { width: 1800, align: AlignmentType.CENTER, bold: true, color: DARK_BLUE }),
      cell("17%",                 { width: 1440, align: AlignmentType.CENTER, color: "2E7D32" }),
      cell("~$14.90/mes",         { width: 1980, align: AlignmentType.CENTER, color: "888888" }),
    ]}),
    new TableRow({ children: [
      cell("Professional (1 PC)", { width: 2340, bold: true, fill: GRAY_ROW }),
      cell("L599/mes",            { width: 1800, align: AlignmentType.CENTER, fill: GRAY_ROW }),
      cell("L5,999/ano",          { width: 1800, align: AlignmentType.CENTER, bold: true, color: DARK_BLUE, fill: GRAY_ROW }),
      cell("17%",                 { width: 1440, align: AlignmentType.CENTER, color: "2E7D32", fill: GRAY_ROW }),
      cell("~$22.40/mes",         { width: 1980, align: AlignmentType.CENTER, color: "888888", fill: GRAY_ROW }),
    ]}),
    new TableRow({ children: [
      cell("Bufete (3 PC)",       { width: 2340, bold: true }),
      cell("L999/mes",            { width: 1800, align: AlignmentType.CENTER }),
      cell("L9,499/ano",          { width: 1800, align: AlignmentType.CENTER, bold: true, color: DARK_BLUE }),
      cell("21%",                 { width: 1440, align: AlignmentType.CENTER, color: "2E7D32" }),
      cell("~$37.30/mes",         { width: 1980, align: AlignmentType.CENTER, color: "888888" }),
    ]}),
  ]
});

// ─── CHANNELS TABLE ──────────────────────────────────────────────────────────
// ColWidths: 2000 + 4200 + 1560 + 1600 = 9360
const channelsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2000, 4200, 1560, 1600],
  rows: [
    new TableRow({ children: [
      hcell("CANAL",            { width: 2000 }),
      hcell("ACCIONES CLAVE",   { width: 4200 }),
      hcell("META MENSUAL",     { width: 1560 }),
      hcell("PRIORIDAD",        { width: 1600 }),
    ]}),
    ...([
      ["Venta directa (WhatsApp)",   "Demo remota por videollamada, envio de licencia digital por correo con instructivo de instalacion.",      "4 licencias",  "ALTA",  false],
      ["Programa de referidos",       "Descuento del 10% al referidor y 10% al nuevo cliente. Cadena automatica de confianza.",                  "3 licencias",  "ALTA",  true ],
      ["Colegio de Abogados (CASDEH)","Presentacion ante la junta directiva; convenio de tarifa corporativa para colegiados.",                   "2 licencias",  "ALTA",  false],
      ["Redes sociales (FB/IG)",      "Reels de demo funcional, testimonios reales, publicaciones con casos de uso practicos.",                   "2 licencias",  "MEDIA", true ],
      ["Fiscalias y sector publico",  "Propuesta institucional para unidades de fiscales o despachos del Ministerio Publico.",                    "1 contrato",   "MEDIA", false],
      ["Email / broadcast WhatsApp",  "Secuencia de seguimiento post-demo con prueba gratuita de 7 dias para cerrar ventas lentas.",             "2 licencias",  "MEDIA", true ],
    ].map(([canal, acc, meta, prio, alt]) => {
      const prioColor = prio === "ALTA" ? "C62828" : "E65100";
      return new TableRow({ children: [
        cell(canal, { width: 2000, fill: alt ? GRAY_ROW : WHITE, bold: true }),
        cell(acc,   { width: 4200, fill: alt ? GRAY_ROW : WHITE }),
        cell(meta,  { width: 1560, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER }),
        cell(prio,  { width: 1600, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER, bold: true, color: prioColor }),
      ]});
    }))
  ]
});

// ─── KPI TABLE ───────────────────────────────────────────────────────────────
// ColWidths: 3000 + 1440 + 1440 + 1440 + 2040 = 9360
const kpiTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [3000, 1440, 1440, 1440, 2040],
  rows: [
    new TableRow({ children: [
      hcell("INDICADOR",                 { width: 3000 }),
      hcell("MES 1",                     { width: 1440 }),
      hcell("MES 3",                     { width: 1440 }),
      hcell("MES 6",                     { width: 1440 }),
      hcell("ANO 1",                     { width: 2040 }),
    ]}),
    ...([
      ["Licencias vendidas (acumulado)",           "3",       "15",       "40",       "100",       false],
      ["Ingresos mensuales (HNL)",                  "L9,000",  "L45,000",  "L95,000",  "L150,000+", true ],
      ["Demos realizadas",                           "8",       "25",       "60",       "150",       false],
      ["Tasa de conversion (demo - venta)",          "35%",     "40%",      "45%",      "50%",       true ],
      ["Satisfaccion del cliente (NPS)",             "-",       ">7/10",    ">8/10",    ">8.5/10",   false],
      ["Clientes activos en programa de referidos",  "2",       "10",       "25",       "60",        true ],
    ].map(([ind, m1, m3, m6, m12, alt]) => new TableRow({ children: [
      cell(ind, { width: 3000, fill: alt ? GRAY_ROW : WHITE }),
      cell(m1,  { width: 1440, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER }),
      cell(m3,  { width: 1440, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER }),
      cell(m6,  { width: 1440, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER }),
      cell(m12, { width: 2040, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER, bold: true, color: DARK_BLUE }),
    ]})))
  ]
});

// ─── TIMELINE TABLE ──────────────────────────────────────────────────────────
// ColWidths: 1300 + 1800 + 4560 + 1700 = 9360
const timelineTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1300, 1800, 4560, 1700],
  rows: [
    new TableRow({ children: [
      hcell("FASE",                    { width: 1300 }),
      hcell("PERIODO",                 { width: 1800 }),
      hcell("ACCIONES PRIORITARIAS",   { width: 4560 }),
      hcell("RESULTADO",               { width: 1700 }),
    ]}),
    ...([
      ["Fase 1", "Jul-Ago 2026",  "Validacion: 5 demos con abogados de confianza; prueba gratuita 7 dias; recopilar testimonios y ajustar el producto.",   "3 primeras ventas", false],
      ["Fase 2", "Sep-Oct 2026",  "Presentacion al Colegio de Abogados; lanzar programa de referidos; publicidad en redes con casos reales.",               "15 licencias",      true ],
      ["Fase 3", "Nov-Dic 2026",  "Campana fin de ano (descuento 15%); propuesta a despachos notariales; primer convenio institucional.",                   "40 licencias",      false],
      ["Fase 4", "Ene-Jun 2027",  "Escalar canales digitales; evaluar distribuidores locales; explorar version multidispositivo o SaaS.",                   "100 licencias",     true ],
    ].map(([f, p, a, r, alt]) => new TableRow({ children: [
      cell(f, { width: 1300, fill: alt ? GRAY_ROW : WHITE, bold: true, color: DARK_BLUE }),
      cell(p, { width: 1800, fill: alt ? GRAY_ROW : WHITE }),
      cell(a, { width: 4560, fill: alt ? GRAY_ROW : WHITE }),
      cell(r, { width: 1700, fill: alt ? GRAY_ROW : WHITE, align: AlignmentType.CENTER, bold: true }),
    ]})))
  ]
});

// ─── INCOME PROJECTION TABLE ─────────────────────────────────────────────────
// ColWidths: 2340 + 2340 + 2340 + 2340 = 9360
const incomeTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2340, 2340, 2340, 2340],
  rows: [
    new TableRow({ children: [
      hcell("PERIODO",              { width: 2340 }),
      hcell("LICENCIAS VENDIDAS",   { width: 2340 }),
      hcell("INGRESO TOTAL (HNL)",  { width: 2340 }),
      hcell("INGRESO TOTAL (USD)",  { width: 2340 }),
    ]}),
    ...([
      ["Mes 1-3",   "15",  "~L48,000",  "~$1,793",  false],
      ["Mes 4-6",   "25",  "~L75,000",  "~$2,801",  true ],
      ["Mes 7-12",  "60",  "~L190,000", "~$7,096",  false],
    ].map(([p, l, h, u, alt]) => new TableRow({ children: [
      cell(p, { width: 2340, align: AlignmentType.CENTER, fill: alt ? GRAY_ROW : WHITE }),
      cell(l, { width: 2340, align: AlignmentType.CENTER, fill: alt ? GRAY_ROW : WHITE }),
      cell(h, { width: 2340, align: AlignmentType.CENTER, fill: alt ? GRAY_ROW : WHITE }),
      cell(u, { width: 2340, align: AlignmentType.CENTER, fill: alt ? GRAY_ROW : WHITE }),
    ]}))),
    new TableRow({ children: [
      cell("TOTAL ANO 1",  { width: 2340, align: AlignmentType.CENTER, fill: DARK_BLUE, color: WHITE, bold: true }),
      cell("100",          { width: 2340, align: AlignmentType.CENTER, fill: DARK_BLUE, color: WHITE, bold: true }),
      cell("~L313,000",    { width: 2340, align: AlignmentType.CENTER, fill: DARK_BLUE, color: WHITE, bold: true }),
      cell("~$11,690",     { width: 2340, align: AlignmentType.CENTER, fill: DARK_BLUE, color: WHITE, bold: true }),
    ]}),
  ]
});

// ─── DIFFERENTIATION TABLE ───────────────────────────────────────────────────
const diffTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [4680, 4680],
  rows: [
    new TableRow({ children: [
      hcell("VENTAJA COMPETITIVA",   { width: 4680 }),
      hcell("IMPACTO EN EL CLIENTE", { width: 4680 }),
    ]}),
    ...([
      ["100% Offline: datos bajo control total del usuario",                          "Garantiza secreto profesional absoluto; no depende de internet.",                false],
      ["Protocolo notarial digital con validacion de folios",                         "Elimina errores que generan sanciones de la Controloria del Notariado.",         true ],
      ["JURIS-AI integrado para redaccion de escritos legales",                       "Reduce hasta 70% el tiempo en documentos repetitivos.",                         false],
      ["Hecho en Honduras, para Honduras",                                            "Plantillas adaptadas al Codigo Procesal hondureno y terminologia local.",        true ],
      ["Pago unico sin suscripcion obligatoria",                                      "Sin compromisos mensuales; ideal para profesionales independientes.",            false],
      ["Precio hasta 10x menor que software SaaS internacional equivalente",          "El retorno de inversion se logra en las primeras horas de uso del producto.",   true ],
    ].map(([v, i, alt]) => new TableRow({ children: [
      cell(v, { width: 4680, fill: alt ? GRAY_ROW : WHITE }),
      cell(i, { width: 4680, fill: alt ? GRAY_ROW : WHITE }),
    ]})))
  ]
});

// ─── DOCUMENT ────────────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "-", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
  },
  sections: [
    // PAGE 1: COVER
    {
      properties: {
        page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
      },
      children: [
        ...space(2),
        coverBanner,
        ...space(2),
        coverMeta,
        ...space(4),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 80 }, children: [
          new TextRun({ text: "Contacto comercial", font: "Arial", size: 20, bold: true, color: DARK_BLUE })
        ]}),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 60 }, children: [
          new TextRun({ text: "WhatsApp: +504-3352-7444   |   frardonr@hotmail.com", font: "Arial", size: 20, color: MED_GRAY })
        ]}),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: "JURIS-GESTION-PRO  -  Justicia, Tecnologia y Control en sus manos.", font: "Arial", size: 20, italics: true, color: GOLD })
        ]}),
      ]
    },
    // PAGES 2+: CONTENT
    {
      properties: {
        page: { size: { width: 12240, height: 15840 }, margin: { top: 1000, right: 1000, bottom: 1000, left: 1000 } }
      },
      headers: {
        default: new Header({ children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: MID_BLUE, space: 4 } },
          children: [
            new TextRun({ text: "JURIS-GESTION-PRO  |  Plan Estrategico de Ventas 2026", font: "Arial", size: 18, bold: true, color: DARK_BLUE }),
            new TextRun({ text: "\t", font: "Arial", size: 18 }),
            new TextRun({ text: "Ing. Fernando Rafael Ardon Rodriguez", font: "Arial", size: 16, color: "888888", italics: true }),
          ],
          tabStops: [{ type: "right", position: 9160 }]
        })]}),
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: MID_BLUE, space: 4 } },
          children: [
            new TextRun({ text: "CONFIDENCIAL  |  Uso comercial exclusivo del desarrollador", font: "Arial", size: 16, color: "999999", italics: true }),
            new TextRun({ text: "\t", font: "Arial", size: 16 }),
            new TextRun({ text: "Pagina ", font: "Arial", size: 16, color: "999999" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "999999" }),
          ],
          tabStops: [{ type: "right", position: 9160 }]
        })]}),
      },
      children: [

        // 1. RESUMEN EJECUTIVO
        colored_heading("1. Resumen Ejecutivo"),
        p("JURIS-GESTION-PRO es una aplicacion de escritorio para Windows disenada especificamente para el mercado legal hondureno. Combina gestion de expedientes, protocolo notarial digital, asistente con inteligencia artificial (JURIS-AI) y seguridad de datos offline. Este plan define la estrategia de precios, los canales de venta y las metas para los primeros 12 meses de comercializacion en Honduras."),
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [2340, 2340, 2340, 2340],
          rows: [
            new TableRow({ children: [
              hcell("Tipo de cambio ref.",  { width: 2340 }),
              hcell("Mercado primario",     { width: 2340 }),
              hcell("Modelo de venta",      { width: 2340 }),
              hcell("Meta ano 1",           { width: 2340 }),
            ]}),
            new TableRow({ children: [
              cell("L26.78 / USD (BCH, jun-2026)", { width: 2340, align: AlignmentType.CENTER }),
              cell("Honduras (TGU, SPS y Departamentos)", { width: 2340, align: AlignmentType.CENTER }),
              cell("Licencia perpetua + soporte anual", { width: 2340, align: AlignmentType.CENTER }),
              cell("100 licencias / L150,000/mes", { width: 2340, align: AlignmentType.CENTER, bold: true, color: DARK_BLUE }),
            ]}),
          ]
        }),
        ...space(1),

        // 2. ANALISIS DEL MERCADO
        colored_heading("2. Analisis del Mercado Objetivo"),
        sub_heading("2.1  Tamano del mercado"),
        p("Honduras cuenta con aproximadamente 8,000 abogados colegiados activos en el Colegio de Abogados y Notarios (CASDEH) y seccionales departamentales, mas de 600 notarios habilitados y una red de fiscales del Ministerio Publico distribuidos en 18 seccionales. La mayoria opera sin software de gestion especializado, dependiendo de herramientas genericas como Excel o documentos Word.", { size: 20 }),
        ...space(1),
        sub_heading("2.2  Segmentos prioritarios"),
        bul("Abogados independientes (despacho propio): mayor volumen, decision de compra directa e inmediata."),
        bul("Notarios: necesidad critica del modulo de protocolo notarial para cumplir regulaciones de la Controloria del Notariado."),
        bul("Fiscales y defensores publicos: alto volumen de expedientes; potencial de contratos institucionales."),
        bul("Bufetes pequenos (2-5 abogados): dispuestos a pagar mas por eficiencia de equipo y trabajo colaborativo."),
        ...space(1),
        sub_heading("2.3  Contexto economico y competitivo"),
        bul("Salario mensual promedio de abogados: L17,680 a L54,660 (Computrabajo HN, 2026)."),
        bul("Tipo de cambio referencia: L26.78 por USD (Banco Central de Honduras, 23 jun-2026). El lempira ha registrado depreciacion de L0.125 en lo que va de 2026."),
        bul("Competencia internacional (LexIAGest, Clio, MyCase): $49-$99 USD/mes equivalente a L1,312-L2,651/mes. JURIS-GESTION-PRO es hasta 10x mas economico."),
        bul("No existe software legal de escritorio offline hecho en Honduras, lo que representa una ventana de mercado sin competencia directa."),
        ...space(1),

        // 3. PROPUESTA DE VALOR
        colored_heading("3. Propuesta de Valor Diferenciadora"),
        diffTable,
        ...space(1),

        // 4. ESTRATEGIA DE PRECIOS
        colored_heading("4. Estrategia de Precios"),
        sub_heading("4.1  Licencia perpetua (oferta principal recomendada)"),
        p("El modelo de pago unico es el mas adecuado para el mercado hondureno, donde la aversion a pagos recurrentes es alta. Se complementa con un add-on opcional de soporte anual para generar ingreso recurrente.", { size: 20, after: 120 }),
        pricingTable,
        note("Tipo de cambio utilizado: L26.78 / USD (BCH, 23 de junio de 2026). Los precios en USD son referenciales para clientes de la diaspora o con facturacion en dolares."),
        ...space(1),
        sub_heading("4.2  Suscripcion mensual/anual (oferta complementaria)"),
        p("Para clientes que prefieren pagos escalonados o deseen evaluar antes de comprar, se ofrece una modalidad de suscripcion con descuento del 17-21% al optar por el plan anual.", { size: 20, after: 120 }),
        subscriptionTable,
        note("El plan anual equivale a pagar 10 meses y obtener 2 meses gratis. Recomendado como segunda opcion para retener clientes que no cierren con la licencia perpetua."),
        ...space(1),
        sub_heading("4.3  Justificacion del precio"),
        bul("Un abogado con salario minimo (L17,680/mes) destina solo el 14.1% de su ingreso mensual para la licencia STARTER, recuperando la inversion en las primeras horas de trabajo ahorrado."),
        bul("El plan PROFESSIONAL (L3,999) equivale a 2 dias de honorarios de un abogado promedio, validando un retorno de inversion inmediato y concreto."),
        bul("Frente a la competencia internacional que cobra entre L1,312-L2,651 al mes, la licencia perpetua se paga sola en los primeros 2-3 meses de uso versus cualquier alternativa SaaS."),
        ...space(1),

        // 5. CANALES DE VENTA
        colored_heading("5. Canales de Venta y Distribucion"),
        channelsTable,
        ...space(1),
        sub_heading("5.1  Proceso de venta estandar"),
        num("Contacto inicial via WhatsApp, referido o red social."),
        num("Demo remota de 20-30 minutos (videollamada con pantalla compartida)."),
        num("Prueba gratuita de 7 dias (version con licencia temporal de acceso completo)."),
        num("Cierre: pago via transferencia bancaria o pago movil (Tengo, Tigo Money) y envio de licencia digital por correo."),
        num("Seguimiento a 30 dias y solicitud de testimonio o referido activo."),
        ...space(1),

        // 6. PLAN DE IMPLEMENTACION
        colored_heading("6. Plan de Implementacion por Fases"),
        timelineTable,
        ...space(1),

        // 7. METAS Y KPIs
        colored_heading("7. Metas y KPIs"),
        kpiTable,
        ...space(1),
        sub_heading("7.1  Proyeccion de ingresos (escenario moderado)"),
        incomeTable,
        ...space(1),

        // 8. RECOMENDACIONES
        colored_heading("8. Recomendaciones Finales"),
        bul("Lanzar con el plan PROFESSIONAL como oferta principal: el modulo notarial diferencia el producto de cualquier alternativa generica disponible en Honduras."),
        bul("Implementar la prueba de 7 dias como estandar: el producto se vende solo una vez que el usuario lo experimenta en su flujo de trabajo real."),
        bul("Priorizar al Colegio de Abogados (CASDEH) como primer canal institucional: un convenio puede significar acceso a mas de 8,000 potenciales clientes."),
        bul("Aceptar pagos por Tigo Money, Tengo y transferencia bancaria (BAC/Atlantida) para eliminar la friccion en el cobro."),
        bul("Publicar el video de demo de 3 minutos (guion tecnico ya disponible en el proyecto) en YouTube y Facebook para generar trafico organico sin costo publicitario."),
        bul("Revisar precios semestralmente ajustando segun el tipo de cambio del BCH para mantener la competitividad en terminos de dolares y preservar el margen real."),
        ...space(2),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 240, after: 60 },
          border: { top: { style: BorderStyle.SINGLE, size: 6, color: GOLD, space: 8 } },
          children: [
            new TextRun({ text: "Ing. FERNANDO RAFAEL ARDON RODRIGUEZ", font: "Arial", size: 20, bold: true, color: DARK_BLUE })
          ]
        }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 60 }, children: [
          new TextRun({ text: "SECCION TECNICA AMBIENTAL, FISCALIA DE MEDIO AMBIENTE", font: "Arial", size: 18, color: MED_GRAY })
        ]}),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: "WhatsApp: +504-3352-7444  |  frardonr@hotmail.com  |  JURIS-GESTION-PRO", font: "Arial", size: 18, italics: true, color: GOLD })
        ]}),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/sessions/affectionate-vigilant-babbage/mnt/JURIS-GESTION-PRO/PLAN_VENTAS_JURIS-GESTION-PRO_2026.docx", buf);
  console.log("OK");
}).catch(e => { console.error(e.message); process.exit(1);});
 });
