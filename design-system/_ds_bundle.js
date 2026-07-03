/* @ds-bundle: {"format":4,"namespace":"TheOperatorEconomyDesignSystem_bf951d","components":[{"name":"Annotation","sourcePath":"components/brand/Annotation.jsx"},{"name":"CitationChip","sourcePath":"components/brand/CitationChip.jsx"},{"name":"GapFigure","sourcePath":"components/brand/GapFigure.jsx"},{"name":"Schematic","sourcePath":"components/brand/Schematic.jsx"},{"name":"SchematicNode","sourcePath":"components/brand/SchematicNode.jsx"},{"name":"SheetHeader","sourcePath":"components/brand/SheetHeader.jsx"},{"name":"Stat","sourcePath":"components/brand/Stat.jsx"},{"name":"TitleBlock","sourcePath":"components/brand/TitleBlock.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"BarChart","sourcePath":"components/data/BarChart.jsx"},{"name":"DataTable","sourcePath":"components/data/DataTable.jsx"}],"sourceHashes":{"components/brand/Annotation.jsx":"a7cde85e7023","components/brand/CitationChip.jsx":"31acdbd06523","components/brand/GapFigure.jsx":"58a738124e53","components/brand/Schematic.jsx":"ee2af0eb7249","components/brand/SchematicNode.jsx":"1c4b0897b078","components/brand/SheetHeader.jsx":"6eedbce02560","components/brand/Stat.jsx":"c248c827f9df","components/brand/TitleBlock.jsx":"2613d10c20ae","components/core/Badge.jsx":"e25a6e7b3555","components/core/Button.jsx":"2843a37a7889","components/core/Card.jsx":"220e9d13b9ae","components/core/Input.jsx":"4c181a1a22b4","components/data/BarChart.jsx":"640134bbb566","components/data/DataTable.jsx":"21ae14839173","ui_kits/blueprint/BlueprintApp.jsx":"03a715a2c6e9","ui_kits/newsletter/NewsletterApp.jsx":"dcfe5d88f5c0","ui_kits/website/WebsiteApp.jsx":"4c20a1cd76d4"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.TheOperatorEconomyDesignSystem_bf951d = window.TheOperatorEconomyDesignSystem_bf951d || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/brand/Annotation.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Annotation — the diagram-being-explained motif. Wraps content with a
 * measurement-style bracket and a small-caps label in the margin, as if
 * a schematic were being called out. `side` places the bracket.
 */
function Annotation({
  label,
  side = 'right',
  color = 'var(--drafting-blue)',
  children,
  style,
  ...props
}) {
  const horizontal = side === 'top' || side === 'bottom';
  const bracket = /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: horizontal ? {
      height: '7px',
      borderLeft: `1.5px solid ${color}`,
      borderRight: `1.5px solid ${color}`,
      borderTop: side === 'top' ? 'none' : `1.5px solid ${color}`,
      borderBottom: side === 'top' ? `1.5px solid ${color}` : 'none',
      width: '100%'
    } : {
      width: '7px',
      borderTop: `1.5px solid ${color}`,
      borderBottom: `1.5px solid ${color}`,
      borderLeft: side === 'left' ? 'none' : `1.5px solid ${color}`,
      borderRight: side === 'left' ? `1.5px solid ${color}` : 'none',
      alignSelf: 'stretch'
    }
  });
  const tag = /*#__PURE__*/React.createElement("span", {
    className: "oe-label",
    style: {
      color,
      whiteSpace: horizontal ? 'nowrap' : 'normal',
      writingMode: horizontal ? 'horizontal-tb' : 'horizontal-tb',
      maxWidth: horizontal ? 'none' : '12ch'
    }
  }, label);
  const gap = 'var(--space-3)';
  if (horizontal) {
    return /*#__PURE__*/React.createElement("div", _extends({
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap,
        ...style
      }
    }, props), side === 'top' && /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '4px'
      }
    }, bracket, tag), /*#__PURE__*/React.createElement("div", null, children), side === 'bottom' && /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '4px'
      }
    }, bracket, tag));
  }
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'flex',
      flexDirection: side === 'left' ? 'row' : 'row',
      alignItems: 'stretch',
      gap,
      ...style
    }
  }, props), side === 'left' && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '6px'
    }
  }, tag, bracket), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, children), side === 'right' && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '6px'
    }
  }, bracket, tag));
}
Object.assign(__ds_scope, { Annotation });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/Annotation.jsx", error: String((e && e.message) || e) }); }

// components/brand/CitationChip.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * CitationChip — THE signature element. An on-screen source chip
 * shown every time a number appears: `SOURCE: Sacra · Apr 2026`.
 * Compliance asset, trust asset, and brand asset in one. Mono.
 * `estimate` flags a marked estimate rather than a hard source.
 * `onInk` renders the video lower-third treatment on dark surfaces.
 */
function CitationChip({
  source,
  date,
  estimate = false,
  onInk = false,
  style,
  ...props
}) {
  const label = estimate ? 'ESTIMATE' : 'SOURCE';
  const accent = onInk ? 'var(--gold-bright)' : estimate ? 'var(--gold-700)' : 'var(--drafting-blue)';
  const base = onInk ? {
    background: 'rgba(26,26,26,0.82)',
    color: 'var(--text-on-ink)',
    border: '1px solid rgba(245,240,230,0.16)',
    backdropFilter: 'blur(2px)'
  } : {
    background: 'var(--paper-0)',
    color: 'var(--ink-700)',
    border: '1px solid var(--border)'
  };
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      padding: '4px 10px',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      fontWeight: 'var(--w-mono)',
      letterSpacing: 'var(--tracking-mono)',
      borderRadius: 'var(--radius-xs)',
      borderLeft: `2px solid ${accent}`,
      lineHeight: 1.3,
      whiteSpace: 'nowrap',
      ...base,
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-3xs)',
      fontWeight: 'var(--w-mono)',
      letterSpacing: 'var(--tracking-caps)',
      color: accent
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      opacity: onInk ? 0.9 : 1
    }
  }, source, date ? ` · ${date}` : ''));
}
Object.assign(__ds_scope, { CitationChip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/CitationChip.jsx", error: String((e && e.message) || e) }); }

// components/brand/GapFigure.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * GapFigure — the signature before/after economics gap:
 * "$5.9B → $2K" with the gold arrow. The arrow and destination
 * figure are gold; the origin stays neutral. Optional bracket
 * label underneath ("THE GAP"). Fragment Mono, single weight.
 */
function GapFigure({
  from,
  to,
  label,
  onInk = false,
  size = 'md',
  style,
  ...props
}) {
  const sizes = {
    sm: '1.5rem',
    md: '2.75rem',
    lg: '4.5rem',
    xl: '7rem'
  };
  const gold = onInk ? 'var(--gold-bright)' : 'var(--gold-700)';
  const base = onInk ? 'var(--text-on-ink)' : 'var(--ink-900)';
  const rule = onInk ? 'rgba(245,240,230,0.4)' : 'var(--rule-strong)';
  const muted = onInk ? 'var(--text-on-ink-muted)' : 'var(--text-muted)';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'inline-flex',
      flexDirection: 'column',
      alignItems: 'center',
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 'var(--w-mono)',
      fontSize: sizes[size],
      lineHeight: 1,
      letterSpacing: '-0.02em',
      color: base,
      fontFeatureSettings: "'tnum' 1",
      whiteSpace: 'nowrap'
    }
  }, from, " ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: gold
    }
  }, "\u2192"), " ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: gold
    }
  }, to)), label && /*#__PURE__*/React.createElement("div", {
    style: {
      width: '58%',
      marginTop: '10px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      height: '8px',
      border: `1px solid ${rule}`,
      borderTop: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      marginTop: '8px',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-3xs)',
      letterSpacing: 'var(--tracking-label)',
      textTransform: 'uppercase',
      color: muted
    }
  }, label)));
}
Object.assign(__ds_scope, { GapFigure });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/GapFigure.jsx", error: String((e && e.message) || e) }); }

