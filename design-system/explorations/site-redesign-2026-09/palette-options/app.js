const SURFACES = {
  home: {
    label: "Homepage",
    path: "../artboards/B4-homepage.html",
    route: "/",
    compareHeight: 670,
    focusHeight: 920,
  },
  canvas: {
    label: "Canvas",
    path: "../artboards/B1-canvas-page.html",
    route: "/canvas/direct-booking-recovery",
    compareHeight: 760,
    focusHeight: 980,
  },
  pdf: {
    label: "PDF",
    path: "../artboards/B9-pdf.html",
    route: "/canvas/direct-booking-recovery.pdf",
    compareHeight: 690,
    focusHeight: 920,
  },
};

const PALETTES = {
  control: {
    index: "00 · CONTROL",
    name: "Rev C",
    position: "Premium blueprint",
    question: "Does continuity outweigh the risk that OE looks like a polished answer before the category is proven?",
    colors: {
      paper: "#F5F0E6",
      field: "#14263E",
      core: "#C4A45F",
      perimeter: "#1F3A5F",
      risk: "#9B3E2E",
    },
    roles: [
      ["Identity", "Premium editorial and working schematic"],
      ["Accent", "Ledger value and counter-system"],
      ["Continuity", "Current production palette"],
      ["Primary risk", "Finance and finished-authority cues"],
    ],
    tokens: null,
  },
  accountable: {
    index: "01 · RECOMMENDED",
    name: "Accountable Core",
    position: "Human-scale institution",
    question: "Does this feel like real ownership under inspection, rather than a polished theory?",
    colors: {
      paper: "#F1F2ED",
      field: "#204440",
      core: "#B5482F",
      coreOnDark: "#FB8B69",
      perimeter: "#586D74",
      risk: "#90394A",
    },
    roles: [
      ["Core oxide", "Owner, decision rights, active test"],
      ["Perimeter steel", "Rented capability and dependency"],
      ["Deep mineral", "Evidence, method, institutional ground"],
      ["Primary risk", "Ecological or industrial association"],
    ],
    tokens: {
      "--ink": "#19201F",
      "--paper": "#F1F2ED",
      "--drafting-blue": "#586D74",
      "--ledger-gold": "#B5482F",
      "--sage": "#7FA48E",
      "--ink-900": "#19201F",
      "--ink-700": "#303B39",
      "--ink-500": "#566461",
      "--ink-400": "#63706C",
      "--ink-300": "#A9B0AD",
      "--paper-0": "#F8F9F5",
      "--paper-100": "#F1F2ED",
      "--paper-200": "#E7E9E4",
      "--paper-300": "#DCE0DA",
      "--rule": "#CDD2CC",
      "--rule-strong": "#AEB7B1",
      "--blue-900": "#33464C",
      "--blue-700": "#586D74",
      "--blue-500": "#71868D",
      "--blue-tint": "#DEE5E5",
      "--gold-700": "#87341F",
      "--gold-500": "#B5482F",
      "--gold-bright": "#FB8B69",
      "--gold-tint": "#F3DDD6",
      "--sage-700": "#3F6855",
      "--sage-500": "#7FA48E",
      "--negative": "#90394A",
      "--surface-page": "var(--paper-100)",
      "--surface-card": "var(--paper-0)",
      "--surface-sunken": "var(--paper-200)",
      "--surface-ink": "var(--ink-900)",
      "--surface-schematic": "#204440",
      "--text-strong": "var(--ink-900)",
      "--text-body": "var(--ink-700)",
      "--text-muted": "var(--ink-500)",
      "--text-faint": "var(--ink-400)",
      "--text-disabled": "var(--ink-300)",
      "--text-on-ink": "#F1F2ED",
      "--text-on-ink-muted": "rgba(241,242,237,.72)",
      "--text-on-ink-faint": "rgba(241,242,237,.62)",
      "--schem-grid": "rgba(241,242,237,.06)",
      "--schem-node-border": "rgba(241,242,237,.42)",
      "--schem-node-bg": "rgba(88,109,116,.32)",
      "--schem-wire": "rgba(241,242,237,.42)",
      "--status-live": "#A4C6B2",
      "--accent": "var(--ledger-gold)",
      "--accent-hover": "#9A3923",
      "--accent-press": "#772B1A",
      "--link": "var(--drafting-blue)",
      "--data-highlight": "var(--ledger-gold)",
      "--data-highlight-ink": "var(--gold-bright)",
      "--delta-positive": "var(--sage-700)",
      "--delta-negative": "var(--negative)",
      "--border": "var(--rule)",
      "--border-strong": "var(--rule-strong)",
      "--border-ink": "rgba(241,242,237,.18)",
      "--focus-ring": "#CC6F32",
      "--blue-950-candidate": "#14312E",
    },
  },
  datum: {
    index: "02 · COOLER",
    name: "Datum",
    position: "Measurement-first field instrument",
    question: "Does this increase trust and precision without turning the publication into a sterile lab or think tank?",
    colors: {
      paper: "#F3F5F2",
      field: "#232B31",
      core: "#B44A1A",
      coreOnDark: "#FF9B5B",
      perimeter: "#0D6587",
      risk: "#963C3A",
    },
    roles: [
      ["Survey orange", "Active test and changed assumption"],
      ["Instrument blue", "Structure and measured material"],
      ["Basalt", "Research field and video ground"],
      ["Primary risk", "Sterile technical authority"],
    ],
    tokens: {
      "--ink": "#171C20",
      "--paper": "#F3F5F2",
      "--drafting-blue": "#0D6587",
      "--ledger-gold": "#B44A1A",
      "--sage": "#6F9B86",
      "--ink-900": "#171C20",
      "--ink-700": "#343D43",
      "--ink-500": "#59646A",
      "--ink-400": "#667177",
      "--ink-300": "#ABB2B5",
      "--paper-0": "#FAFBF8",
      "--paper-100": "#F3F5F2",
      "--paper-200": "#E9ECE9",
      "--paper-300": "#DCE2DF",
      "--rule": "#CBD2CF",
      "--rule-strong": "#AAB5B0",
      "--blue-900": "#07445E",
      "--blue-700": "#0D6587",
      "--blue-500": "#277C9B",
      "--blue-tint": "#DDEAF0",
      "--gold-700": "#92380F",
      "--gold-500": "#B44A1A",
      "--gold-bright": "#FF9B5B",
      "--gold-tint": "#F5DFD1",
      "--sage-700": "#356950",
      "--sage-500": "#6F9B86",
      "--negative": "#963C3A",
      "--surface-page": "var(--paper-100)",
      "--surface-card": "var(--paper-0)",
      "--surface-sunken": "var(--paper-200)",
      "--surface-ink": "var(--ink-900)",
      "--surface-schematic": "#232B31",
      "--text-strong": "var(--ink-900)",
      "--text-body": "var(--ink-700)",
      "--text-muted": "var(--ink-500)",
      "--text-faint": "var(--ink-400)",
      "--text-disabled": "var(--ink-300)",
      "--text-on-ink": "#F3F5F2",
      "--text-on-ink-muted": "rgba(243,245,242,.72)",
      "--text-on-ink-faint": "rgba(243,245,242,.60)",
      "--schem-grid": "rgba(243,245,242,.055)",
      "--schem-node-border": "rgba(243,245,242,.40)",
      "--schem-node-bg": "rgba(13,101,135,.28)",
      "--schem-wire": "rgba(243,245,242,.40)",
      "--status-live": "#85B79F",
      "--accent": "var(--drafting-blue)",
      "--accent-hover": "#085775",
      "--accent-press": "#07445E",
      "--link": "var(--drafting-blue)",
      "--data-highlight": "var(--ledger-gold)",
      "--data-highlight-ink": "var(--gold-bright)",
      "--delta-positive": "var(--sage-700)",
      "--delta-negative": "var(--negative)",
      "--border": "var(--rule)",
      "--border-strong": "var(--rule-strong)",
      "--border-ink": "rgba(243,245,242,.18)",
      "--focus-ring": "#107E8C",
      "--blue-950-candidate": "#171C20",
    },
  },
  civic: {
    index: "03 · EDITORIAL",
    name: "Civic Register",
    position: "Public-interest economics",
    question: "Does this feel independently authoritative without losing the operator's physical, practical energy?",
    colors: {
      paper: "#F4F3EE",
      field: "#292F61",
      core: "#A93C47",
      coreOnDark: "#FF8A82",
      perimeter: "#275A86",
      risk: "#94313C",
    },
    roles: [
      ["Signal red", "Correction, decision, public consequence"],
      ["Mineral violet", "External systems and adjacent evidence"],
      ["Deep indigo", "Institutional analysis and economics"],
      ["Primary risk", "Policy desk rather than operator desk"],
    ],
    tokens: {
      "--ink": "#1C1E29",
      "--paper": "#F4F3EE",
      "--drafting-blue": "#275A86",
      "--ledger-gold": "#A93C47",
      "--sage": "#789888",
      "--ink-900": "#1C1E29",
      "--ink-700": "#383A49",
      "--ink-500": "#5D6070",
      "--ink-400": "#6A6D7C",
      "--ink-300": "#ADB0B8",
      "--paper-0": "#FAF9F6",
      "--paper-100": "#F4F3EE",
      "--paper-200": "#E9E8E2",
      "--paper-300": "#DEDDD6",
      "--rule": "#CECDC4",
      "--rule-strong": "#AEAFA8",
      "--blue-900": "#183B5B",
      "--blue-700": "#275A86",
      "--blue-500": "#4779A3",
      "--blue-tint": "#E1E8F0",
      "--gold-700": "#87303A",
      "--gold-500": "#A93C47",
      "--gold-bright": "#FF8A82",
      "--gold-tint": "#F3DEE0",
      "--sage-700": "#3C6958",
      "--sage-500": "#789888",
      "--negative": "#94313C",
      "--surface-page": "var(--paper-100)",
      "--surface-card": "var(--paper-0)",
      "--surface-sunken": "var(--paper-200)",
      "--surface-ink": "var(--ink-900)",
      "--surface-schematic": "#292F61",
      "--text-strong": "var(--ink-900)",
      "--text-body": "var(--ink-700)",
      "--text-muted": "var(--ink-500)",
      "--text-faint": "var(--ink-400)",
      "--text-disabled": "var(--ink-300)",
      "--text-on-ink": "#F4F3EE",
      "--text-on-ink-muted": "rgba(244,243,238,.72)",
      "--text-on-ink-faint": "rgba(244,243,238,.60)",
      "--schem-grid": "rgba(244,243,238,.06)",
      "--schem-node-border": "rgba(244,243,238,.40)",
      "--schem-node-bg": "rgba(39,90,134,.30)",
      "--schem-wire": "rgba(244,243,238,.40)",
      "--status-live": "#9FC1DC",
      "--accent": "var(--drafting-blue)",
      "--accent-hover": "#204D75",
      "--accent-press": "#183B5B",
      "--link": "var(--drafting-blue)",
      "--data-highlight": "var(--ledger-gold)",
      "--data-highlight-ink": "var(--gold-bright)",
      "--delta-positive": "var(--sage-700)",
      "--delta-negative": "var(--negative)",
      "--border": "var(--rule)",
      "--border-strong": "var(--rule-strong)",
      "--border-ink": "rgba(244,243,238,.18)",
      "--focus-ring": "#C95B64",
      "--blue-950-candidate": "#202448",
    },
  },
};

