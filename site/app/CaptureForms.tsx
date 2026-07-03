'use client';

import s from './page.module.css';

export function BlueprintForm() {
  return (
    <form
      className={s.captureCard}
      onSubmit={(e) => e.preventDefault()}
      action="#"
    >
      <div className={s.captureHead}>
        <span className={s.cardEpisode}>Operator Blueprint №001</span>
        <span className={s.tag}>Rev A</span>
      </div>
      <div className={s.captureName}>AI implementation as a service</div>
      <div className={s.captureMeta}>
        <div className={s.metaCell}>
          <div className={s.metaLabel}>Date</div>
          <div className={s.metaValue}>2026-07</div>
        </div>
        <div className={s.metaCell}>
          <div className={s.metaLabel}>Sources</div>
          <div className={s.metaValue}>8</div>
        </div>
        <div className={s.metaCell}>
          <div className={s.metaLabel}>Read</div>
          <div className={s.metaValue}>9 min</div>
        </div>
      </div>
      <div className={s.inputLabel}>Work email</div>
      <input
        type="email"
        placeholder="you@company.com"
        className={`${s.input} oe-input`}
        required
      />
      <button type="submit" className={s.submit}>
        Get Blueprint №001
      </button>
      <div className={s.captureFineprint}>
        PDF + every citation · straight to your inbox
      </div>
    </form>
  );
}

export function LedgerForm() {
  return (
    <form
      className={s.ledgerForm}
      onSubmit={(e) => e.preventDefault()}
      action="#"
    >
      <input
        type="email"
        placeholder="you@company.com"
        className={s.ledgerInput}
        required
      />
      <button type="submit" className={s.ledgerSubmit}>
        Get the Blueprints
      </button>
    </form>
  );
}