// components/brand/Schematic.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Schematic — the navy working-schematic panel: drafting grid,
 * sheet tag, live status, nodes wired in sequence, optional
 * measurement bracket and sourced footer. Children (usually
 * SchematicNodes) are automatically joined by wires.
 * RULE: the panel must cite its sources (source prop) and every
 * node must carry a real figure.
 */
function Schematic({
  sheet = 1,
  total = 5,
  title,
  running = 'Running',
  bracket,
  source,
  footer,
  width,
  children,
  style,
  ...props
}) {
  const kids = React.Children.toArray(children);
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      background: 'var(--surface-schematic)',
      backgroundImage: 'repeating-linear-gradient(0deg, var(--schem-grid) 0 1px, transparent 1px 36px),' + 'repeating-linear-gradient(90deg, var(--schem-grid) 0 1px, transparent 1px 36px)',
      padding: '22px 26px',
      width,
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      gap: '16px',
      marginBottom: '24px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: '10.5px',
      letterSpacing: 'var(--tracking-caps)',
      textTransform: 'uppercase',
      color: 'rgba(245,240,230,0.65)'
    }
  }, "Sheet ", String(sheet).padStart(2, '0'), " of ", String(total).padStart(2, '0'), title ? ` — ${title}` : ''), running && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      gap: '7px',
      alignItems: 'center',
      fontFamily: 'var(--font-mono)',
      fontSize: '10px',
      letterSpacing: 'var(--tracking-label)',
      textTransform: 'uppercase',
      color: 'var(--status-live)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "oe-pulse",
    style: {
      width: '6px',
      height: '6px',
      borderRadius: 'var(--radius-pill)',
      background: 'var(--status-live)'
    }
  }), running)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'stretch',
      gap: '18px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column'
    }
  }, kids.map((child, i) => /*#__PURE__*/React.createElement(React.Fragment, {
    key: i
  }, child, i < kids.length - 1 && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      display: 'block',
      width: '1px',
      height: '24px',
      background: 'var(--schem-wire)',
      marginLeft: '44px'
    }
  })))), bracket && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'stretch',
      gap: '9px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      width: '9px',
      border: '1px solid rgba(245,240,230,0.4)',
      borderLeft: 'none'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      alignSelf: 'center',
      writingMode: 'vertical-rl',
      fontFamily: 'var(--font-mono)',
      fontSize: '9px',
      letterSpacing: 'var(--tracking-label)',
      textTransform: 'uppercase',
      color: 'rgba(245,240,230,0.6)',
      whiteSpace: 'nowrap'
    }
  }, bracket))), (source || footer) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      gap: '16px',
      marginTop: '24px'
    }
  }, source ? /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      padding: '4px 10px',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      background: 'rgba(26,26,26,0.5)',
      border: '1px solid rgba(245,240,230,0.22)',
      borderLeft: '2px solid var(--gold-bright)',
      color: 'rgba(245,240,230,0.8)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '9.5px',
      letterSpacing: 'var(--tracking-caps)',
      color: 'var(--gold-bright)'
    }
  }, "SOURCE"), source) : /*#__PURE__*/React.createElement("span", null), footer && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: '12px',
      color: 'rgba(245,240,230,0.85)'
    }
  }, footer)));
}
Object.assign(__ds_scope, { Schematic });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/Schematic.jsx", error: String((e && e.message) || e) }); }

// components/brand/SchematicNode.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * SchematicNode — one labeled node in the working schematic.
 * RULE: every node carries a REAL figure and its source is cited at
 * panel level. Placeholder nodes ("your tool here", "$???") are
 * banned — a node with no figure renders a dev warning.
 * Use inside <Schematic>; also works standalone on navy surfaces.
 */
function SchematicNode({
  step,
  name,
  figure,
  unit,
  status,
  highlight = false,
  style,
  ...props
}) {
  if (figure === undefined || figure === null || figure === '') {
    // eslint-disable-next-line no-console
    console.warn('SchematicNode: every node must carry a real figure + source. Placeholder nodes are banned.');
  }
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      position: 'relative',
      border: '1px solid var(--schem-node-border)',
      background: 'var(--schem-node-bg)',
      padding: '12px 14px',
      borderRadius: 'var(--radius-none)',
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      gap: '10px',
      fontFamily: 'var(--font-mono)',
      fontSize: '9px',
      letterSpacing: '0.12em',
      textTransform: 'uppercase',
      color: 'rgba(245,240,230,0.55)',
      marginBottom: '7px'
    }
  }, /*#__PURE__*/React.createElement("span", null, step), status && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--status-live)'
    }
  }, "\u25CF ", status)), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: '14.5px',
      fontWeight: 'var(--w-medium)',
      color: 'var(--paper-100)',
      marginBottom: '6px'
    }
  }, name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 'var(--w-mono)',
      fontSize: '17px',
      color: highlight ? 'var(--gold-bright)' : 'rgba(245,240,230,0.92)',
      fontFeatureSettings: "'tnum' 1"
    }
  }, figure ?? '—', unit && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '11px',
      color: 'rgba(245,240,230,0.55)'
    }
  }, unit)));
}
Object.assign(__ds_scope, { SchematicNode });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/SchematicNode.jsx", error: String((e && e.message) || e) }); }

// components/brand/SheetHeader.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * SheetHeader — chapter card styled as a drawing sheet:
 * "SHEET 2 OF 5 — UNIT ECONOMICS". Used for video chapter cards,
 * LinkedIn carousel sheets, and blueprint section dividers.
 * `onInk` for the dark video treatment.
 */