PALETTES.boundaryLedger = {
  ...PALETTES.accountable,
  index: "A · LOCKED DIRECTION",
  name: "Boundary Ledger",
  position: "A warm record of ownership",
  question: "Does this make owned versus rented capability legible without turning the thesis into an abstract diagram?",
  colors: {
    ...PALETTES.accountable.colors,
    paper: "#F5F0E6",
  },
  roles: [
    ["Warm ledger", "The human context and working record"],
    ["Deep mineral", "Owned core and institutional ground"],
    ["Core oxide", "Commitments, exceptions, and active decisions"],
    ["Perimeter steel", "Rented capability and dependency"],
  ],
  polishCss: `
    /* The proof panel stays accountable; the episode model remains an open working sheet. */
    .panel,
    .news-band {
      background-image: none !important;
    }

    .hero {
      grid-template-columns: 120px minmax(0, 1.08fr) minmax(340px, .82fr) !important;
      column-gap: clamp(24px, 3vw, 44px) !important;
      row-gap: 0 !important;
    }

    .hero > .panel {
      position: relative;
      z-index: 2;
      width: 100%;
      align-self: end;
      transform: translateY(16px);
      border: 1px solid rgba(245, 240, 230, .18) !important;
      background-color: var(--surface-schematic) !important;
      box-shadow: 0 18px 44px -24px rgba(23, 53, 48, .50) !important;
    }

    .boundary-episode-figure {
      grid-column: 2 / -1;
      position: relative;
      z-index: 1;
      min-width: 0;
      margin: 0;
      padding: 0;
      overflow: hidden;
      border: 1px solid var(--rule-strong);
      background: var(--paper-100);
    }

    .boundary-episode-sketch {
      display: block;
      width: 100%;
      height: auto;
      aspect-ratio: 3 / 2;
      object-fit: contain;
      background: var(--paper-100);
    }

    .panel .ghost {
      display: none !important;
    }

    .panel .doc-stack {
      margin: var(--space-3) 0 var(--space-4) !important;
    }

    .hero > .panel .doc {
      padding: 0 0 0 var(--space-3) !important;
      border: 0 !important;
      border-left: 2px solid var(--drafting-blue) !important;
      background: transparent !important;
      box-shadow: none !important;
    }

    .panel .panel-head,
    .panel .spec-row {
      border-color: rgba(245, 240, 230, .22) !important;
    }

    .panel .dot.pulse {
      animation: none !important;
    }

    .hero > .panel .spec-row:nth-child(3),
    .hero > .panel .panel-foot {
      display: none !important;
    }

    @media (max-width: 900px) {
      .hero {
        grid-template-columns: 1fr !important;
        row-gap: 0 !important;
      }

      .hero > .panel {
        grid-column: 1;
        margin-top: var(--space-6);
        transform: translateY(16px);
      }

      .boundary-episode-figure {
        grid-column: 1;
        margin-right: calc(-1 * var(--space-5));
        margin-left: calc(-1 * var(--space-5));
      }
    }
  `,
  tokens: {
    ...PALETTES.accountable.tokens,
    "--paper": "#F5F0E6",
    "--paper-0": "#FBF8F1",
    "--paper-100": "#F5F0E6",
    "--paper-200": "#EDE7D8",
    "--paper-300": "#E2DAC7",
    "--rule": "#D8CFB9",
    "--rule-strong": "#C4B99E",
    "--text-on-ink": "#F5F0E6",
    "--text-on-ink-muted": "rgba(245,240,230,.72)",
    "--text-on-ink-faint": "rgba(245,240,230,.62)",
    "--schem-grid": "rgba(245,240,230,.06)",
    "--schem-node-border": "rgba(245,240,230,.42)",
    "--schem-wire": "rgba(245,240,230,.42)",
    "--border-ink": "rgba(245,240,230,.18)",
  },
};

