'use client';

import { useEffect, useState } from 'react';

export function GuideToggle() {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    const sync = () => setEnabled(new URL(window.location.href).searchParams.get('guide') === '1');
    sync();
    window.addEventListener('popstate', sync);
    return () => window.removeEventListener('popstate', sync);
  }, []);

  useEffect(() => {
    document.getElementById('working-paper-shell')?.classList.toggle('guide-on', enabled);
  }, [enabled]);

  function toggle() {
    const next = !enabled;
    setEnabled(next);
    const url = new URL(window.location.href);
    if (next) url.searchParams.set('guide', '1');
    else url.searchParams.delete('guide');
    window.history.pushState(null, '', `${url.pathname}${url.search}${url.hash}`);
  }

  return (
    <>
      <button className="oe-guide-toggle" type="button" aria-pressed={enabled} onClick={toggle}>
        <i aria-hidden="true" />Guided walkthrough
      </button>
      <span className="oe-sr" aria-live="polite">Guided walkthrough {enabled ? 'on' : 'off'}</span>
    </>
  );
}