function SheetHeader({
  sheet = 2,
  total = 5,
  title,
  subtitle,
  onInk = false,
  style,
  ...props
}) {
  const strong = onInk ? 'var(--text-on-ink)' : 'var(--ink-900)';
  const muted = onInk ? 'var(--text-on-ink-muted)' : 'var(--ink-500)';
  const rule = onInk ? 'rgba(245,240,230,0.28)' : 'var(--rule-strong)';
  const accent = onInk ? 'var(--gold-bright)' : 'var(--drafting-blue)';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-4)',
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-3)',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-caps)',
      color: accent,
      fontWeight: 'var(--w-mono)'
    }
  }, /*#__PURE__*/React.createElement("span", null, "Sheet ", String(sheet).padStart(2, '0'), " of ", String(total).padStart(2, '0')), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      height: '1px',
      background: rule
    }
  })), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--w-bold)',
      fontSize: 'var(--text-2xl)',
      lineHeight: 'var(--leading-snug)',
      letterSpacing: 'var(--tracking-heading)',
      color: strong,
      margin: 0
    }
  }, title), subtitle && /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-base)',
      color: muted,
      margin: 0,
      maxWidth: '56ch'
    }
  }, subtitle));
}
Object.assign(__ds_scope, { SheetHeader });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/SheetHeader.jsx", error: String((e && e.message) || e) }); }

// components/brand/Stat.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Stat — a single published figure in mono numerals with its unit and
 * an optional label + delta. The evidence object, not decoration.
 * `emphasis="gold"` marks the one key figure per view. `size` scales
 * from inline data to a thumbnail-grade display number.
 */
function Stat({
  value,
  unit,
  prefix,
  label,
  delta,
  deltaDirection,
  emphasis = 'default',
  size = 'md',
  onInk = false,
  style,
  ...props
}) {
  const sizes = {
    sm: 'var(--text-xl)',
    md: 'var(--text-3xl)',
    lg: 'var(--text-4xl)',
    xl: 'var(--text-5xl)'
  };
  const valueColor = onInk ? emphasis === 'gold' ? 'var(--gold-bright)' : 'var(--text-on-ink)' : emphasis === 'gold' ? 'var(--gold-700)' : emphasis === 'accent' ? 'var(--drafting-blue)' : 'var(--ink-900)';
  const labelColor = onInk ? 'var(--text-on-ink-muted)' : 'var(--text-muted)';
  const deltaColor = deltaDirection === 'down' ? 'var(--negative)' : deltaDirection === 'up' ? 'var(--sage-700)' : 'var(--text-muted)';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '6px',
      ...style
    }
  }, props), label && /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      color: labelColor
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: '10px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 'var(--w-mono)',
      fontSize: sizes[size],
      lineHeight: 1,
      letterSpacing: '-0.01em',
      color: valueColor,
      fontFeatureSettings: "'tnum' 1, 'zero' 1"
    }
  }, prefix, value, unit && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '0.55em',
      fontWeight: 'var(--w-mono)',
      marginLeft: '2px',
      opacity: 0.75
    }
  }, unit)), delta && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--w-mono)',
      color: deltaColor
    }
  }, deltaDirection === 'up' ? '▲' : deltaDirection === 'down' ? '▼' : '', " ", delta)));
}
Object.assign(__ds_scope, { Stat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/Stat.jsx", error: String((e && e.message) || e) }); }

// components/brand/TitleBlock.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * TitleBlock — the drafting-style title block on every blueprint PDF,
 * video end-card, and chart. Signals "versioned, sourced document",
 * not lead-gen PDF. A framed grid of mono metadata fields.
 * `onInk` for dark end-cards.
 */
function TitleBlock({
  docNumber = 'Operator Blueprint №004',
  title,
  fields = [],
  onInk = false,
  style,
  ...props
}) {
  const ink = onInk;
  const frame = ink ? 'rgba(245,240,230,0.28)' : 'var(--rule-strong)';
  const strong = ink ? 'var(--text-on-ink)' : 'var(--ink-900)';
  const muted = ink ? 'var(--text-on-ink-muted)' : 'var(--ink-500)';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      border: `1.5px solid ${frame}`,
      borderRadius: 'var(--radius-xs)',
      background: ink ? 'transparent' : 'var(--paper-0)',
      fontFamily: 'var(--font-mono)',
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'baseline',
      gap: 'var(--space-4)',
      padding: '10px 16px',
      borderBottom: `1px solid ${frame}`,
      fontSize: 'var(--text-3xs)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-caps)',
      color: ink ? 'var(--gold-bright)' : 'var(--drafting-blue)',
      fontWeight: 'var(--w-mono)'
    }
  }, /*#__PURE__*/React.createElement("span", null, docNumber), /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted
    }
  }, "The Operator Economy")), title && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '16px',
      borderBottom: fields.length ? `1px solid ${frame}` : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--w-bold)',
      fontSize: 'var(--text-xl)',
      lineHeight: 'var(--leading-snug)',
      color: strong,
      letterSpacing: 'var(--tracking-tight)'
    }
  }, title)), fields.length > 0 && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: `repeat(${Math.min(fields.length, 4)}, 1fr)`
    }
  }, fields.map((f, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      padding: '10px 16px',
      borderRight: (i + 1) % Math.min(fields.length, 4) !== 0 ? `1px solid ${frame}` : 'none',
      borderTop: i >= Math.min(fields.length, 4) ? `1px solid ${frame}` : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--text-3xs)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-caps)',
      color: muted,
      marginBottom: '4px'
    }
  }, f.label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--w-mono)',
      color: strong
    }
  }, f.value)))));
}
Object.assign(__ds_scope, { TitleBlock });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/TitleBlock.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Badge — small-caps annotation label / status tag.
 * Reads like a drafting stamp, not a pill. Tones map to brand
 * semantics: neutral, accent (blue), gold (key), positive (sage),
 * negative (brick). Set `dot` for a status marker.
 */
function Badge({
  tone = 'neutral',
  dot = false,
  children,
  style,
  ...props
}) {
  const tones = {
    neutral: {
      color: 'var(--ink-700)',
      border: 'var(--border-strong)',
      bg: 'var(--paper-0)'
    },
    accent: {
      color: 'var(--drafting-blue)',
      border: 'var(--drafting-blue)',
      bg: 'var(--blue-tint)'
    },
    gold: {
      color: 'var(--gold-700)',
      border: 'var(--gold-500)',
      bg: 'var(--gold-tint)'
    },
    positive: {
      color: 'var(--sage-700)',
      border: 'var(--sage-500)',
      bg: 'transparent'
    },
    negative: {
      color: 'var(--negative)',
      border: 'var(--negative)',
      bg: 'transparent'
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      padding: '3px 8px',
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--w-semibold)',
      fontSize: 'var(--text-3xs)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      color: t.color,
      background: t.bg,
      border: `1px solid ${t.border}`,
      borderRadius: 'var(--radius-xs)',
      lineHeight: 1,
      whiteSpace: 'nowrap',
      ...style
    }
  }, props), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: '6px',
      height: '6px',
      borderRadius: 'var(--radius-pill)',
      background: t.color,
      flex: '0 0 auto'
    }
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Button — Welsh-grade restraint. One clear action per view.
 * Variants: primary (Drafting Blue), secondary (outline), ghost (text).
 * Never neon, never gradient. Square-ish corners; the label is sans.
 */