PALETTES.signalLedger = {
  ...PALETTES.datum,
  index: "B · SIGNAL",
  name: "Signal Ledger",
  position: "A live research instrument",
  question: "Does the added energy make the evidence feel alive without making it feel gamified?",
  colors: {
    paper: "#F5F0E6",
    field: "#14263E",
    core: "#BC472A",
    coreOnDark: "#FF835D",
    perimeter: "#0D7079",
    risk: "#9B3E2E",
  },
  roles: [
    ["Rev C paper + navy", "Institutional continuity and record"],
    ["Signal teal", "Evidence, systems, and model structure"],
    ["Decision orange", "Changed assumptions, action, and movement"],
    ["Primary risk", "Teal and orange compete or feel software-led"],
  ],
  tokens: {
    ...PALETTES.datum.tokens,
    "--ink": "#1A1A1A",
    "--paper": "#F5F0E6",
    "--drafting-blue": "#0D7079",
    "--ledger-gold": "#BC472A",
    "--sage": "#7B9E87",
    "--ink-900": "#1A1A1A",
    "--ink-700": "#3C3A36",
    "--ink-500": "#6B675E",
    "--ink-400": "#8A857A",
    "--ink-300": "#B4AE9F",
    "--paper-0": "#FBF8F1",
    "--paper-100": "#F5F0E6",
    "--paper-200": "#EDE7D8",
    "--paper-300": "#E2DAC7",
    "--rule": "#D8CFB9",
    "--rule-strong": "#C4B99E",
    "--blue-900": "#084C54",
    "--blue-700": "#0D7079",
    "--blue-500": "#2A8790",
    "--blue-tint": "#DAEAE8",
    "--gold-700": "#91331F",
    "--gold-500": "#BC472A",
    "--gold-bright": "#FF835D",
    "--gold-tint": "#F2DDD3",
    "--sage-700": "#5E7F6A",
    "--sage-500": "#7B9E87",
    "--negative": "#9B3E2E",
    "--surface-page": "var(--paper-100)",
    "--surface-card": "var(--paper-0)",
    "--surface-sunken": "var(--paper-200)",
    "--surface-ink": "var(--ink-900)",
    "--surface-schematic": "#14263E",
    "--text-strong": "var(--ink-900)",
    "--text-body": "var(--ink-700)",
    "--text-muted": "var(--ink-500)",
    "--text-faint": "var(--ink-400)",
    "--text-disabled": "var(--ink-300)",
    "--text-on-ink": "#F5F0E6",
    "--text-on-ink-muted": "rgba(245,240,230,.68)",
    "--text-on-ink-faint": "rgba(245,240,230,.50)",
    "--schem-grid": "rgba(245,240,230,.055)",
    "--schem-node-border": "rgba(245,240,230,.34)",
    "--schem-node-bg": "rgba(13,112,121,.38)",
    "--schem-wire": "rgba(245,240,230,.34)",
    "--status-live": "#76B89C",
    "--accent": "var(--drafting-blue)",
    "--accent-hover": "#0A6068",
    "--accent-press": "#084C54",
    "--link": "var(--drafting-blue)",
    "--data-highlight": "var(--ledger-gold)",
    "--data-highlight-ink": "var(--gold-bright)",
    "--delta-positive": "var(--sage-700)",
    "--delta-negative": "var(--negative)",
    "--border": "var(--rule)",
    "--border-strong": "var(--rule-strong)",
    "--border-ink": "rgba(245,240,230,.16)",
    "--focus-ring": "#0D7079",
    "--blue-950-candidate": "#14263E",
  },
};

