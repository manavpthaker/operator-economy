import {useEffect, useRef} from 'react';
import {continueRender, delayRender} from 'remotion';

// Side-effect import so webpack bundles the @import URLs (Fontshare +
// Google Fonts). Every module in ./oe/ ultimately depends on this.
import './globals.css';

/**
 * Await document.fonts.ready during render so Boska/Zodiak/Supreme/
 * Fragment Mono are actually loaded before Remotion captures frames.
 * Fontshare returns 502 occasionally; we time out at 8s and continue
 * with system fallbacks rather than block the whole render.
 */
export function useEnsureFontsLoaded() {
  const handle = useRef<number | null>(null);
  if (handle.current === null) {
    handle.current = delayRender('operator-economy fonts', {timeoutInMilliseconds: 12_000});
  }

  useEffect(() => {
    let cancelled = false;
    const timeout = window.setTimeout(() => {
      if (!cancelled && handle.current !== null) {
        continueRender(handle.current);
        handle.current = -1;
      }
    }, 8_000);

    (document as any).fonts?.ready
      ?.then(() => {
        window.clearTimeout(timeout);
        if (!cancelled && handle.current !== null && handle.current >= 0) {
          continueRender(handle.current);
          handle.current = -1;
        }
      })
      .catch(() => {
        window.clearTimeout(timeout);
        if (!cancelled && handle.current !== null && handle.current >= 0) {
          continueRender(handle.current);
          handle.current = -1;
        }
      });

    return () => {
      cancelled = true;
      window.clearTimeout(timeout);
    };
  }, []);
}