function Button({
  variant = 'primary',
  size = 'md',
  as = 'button',
  fullWidth = false,
  disabled = false,
  children,
  style,
  ...props
}) {
  const sizes = {
    sm: {
      padding: '7px 14px',
      fontSize: 'var(--text-xs)'
    },
    md: {
      padding: '10px 20px',
      fontSize: 'var(--text-sm)'
    },
    lg: {
      padding: '14px 28px',
      fontSize: 'var(--text-base)'
    }
  };
  const variants = {
    primary: {
      background: 'var(--accent)',
      color: 'var(--paper-100)',
      border: '1px solid var(--accent)'
    },
    secondary: {
      background: 'transparent',
      color: 'var(--ink-900)',
      border: '1px solid var(--border-strong)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--accent)',
      border: '1px solid transparent'
    }
  };
  const Tag = as;
  return /*#__PURE__*/React.createElement(Tag, _extends({
    disabled: Tag === 'button' ? disabled : undefined,
    "data-variant": variant,
    className: "oe-btn",
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 'var(--space-2)',
      width: fullWidth ? '100%' : 'auto',
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--w-semibold)',
      lineHeight: 1,
      letterSpacing: '0.005em',
      borderRadius: 'var(--radius-sm)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.45 : 1,
      transition: 'background var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard), color var(--dur-fast) var(--ease-standard)',
      textDecoration: 'none',
      whiteSpace: 'nowrap',
      ...sizes[size],
      ...variants[variant],
      ...style
    }
  }, props), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Card — a blueprint surface. Near-square corners, hairline rule,
 * whisper-quiet shadow. Depth comes from paper tone, not float.
 * Use `sheet` to add the top drafting rule + optional kicker label.
 */
function Card({
  as = 'div',
  kicker,
  sheet = false,
  padding = 'md',
  children,
  style,
  ...props
}) {
  const pads = {
    none: 0,
    sm: 'var(--space-4)',
    md: 'var(--space-5)',
    lg: 'var(--space-6)'
  };
  const Tag = as;
  return /*#__PURE__*/React.createElement(Tag, _extends({
    style: {
      background: 'var(--surface-card)',
      border: '1px solid var(--border)',
      borderTop: sheet ? '2px solid var(--drafting-blue)' : '1px solid var(--border)',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      padding: pads[padding],
      ...style
    }
  }, props), kicker && /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      marginBottom: 'var(--space-3)'
    }
  }, kicker), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Input — text field for the one capture the site allows (email).
 * Sunken paper well, hairline border, blue focus. Mono variant for
 * numeric/code entry. Pair with a small-caps <label className="oe-label">.
 */
function Input({
  mono = false,
  invalid = false,
  size = 'md',
  style,
  ...props
}) {
  const sizes = {
    sm: {
      padding: '8px 10px',
      fontSize: 'var(--text-sm)'
    },
    md: {
      padding: '11px 14px',
      fontSize: 'var(--text-base)'
    },
    lg: {
      padding: '14px 16px',
      fontSize: 'var(--text-lg)'
    }
  };
  return /*#__PURE__*/React.createElement("input", _extends({
    className: "oe-input",
    style: {
      width: '100%',
      fontFamily: mono ? 'var(--font-mono)' : 'var(--font-sans)',
      fontWeight: 'var(--w-regular)',
      color: 'var(--ink-900)',
      background: 'var(--paper-0)',
      border: `1px solid ${invalid ? 'var(--negative)' : 'var(--border-strong)'}`,
      borderRadius: 'var(--radius-xs)',
      boxShadow: 'var(--shadow-inset)',
      lineHeight: 1.4,
      transition: 'border-color var(--dur-fast) var(--ease-standard), box-shadow var(--dur-fast) var(--ease-standard)',
      ...sizes[size],
      ...style
    }
  }, props));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/data/BarChart.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * BarChart — a custom chart that reads as institutional research, never
 * default Excel. Drafting-Blue bars on a baseline axis, mono value
 * labels, one optional Ledger-Gold highlight bar, sourced footer.
 * data: [{ label, value, highlight? }]
 */
function BarChart({
  data = [],
  unit = '',
  prefix = '',
  height = 220,
  source,
  format,
  style,
  ...props
}) {
  const max = Math.max(...data.map(d => d.value), 1);
  const fmt = format || (v => `${prefix}${v.toLocaleString()}${unit}`);
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      fontFamily: 'var(--font-sans)',
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      gap: 'var(--space-5)',
      height,
      borderBottom: '1.5px solid var(--ink-900)',
      paddingBottom: 0
    }
  }, data.map((d, i) => {
    const h = Math.max(d.value / max * 100, 1.5);
    const color = d.highlight ? 'var(--ledger-gold)' : 'var(--drafting-blue)';
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-end',
        alignItems: 'center',
        height: '100%'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-sm)',
        fontWeight: 'var(--w-mono)',
        color: d.highlight ? 'var(--gold-700)' : 'var(--ink-900)',
        marginBottom: '8px',
        fontFeatureSettings: "'tnum' 1",
        whiteSpace: 'nowrap'
      }
    }, fmt(d.value)), /*#__PURE__*/React.createElement("div", {
      style: {
        width: '100%',
        maxWidth: '96px',
        height: `${h}%`,
        background: color,
        transition: 'height var(--dur-slow) var(--ease-out)'
      }
    }));
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 'var(--space-5)',
      marginTop: '10px'
    }
  }, data.map((d, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "oe-label",
    style: {
      flex: 1,
      textAlign: 'center',
      color: 'var(--text-muted)'
    }
  }, d.label))), source && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'var(--space-4)',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-3xs)',
      letterSpacing: 'var(--tracking-caps)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)'
    }
  }, "Source: ", source));
}
Object.assign(__ds_scope, { BarChart });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/BarChart.jsx", error: String((e && e.message) || e) }); }

// components/data/DataTable.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * DataTable — a ledger. Mono numerals, right-aligned, hairline rules,
 * optional zebra rows and a source footer. Numeric columns are mono
 * automatically; the first column reads as a label in sans.
 * columns: [{ key, label, align?, numeric? }]
 */