const paletteOrder = ["boundaryLedger", "signalLedger"];

const DEFAULT_STATE = {
  surface: "home",
  view: "compare",
  palette: "boundaryLedger",
  device: "desktop",
};

const state = readState();
const compareGrid = document.querySelector(".compare-grid");
const focusStage = document.querySelector(".focus-stage");
const focusFrame = document.querySelector("#focus-frame");
const focusFrameWrap = document.querySelector(".focus-frame-wrap");
const renderStatus = document.querySelector("#render-status");
const deviceControl = document.querySelector(".device-control");

function readState() {
  const params = new URLSearchParams(window.location.search);
  return {
    surface: SURFACES[params.get("surface")] ? params.get("surface") : DEFAULT_STATE.surface,
    view: ["compare", "focus"].includes(params.get("view")) ? params.get("view") : DEFAULT_STATE.view,
    palette: paletteOrder.includes(params.get("palette")) ? params.get("palette") : DEFAULT_STATE.palette,
    device: ["desktop", "mobile"].includes(params.get("device")) ? params.get("device") : DEFAULT_STATE.device,
  };
}

function writeState() {
  const params = new URLSearchParams(state);
  window.history.replaceState(
    null,
    "",
    `${window.location.pathname}?${params.toString()}${window.location.hash}`,
  );
}