function DataTable({
  columns = [],
  rows = [],
  source,
  zebra = true,
  style,
  ...props
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-xs)',
      overflow: 'hidden',
      background: 'var(--paper-0)',
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      borderCollapse: 'collapse',
      fontFamily: 'var(--font-sans)'
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, columns.map(c => /*#__PURE__*/React.createElement("th", {
    key: c.key,
    style: {
      textAlign: c.align || (c.numeric ? 'right' : 'left'),
      padding: '10px 16px',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-3xs)',
      fontWeight: 'var(--w-semibold)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      color: 'var(--text-muted)',
      borderBottom: '1.5px solid var(--border-strong)',
      background: 'var(--paper-200)',
      whiteSpace: 'nowrap'
    }
  }, c.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, ri) => /*#__PURE__*/React.createElement("tr", {
    key: ri,
    style: {
      background: zebra && ri % 2 === 1 ? 'var(--paper-100)' : 'transparent'
    }
  }, columns.map((c, ci) => /*#__PURE__*/React.createElement("td", {
    key: c.key,
    style: {
      textAlign: c.align || (c.numeric ? 'right' : 'left'),
      padding: '11px 16px',
      fontFamily: c.numeric ? 'var(--font-mono)' : 'var(--font-sans)',
      fontSize: 'var(--text-sm)',
      fontWeight: ci === 0 ? 'var(--w-medium)' : 'var(--w-regular)',
      color: ci === 0 ? 'var(--ink-900)' : 'var(--ink-700)',
      fontFeatureSettings: c.numeric ? "'tnum' 1, 'zero' 1" : undefined,
      borderBottom: ri < rows.length - 1 ? '1px solid var(--border)' : 'none',
      whiteSpace: 'nowrap'
    }
  }, r[c.key])))))), source && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '8px 16px',
      borderTop: '1px solid var(--border)',
      background: 'var(--paper-200)',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-3xs)',
      letterSpacing: 'var(--tracking-caps)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)'
    }
  }, "Source: ", source));
}
Object.assign(__ds_scope, { DataTable });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/DataTable.jsx", error: String((e && e.message) || e) }); }

// ui_kits/blueprint/BlueprintApp.jsx
try { (() => {
/* BlueprintApp — Operator Blueprint PDF. Paper, title block, mono
   tables, annotated data, full source list. Real operator documentation
   a VP would save and annotate. Composes DS primitives. */
const OE_B = window.TheOperatorEconomyDesignSystem_bf951d;
const {
  TitleBlock: BTitle,
  SheetHeader: BSheet,
  DataTable: BTable,
  BarChart: BChart,
  Stat: BStat,
  CitationChip: BCite,
  Badge: BBadge,
  Annotation: BAnno
} = OE_B;
function DocFooter({
  page
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderTop: '1px solid var(--border)',
      paddingTop: 12,
      marginTop: 40
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "The Operator Economy \xB7 Blueprint \u2116004"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "Sheet ", page, " of 3"));
}
function Sheet({
  children,
  page
}) {
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: 'var(--paper-0)',
      border: '1px solid var(--border)',
      boxShadow: 'var(--shadow-md)',
      width: 820,
      margin: '0 auto 32px',
      padding: '56px 64px'
    }
  }, children, /*#__PURE__*/React.createElement(DocFooter, {
    page: page
  }));
}
function BlueprintApp() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '40px 20px 64px'
    }
  }, /*#__PURE__*/React.createElement(Sheet, {
    page: 1
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      marginBottom: 40
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      lineHeight: 1.1
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "The"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontWeight: 600,
      fontSize: 20,
      color: 'var(--ink-900)'
    }
  }, "Operator Economy")), /*#__PURE__*/React.createElement(BBadge, {
    tone: "accent"
  }, "Operator Blueprint")), /*#__PURE__*/React.createElement("h1", {
    style: {
      font: 'var(--type-display)',
      fontSize: 52,
      color: 'var(--ink-900)',
      margin: '0 0 16px',
      lineHeight: 1.05
    }
  }, "AI Implementation", /*#__PURE__*/React.createElement("br", null), "as a Service"), /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-lead)',
      color: 'var(--text-body)',
      maxWidth: '52ch',
      margin: '0 0 40px'
    }
  }, "Who pays, what they pay for, the real numbers at both ends of the market, the exact tool stack, and a step-by-step plan to a first client."), /*#__PURE__*/React.createElement(BTitle, {
    docNumber: "Operator Blueprint \u2116004",
    title: "AI Implementation as a Service",
    fields: [{
      label: 'Date',
      value: '2026-06-14'
    }, {
      label: 'Revision',
      value: 'B'
    }, {
      label: 'Sources',
      value: '11'
    }, {
      label: 'Difficulty',
      value: 'Med'
    }]
  })), /*#__PURE__*/React.createElement(Sheet, {
    page: 2
  }, /*#__PURE__*/React.createElement(BSheet, {
    sheet: 2,
    total: 3,
    title: "Unit economics",
    subtitle: "The same service exists at three scales. The only variable is who's buying."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 40,
      margin: '36px 0'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      marginBottom: 16
    }
  }, "Accenture GenAI bookings"), /*#__PURE__*/React.createElement(BChart, {
    prefix: "$",
    unit: "B",
    data: [{
      label: 'FY24',
      value: 3.0
    }, {
      label: 'FY25',
      value: 5.9,
      highlight: true
    }],
    source: "Accenture Annual Report 2025",
    height: 180
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 24,
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(BAnno, {
    label: "Proves demand",
    side: "left"
  }, /*#__PURE__*/React.createElement(BStat, {
    prefix: "$",
    value: "5.9",
    unit: "B",
    label: "Enterprise ceiling",
    emphasis: "gold",
    size: "md"
  })), /*#__PURE__*/React.createElement(BAnno, {
    label: "Where you start",
    side: "left",
    color: "var(--sage-700)"
  }, /*#__PURE__*/React.createElement(BStat, {
    prefix: "$",
    value: "5\u20136K",
    unit: "/mo",
    label: "Freelancer floor",
    size: "md"
  })))), /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      margin: '8px 0 12px'
    }
  }, "Pricing across the market"), /*#__PURE__*/React.createElement(BTable, {
    columns: [{
      key: 'tier',
      label: 'Tier'
    }, {
      key: 'first',
      label: 'First project',
      numeric: true
    }, {
      key: 'retainer',
      label: 'Monthly retainer',
      numeric: true
    }, {
      key: 'clients',
      label: 'Typical clients',
      numeric: true
    }],
    rows: [{
      tier: 'Freelancer',
      first: '$2,000',
      retainer: '$500–2,000',
      clients: '1–3'
    }, {
      tier: 'Boutique agency',
      first: '$8,000',
      retainer: '$3,000–5,000',
      clients: '5–10'
    }, {
      tier: 'Enterprise (ref.)',
      first: '$5.9B',
      retainer: '—',
      clients: 'Global 2000'
    }],
    source: "Multiple creator reports; ranges consistent \u2014 estimate"
  })), /*#__PURE__*/React.createElement(Sheet, {
    page: 3
  }, /*#__PURE__*/React.createElement(BSheet, {
    sheet: 3,
    total: 3,
    title: "The stack & the plan",
    subtitle: "Under $100/mo in tooling. The margin is your judgment, not your infrastructure."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr 1fr',
      gap: 16,
      margin: '32px 0'
    }
  }, [{
    l: 'The brain',
    v: 'Claude / ChatGPT',
    p: '$20–40/mo'
  }, {
    l: 'The runtime',
    v: 'n8n · Make · Zapier',
    p: '~$0–50/mo'
  }, {
    l: 'Client layer',
    v: 'Airtable / Notion',
    p: '$0–20/mo'
  }].map(s => /*#__PURE__*/React.createElement("div", {
    key: s.l,
    style: {
      border: '1px solid var(--border)',
      borderTop: '2px solid var(--drafting-blue)',
      borderRadius: 'var(--radius-xs)',
      padding: '16px',
      background: 'var(--paper-100)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      marginBottom: 8
    }
  }, s.l), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 600,
      fontSize: 15,
      color: 'var(--ink-900)',
      marginBottom: 6
    }
  }, s.v), /*#__PURE__*/React.createElement("div", {
    className: "oe-mono",
    style: {
      fontSize: 13,
      color: 'var(--gold-700)',
      fontWeight: 600
    }
  }, s.p)))), /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      margin: '32px 0 14px'
    }
  }, "Sources"), /*#__PURE__*/React.createElement("ol", {
    style: {
      margin: 0,
      padding: 0,
      listStyle: 'none',
      counterReset: 'src',
      display: 'flex',
      flexDirection: 'column',
      gap: 8
    }
  }, ['CIO Dive — Accenture GenAI bookings, FY2025', 'Constellation Research — enterprise AI services analysis, Q1 FY2026', 'Accenture Annual Report 2025', 'Medium / The AI Studio — solo agency report, Mar 2026 (unverified)', 'Public tool pricing — Anthropic, OpenAI, n8n, Make, Zapier'].map((src, i) => /*#__PURE__*/React.createElement("li", {
    key: i,
    style: {
      display: 'flex',
      gap: 12,
      fontFamily: 'var(--font-mono)',
      fontSize: 13,
      color: 'var(--ink-700)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--drafting-blue)',
      fontWeight: 600
    }
  }, "[", String(i + 1).padStart(2, '0'), "]"), /*#__PURE__*/React.createElement("span", null, src)))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 28,
      display: 'flex',
      gap: 10,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(BCite, {
    source: "CIO Dive",
    date: "FY2025"
  }), /*#__PURE__*/React.createElement(BCite, {
    source: "Creator reports",
    estimate: true
  }))));
}
window.BlueprintApp = BlueprintApp;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/blueprint/BlueprintApp.jsx", error: String((e && e.message) || e) }); }