function buildOverrideCss(paletteId) {
  const palette = PALETTES[paletteId];
  if (!palette.tokens) return "";

  const variables = Object.entries(palette.tokens)
    .map(([property, value]) => `${property}: ${value} !important;`)
    .join("\n");

  return `
    :root {
      ${variables}
    }

    html { color-scheme: light !important; }

    ::selection {
      background: var(--gold-tint) !important;
      color: var(--ink-900) !important;
    }

    /* Evidence class still requires its word and border treatment. Hue never stands alone. */
    .chip,
    .badge,
    [class*="evidence-chip"] {
      text-decoration-color: currentColor;
    }

    ${palette.polishCss || ""}
  `;
}

function applyPalette(frame, paletteId) {
  try {
    const doc = frame.contentDocument;
    if (!doc || !doc.head) throw new Error("The artboard document is not available.");

    doc.querySelector("#oe-palette-study-override")?.remove();
    doc.documentElement.dataset.paletteStudy = paletteId;

    const css = buildOverrideCss(paletteId);
    if (css) {
      const style = doc.createElement("style");
      style.id = "oe-palette-study-override";
      style.textContent = css;
      doc.head.append(style);
    }

    if (paletteId === "boundaryLedger") {
      const heroPanel = doc.querySelector(".hero > .panel");
      const stateLine = heroPanel?.querySelector(".state-line");
      const rows = heroPanel?.querySelectorAll(".spec-row");

      if (heroPanel && !doc.querySelector(".boundary-episode-figure")) {
        const figure = doc.createElement("figure");
        figure.className = "boundary-episode-figure";

        const sketch = doc.createElement("img");
        sketch.className = "boundary-episode-sketch";
        sketch.src = new URL(
          "./assets/episode-006-hotel-working-model.jpg",
          window.location.href,
        ).href;
        sketch.alt = "A rough hand-drawn working model showing a guest's first hotel stay routed through an OTA toll booth and the second stay returning directly to the hotel.";
        sketch.loading = "eager";
        sketch.decoding = "async";

        figure.append(sketch);
        heroPanel.after(figure);
      }

      if (stateLine) stateLine.textContent = "№006 · Legacy Blueprint";
      if (rows?.[1]) rows[1].querySelector("span").textContent = "Sources";
      if (rows?.[3]) {
        rows[3].querySelector("span").textContent = "Canvas status";
        rows[3].querySelector("b").textContent = "In development";
      }
    }

    return true;
  } catch (error) {
    console.error("Palette injection failed", error);
    return false;
  }
}

function makeComparePanel(paletteId) {
  const palette = PALETTES[paletteId];
  const surface = SURFACES[state.surface];
  const panel = document.createElement("article");
  panel.className = "compare-panel";
  panel.dataset.palette = paletteId;

  const head = document.createElement("div");
  head.className = "compare-panel__head";

  const label = document.createElement("div");
  label.innerHTML = `
    <span class="compare-panel__name">${palette.name}</span>
    <span class="compare-panel__position">${palette.position}</span>
  `;

  const open = document.createElement("button");
  open.type = "button";
  open.textContent = "Open large";
  open.addEventListener("click", () => {
    state.palette = paletteId;
    state.view = "focus";
    render();
    document.querySelector("#preview")?.scrollIntoView({ block: "start" });
  });

  const frame = document.createElement("iframe");
  frame.title = `${palette.name} ${surface.label} preview`;
  frame.loading = "eager";
  frame.style.height = `${surface.compareHeight}px`;
  frame.addEventListener("load", () => {
    const passed = applyPalette(frame, paletteId);
    frame.dataset.loaded = passed ? "true" : "false";
    updateLoadStatus();
  });
  frame.src = surface.path;

  head.append(label, open);
  panel.append(head, frame);
  return panel;
}

function renderCompare() {
  compareGrid.replaceChildren(...paletteOrder.map(makeComparePanel));
  renderStatus.textContent = `Loading ${SURFACES[state.surface].label.toLowerCase()} comparisons.`;
}