// ui_kits/newsletter/NewsletterApp.jsx
try { (() => {
/* NewsletterApp — the Monday email styled as a research note.
   Doc number, date, reading time, sources. Single reading column.
   Composes DS primitives from the bundle. */
const OE_N = window.TheOperatorEconomyDesignSystem_bf951d;
const {
  Badge: NBadge,
  CitationChip: NCite,
  Stat: NStat,
  DataTable: NTable,
  SheetHeader: NSheet,
  Button: NButton
} = OE_N;
function MastheadN() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      borderBottom: '2px solid var(--ink-900)',
      paddingBottom: 16,
      marginBottom: 32
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'baseline'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontWeight: 600,
      fontSize: 22,
      color: 'var(--ink-900)'
    }
  }, "The Operator Economy"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "Issue \u2116004 \xB7 Monday")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 18,
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "2026-06-16"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "\xB7"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "9 min read"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "\xB7"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, "11 sources")));
}
function Para({
  children
}) {
  return /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-body)',
      color: 'var(--text-body)',
      margin: '0 0 20px',
      fontSize: 18,
      lineHeight: 1.7
    }
  }, children);
}
function NewsletterApp() {
  return /*#__PURE__*/React.createElement("article", {
    style: {
      maxWidth: 680,
      margin: '0 auto',
      padding: '56px 32px 80px'
    }
  }, /*#__PURE__*/React.createElement(MastheadN, null), /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      color: 'var(--drafting-blue)',
      marginBottom: 14
    }
  }, "This week's thesis"), /*#__PURE__*/React.createElement("h1", {
    style: {
      font: 'var(--type-h1)',
      fontSize: 40,
      color: 'var(--ink-900)',
      margin: '0 0 24px',
      lineHeight: 1.1
    }
  }, "You can sell AI implementation to businesses drowning in it."), /*#__PURE__*/React.createElement(Para, null, "Last year, Accenture booked ", /*#__PURE__*/React.createElement("span", {
    className: "oe-mono",
    style: {
      fontWeight: 600,
      color: 'var(--gold-700)'
    }
  }, "$5.9B"), " of generative-AI work \u2014 not ", /*#__PURE__*/React.createElement("em", null, "building"), " AI, ", /*#__PURE__*/React.createElement("em", null, "installing"), " it. The same service, at solo scale, is a ", /*#__PURE__*/React.createElement("span", {
    className: "oe-mono",
    style: {
      fontWeight: 600
    }
  }, "$2,000"), " project one operator can sell in a month."), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: '0 0 28px'
    }
  }, /*#__PURE__*/React.createElement(NCite, {
    source: "CIO Dive \xB7 Constellation Research",
    date: "Accenture FY2025"
  })), /*#__PURE__*/React.createElement(Para, null, "Here's the thesis. Every business now knows it's supposed to be using AI, and almost none of them know how. That gap between knowing and doing is a service business \u2014 and it's called implementation."), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: '36px 0'
    }
  }, /*#__PURE__*/React.createElement(NSheet, {
    sheet: 1,
    total: 3,
    title: "The market, both ends",
    subtitle: "Start at the top because it proves demand; the floor is where you actually start."
  })), /*#__PURE__*/React.createElement(Para, null, "Accenture's GenAI bookings roughly doubled while overall new bookings stayed flat \u2014 the implementation work is the only thing growing. By late 2025 they stopped reporting it separately because it touched ", /*#__PURE__*/React.createElement("span", {
    className: "oe-mono",
    style: {
      fontWeight: 600
    }
  }, "80%"), " of large deals."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 40,
      margin: '28px 0'
    }
  }, /*#__PURE__*/React.createElement(NStat, {
    prefix: "$",
    value: "5.9",
    unit: "B",
    label: "GenAI bookings, FY25",
    emphasis: "gold",
    size: "md"
  }), /*#__PURE__*/React.createElement(NStat, {
    value: "80",
    unit: "%",
    label: "of large deals touched",
    size: "md"
  }), /*#__PURE__*/React.createElement(NStat, {
    value: "~2",
    unit: "\xD7",
    label: "YoY growth",
    delta: "flat overall",
    deltaDirection: "flat",
    size: "md"
  })), /*#__PURE__*/React.createElement(Para, null, "The floor is better documented because it's boring: freelancers doing AI automation at ", /*#__PURE__*/React.createElement("span", {
    className: "oe-mono",
    style: {
      fontWeight: 600
    }
  }, "$5\u20136K/mo"), " on about ", /*#__PURE__*/React.createElement("span", {
    className: "oe-mono",
    style: {
      fontWeight: 600
    }
  }, "$20"), " of tooling. Pricing converges across every source:"), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: '0 0 12px'
    }
  }, /*#__PURE__*/React.createElement(NTable, {
    columns: [{
      key: 'tier',
      label: 'Tier'
    }, {
      key: 'first',
      label: 'First project',
      numeric: true
    }, {
      key: 'retainer',
      label: 'Monthly retainer',
      numeric: true
    }, {
      key: 'tooling',
      label: 'Tooling',
      numeric: true
    }],
    rows: [{
      tier: 'Freelancer',
      first: '$2,000',
      retainer: '$500',
      tooling: '$20'
    }, {
      tier: 'Boutique',
      first: '$8,000',
      retainer: '$3,000',
      tooling: '$180'
    }, {
      tier: 'Accenture',
      first: '$5.9B',
      retainer: '—',
      tooling: '—'
    }],
    source: "Creator reports; ranges consistent across sources \u2014 estimate"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: '10px 0 28px'
    }
  }, /*#__PURE__*/React.createElement(NBadge, {
    tone: "gold"
  }, "Marked estimate")), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: '36px 0'
    }
  }, /*#__PURE__*/React.createElement(NSheet, {
    sheet: 2,
    total: 3,
    title: "The stack under $100/mo",
    subtitle: "The brain, the runtime, the client-facing layer."
  })), /*#__PURE__*/React.createElement(Para, null, "The brain is Claude or ChatGPT at ", /*#__PURE__*/React.createElement("span", {
    className: "oe-mono",
    style: {
      fontWeight: 600
    }
  }, "$20\u201340"), ". The runtime is n8n, Make, or Zapier \u2014 self-hosted n8n is close to free, which matters when you're quoting margins. The client-facing layer is Airtable or Notion: the dashboard they log into and feel ownership of."), /*#__PURE__*/React.createElement("div", {
    style: {
      borderTop: '1px solid var(--border)',
      borderBottom: '1px solid var(--border)',
      padding: '28px 0',
      margin: '40px 0',
      display: 'flex',
      flexDirection: 'column',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "oe-label"
  }, "Download the full blueprint"), /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-body)',
      color: 'var(--text-muted)',
      margin: 0
    }
  }, "Operator Blueprint \u2116004 \u2014 the who-pays map, the exact stack, a step-by-step plan to a first client, and the full source list."), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(NButton, {
    variant: "primary"
  }, "Get Blueprint \u2116004 (free)"))), /*#__PURE__*/React.createElement("p", {
    className: "oe-caps",
    style: {
      color: 'var(--text-faint)',
      marginTop: 40
    }
  }, "The Operator Economy \xB7 Build. Own. Operate. \xB7 Reply to this email and tell me what you'd build."));
}
window.NewsletterApp = NewsletterApp;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/newsletter/NewsletterApp.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/WebsiteApp.jsx
try { (() => {
/* WebsiteApp — theoperatoreconomy.com landing.
   Welsh-grade restraint: one promise, one capture, evidence up front.
   Composes DS primitives from the bundle namespace. */
const OE = window.TheOperatorEconomyDesignSystem_bf951d;
const {
  Button,
  Badge,
  Card,
  Input,
  CitationChip,
  Stat,
  TitleBlock,
  BarChart,
  DataTable
} = OE;
function Header() {
  const [active, setActive] = React.useState('Episodes');
  const items = ['Episodes', 'Blueprints', 'Newsletter', 'About'];
  return /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '20px 48px',
      borderBottom: '1px solid var(--border)',
      position: 'sticky',
      top: 0,
      background: 'rgba(245,240,230,0.86)',
      backdropFilter: 'blur(8px)',
      zIndex: 100
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      lineHeight: 1
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 11,
      letterSpacing: '0.14em',
      textTransform: 'uppercase',
      color: 'var(--text-muted)'
    }
  }, "The"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontWeight: 600,
      fontSize: 22,
      color: 'var(--ink-900)',
      letterSpacing: '-0.01em'
    }
  }, "Operator Economy")), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: 28,
      alignItems: 'center'
    }
  }, items.map(it => /*#__PURE__*/React.createElement("a", {
    key: it,
    href: "#",
    onClick: e => {
      e.preventDefault();
      setActive(it);
    },
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 14,
      fontWeight: 500,
      color: active === it ? 'var(--ink-900)' : 'var(--text-muted)',
      borderBottom: active === it ? '2px solid var(--drafting-blue)' : '2px solid transparent',
      paddingBottom: 4,
      textDecoration: 'none'
    }
  }, it)), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "sm"
  }, "Get the newsletter")));
}
function Hero() {
  return /*#__PURE__*/React.createElement("section", {
    style: {
      padding: '84px 48px 64px',
      maxWidth: 1120,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1.15fr 0.85fr',
      gap: 64,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "oe-caps",
    style: {
      marginBottom: 20
    }
  }, "Evidence-first \xB7 No hype \xB7 Real numbers"), /*#__PURE__*/React.createElement("h1", {
    style: {
      font: 'var(--type-display)',
      fontSize: 60,
      color: 'var(--ink-900)',
      margin: '0 0 24px',
      letterSpacing: '-0.015em',
      lineHeight: 1.04
    }
  }, "The businesses you could ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--drafting-blue)'
    }
  }, "actually"), " build."), /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-lead)',
      color: 'var(--text-body)',
      maxWidth: '46ch',
      margin: '0 0 32px'
    }
  }, "AI collapsed the cost of building. Every week we take one real business, source the numbers, and show you exactly how hard it is to build your own version \u2014 documentary rigor, zero hustle."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 12,
      alignItems: 'center',
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg"
  }, "Watch the latest breakdown"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "lg"
  }, "Browse the blueprint library"))), /*#__PURE__*/React.createElement(TitleBlock, {
    docNumber: "Operator Blueprint \u2116004",
    title: "AI Implementation as a Service",
    fields: [{
      label: 'Date',
      value: '2026-06-14'
    }, {
      label: 'Revision',
      value: 'B'
    }, {
      label: 'Sources',
      value: '11'
    }, {
      label: 'Read',
      value: '9 min'
    }]
  })));
}
function EvidenceFeature() {
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: 'var(--ink)',
      padding: '72px 48px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1120,
      margin: '0 auto',
      display: 'grid',
      gridTemplateColumns: '0.9fr 1.1fr',
      gap: 64,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      color: 'var(--sage-500)',
      marginBottom: 16
    }
  }, "This week's thesis"), /*#__PURE__*/React.createElement("h2", {
    style: {
      font: 'var(--type-h1)',
      fontSize: 40,
      color: 'var(--paper)',
      margin: '0 0 20px',
      letterSpacing: '-0.01em'
    }
  }, "The gap between knowing and doing is a service business."), /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-body)',
      color: 'var(--text-on-ink-muted)',
      maxWidth: '42ch',
      margin: '0 0 28px'
    }
  }, "Accenture booked billions installing AI it didn't build. The exact same service exists at solo scale \u2014 and businesses at every size are buying."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 32,
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement(Stat, {
    prefix: "$",
    value: "5.9",
    unit: "B",
    label: "Accenture GenAI bookings",
    emphasis: "gold",
    size: "lg",
    onInk: true
  }), /*#__PURE__*/React.createElement(Stat, {
    prefix: "$",
    value: "2,000",
    label: "The solo version",
    size: "lg",
    onInk: true
  })), /*#__PURE__*/React.createElement(CitationChip, {
    source: "CIO Dive \xB7 Constellation Research",
    date: "FY2025",
    onInk: true
  })), /*#__PURE__*/React.createElement(Card, {
    padding: "lg",
    style: {
      background: 'var(--paper-0)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      marginBottom: 18
    }
  }, "Accenture generative-AI bookings"), /*#__PURE__*/React.createElement(BarChart, {
    prefix: "$",
    unit: "B",
    data: [{
      label: 'FY24',
      value: 3.0
    }, {
      label: 'FY25',
      value: 5.9,
      highlight: true
    }],
    source: "Accenture Annual Report 2025",
    height: 190
  }))));
}
function BlueprintLibrary() {
  const items = [{
    n: '№004',
    title: 'AI Implementation as a Service',
    read: '9 min',
    tag: 'Services'
  }, {
    n: '№003',
    title: 'The Vertical Newsletter That Prints',
    read: '7 min',
    tag: 'Media'
  }, {
    n: '№002',
    title: 'Boring SaaS for One Industry',
    read: '11 min',
    tag: 'Software'
  }];
  return /*#__PURE__*/React.createElement("section", {
    style: {
      padding: '80px 48px',
      maxWidth: 1120,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-end',
      marginBottom: 32
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      marginBottom: 10
    }
  }, "The blueprint library"), /*#__PURE__*/React.createElement("h2", {
    style: {
      font: 'var(--type-h2)',
      fontSize: 32,
      color: 'var(--ink-900)',
      margin: 0
    }
  }, "Documentation a VP would save and annotate.")), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary"
  }, "View all 4 blueprints")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: 20
    }
  }, items.map(it => /*#__PURE__*/React.createElement(Card, {
    key: it.n,
    sheet: true,
    padding: "lg",
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16,
      minHeight: 200
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "oe-caps",
    style: {
      color: 'var(--drafting-blue)',
      fontWeight: 600
    }
  }, "Blueprint ", it.n), /*#__PURE__*/React.createElement(Badge, {
    tone: "neutral"
  }, it.tag)), /*#__PURE__*/React.createElement("h3", {
    style: {
      font: 'var(--type-h3)',
      fontSize: 21,
      color: 'var(--ink-900)',
      margin: 0,
      flex: 1
    }
  }, it.title), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "oe-caps"
  }, it.read, " \xB7 PDF"), /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 14,
      fontWeight: 600,
      color: 'var(--drafting-blue)'
    }
  }, "Download \u2192"))))));
}
function Capture() {
  const [email, setEmail] = React.useState('');
  const [done, setDone] = React.useState(false);
  return /*#__PURE__*/React.createElement("section", {
    style: {
      padding: '0 48px 96px',
      maxWidth: 1120,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      border: '1.5px solid var(--rule-strong)',
      borderRadius: 'var(--radius-md)',
      background: 'var(--paper-0)',
      padding: '56px 64px',
      display: 'grid',
      gridTemplateColumns: '1fr 0.8fr',
      gap: 56,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "oe-label",
    style: {
      marginBottom: 14
    }
  }, "The Operator Economy \xB7 Monday"), /*#__PURE__*/React.createElement("h2", {
    style: {
      font: 'var(--type-h2)',
      fontSize: 30,
      color: 'var(--ink-900)',
      margin: '0 0 12px'
    }
  }, "One business, fully sourced, every Monday."), /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-body)',
      color: 'var(--text-muted)',
      margin: 0,
      maxWidth: '44ch'
    }
  }, "Read like a research note: doc number, real figures, exact stack, named failure modes. No hype, no income promises.")), /*#__PURE__*/React.createElement("div", null, done ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "positive",
    dot: true
  }, "You're on the list"), /*#__PURE__*/React.createElement("p", {
    style: {
      font: 'var(--type-body)',
      color: 'var(--text-muted)',
      margin: '6px 0 0'
    }
  }, "Blueprint \u2116004 is on its way to your inbox.")) : /*#__PURE__*/React.createElement("form", {
    onSubmit: e => {
      e.preventDefault();
      if (email.includes('@')) setDone(true);
    },
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("label", {
    className: "oe-label"
  }, "Work email"), /*#__PURE__*/React.createElement(Input, {
    type: "email",
    placeholder: "you@company.com",
    value: email,
    onChange: e => setEmail(e.target.value)
  }), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    fullWidth: true,
    type: "submit"
  }, "Get the free blueprint"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps",
    style: {
      color: 'var(--text-faint)'
    }
  }, "4,100+ operators \xB7 unsubscribe anytime")))));
}
function Footer() {
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      background: 'var(--ink)',
      padding: '48px',
      color: 'var(--text-on-ink-muted)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1120,
      margin: '0 auto',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      flexWrap: 'wrap',
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      lineHeight: 1.1
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontWeight: 600,
      fontSize: 20,
      color: 'var(--paper)'
    }
  }, "The Operator Economy"), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps",
    style: {
      color: 'var(--sage-500)',
      marginTop: 6
    }
  }, "Build. Own. Operate.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 24
    }
  }, ['YouTube', 'Newsletter', 'LinkedIn', 'Blueprints'].map(l => /*#__PURE__*/React.createElement("a", {
    key: l,
    href: "#",
    style: {
      color: 'var(--text-on-ink-muted)',
      fontSize: 14,
      fontFamily: 'var(--font-sans)'
    }
  }, l))), /*#__PURE__*/React.createElement("span", {
    className: "oe-caps",
    style: {
      color: 'var(--text-on-ink-faint)'
    }
  }, "@operatoreconomy \xB7 theoperatoreconomy.com")));
}
function WebsiteApp() {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Header, null), /*#__PURE__*/React.createElement(Hero, null), /*#__PURE__*/React.createElement(EvidenceFeature, null), /*#__PURE__*/React.createElement(BlueprintLibrary, null), /*#__PURE__*/React.createElement(Capture, null), /*#__PURE__*/React.createElement(Footer, null));
}
window.WebsiteApp = WebsiteApp;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/WebsiteApp.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Annotation = __ds_scope.Annotation;

__ds_ns.CitationChip = __ds_scope.CitationChip;

__ds_ns.GapFigure = __ds_scope.GapFigure;

__ds_ns.Schematic = __ds_scope.Schematic;

__ds_ns.SchematicNode = __ds_scope.SchematicNode;

__ds_ns.SheetHeader = __ds_scope.SheetHeader;

__ds_ns.Stat = __ds_scope.Stat;

__ds_ns.TitleBlock = __ds_scope.TitleBlock;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.BarChart = __ds_scope.BarChart;

__ds_ns.DataTable = __ds_scope.DataTable;

})();