function renderFocus() {
  const palette = PALETTES[state.palette];
  const surface = SURFACES[state.surface];

  document.querySelector("#focus-index").textContent = palette.index;
  document.querySelector("#focus-name").textContent = palette.name;
  document.querySelector("#focus-position").textContent = palette.position;
  document.querySelector("#focus-question").textContent = palette.question;
  document.querySelector("#focus-url").textContent = surface.route;

  const roles = document.querySelector("#focus-roles");
  roles.replaceChildren(
    ...palette.roles.map(([term, description]) => {
      const row = document.createElement("div");
      const dt = document.createElement("dt");
      const dd = document.createElement("dd");
      dt.textContent = term;
      dd.textContent = description;
      row.append(dt, dd);
      return row;
    }),
  );

  const focusNotes = document.querySelector(".focus-notes");
  focusNotes.style.setProperty("--focus-paper", palette.colors.paper);
  focusNotes.style.setProperty("--focus-core", palette.colors.core);
  focusNotes.style.setProperty("--focus-perimeter", palette.colors.perimeter);

  focusFrameWrap.dataset.deviceFrame = state.device;
  focusFrame.style.height = `${state.device === "mobile" ? 844 : surface.focusHeight}px`;
  focusFrame.title = `${palette.name} ${surface.label} ${state.device} preview`;
  renderStatus.textContent = `Loading ${palette.name} on the ${surface.label.toLowerCase()}.`;

  focusFrame.onload = () => {
    const passed = applyPalette(focusFrame, state.palette);
    renderStatus.textContent = passed
      ? `${palette.name} rendered on the ${surface.label.toLowerCase()} at ${state.device} width.`
      : "Preview could not be recolored. Run this lab from the repository's local HTTP server.";
  };

  focusFrame.src = surface.path;
}

function updateLoadStatus() {
  const frames = [...compareGrid.querySelectorAll("iframe")];
  const loaded = frames.filter((frame) => frame.dataset.loaded === "true").length;
  const failed = frames.filter((frame) => frame.dataset.loaded === "false").length;
  const surfaceLabel = SURFACES[state.surface].label.toLowerCase();

  if (loaded === frames.length) {
    renderStatus.textContent = `All ${frames.length} ${surfaceLabel} directions rendered. Select Open large to inspect interactions and detail.`;
  } else if (failed > 0) {
    renderStatus.textContent = "One or more previews could not be recolored. Run this lab from the repository's local HTTP server.";
  } else {
    renderStatus.textContent = `Rendered ${loaded} of ${frames.length} ${surfaceLabel} directions.`;
  }
}

function syncControls() {
  document.querySelectorAll("[data-palette]").forEach((button) => {
    const selected = button.dataset.palette === state.palette;
    button.setAttribute("aria-selected", String(selected));
    button.tabIndex = selected ? 0 : -1;
  });

  document.querySelectorAll("[data-surface]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.surface === state.surface));
  });

  document.querySelectorAll("[data-view]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.view === state.view));
  });

  document.querySelectorAll("[data-device]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.device === state.device));
  });

  compareGrid.hidden = state.view !== "compare";
  focusStage.hidden = state.view !== "focus";
  deviceControl.hidden = state.view !== "focus";
}

function render() {
  writeState();
  syncControls();

  if (state.view === "compare") {
    renderCompare();
  } else {
    renderFocus();
  }
}

document.querySelectorAll(".palette-card").forEach((button) => {
  button.addEventListener("click", () => {
    state.palette = button.dataset.palette;
    render();
  });

  button.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const current = paletteOrder.indexOf(button.dataset.palette);
    let next = current;
    if (event.key === "ArrowLeft") next = (current - 1 + paletteOrder.length) % paletteOrder.length;
    if (event.key === "ArrowRight") next = (current + 1) % paletteOrder.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = paletteOrder.length - 1;
    state.palette = paletteOrder[next];
    render();
    document.querySelector(`[data-palette="${state.palette}"]`)?.focus();
  });
});

document.querySelectorAll("[data-surface]").forEach((button) => {
  button.addEventListener("click", () => {
    state.surface = button.dataset.surface;
    render();
  });
});

document.querySelectorAll("[data-view]").forEach((button) => {
  button.addEventListener("click", () => {
    state.view = button.dataset.view;
    render();
  });
});

document.querySelectorAll("[data-device]").forEach((button) => {
  button.addEventListener("click", () => {
    state.device = button.dataset.device;
    render();
  });
});

window.addEventListener("popstate", () => {
  Object.assign(state, readState());
  render();
});

render();
