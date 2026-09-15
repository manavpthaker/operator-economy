<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=720, height=1280" />
    <title>How I build without a dev team</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face { font-family: Archivo; src: url("assets/Archivo-variable.ttf") format("truetype"); font-weight: 100 900; font-display: block; }
      @font-face { font-family: Atkinson; src: url("assets/AtkinsonHyperlegibleNext-variable.ttf") format("truetype"); font-weight: 200 800; font-display: block; }
      @font-face { font-family: JBM; src: url("assets/JetBrainsMono-Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
      :root { --proof:#F3F6F5; --graphite:#202426; --source:#31584D; }
      * { box-sizing: border-box; }
      html, body { margin:0; width:720px; height:1280px; background:#111; overflow:hidden; }
      #root { position:relative; width:720px; height:1280px; overflow:hidden; background:#111; color:var(--graphite); font-family:Atkinson, sans-serif; }
      .scene { position:absolute; inset:0; overflow:hidden; background:#111; }

      #hook-video, #hook-matte { position:absolute; left:0; top:0; width:720px; height:1280px; object-fit:cover; }
      #hook-title { position:absolute; left:56px; top:64px; width:620px; margin:0; font-family:Archivo, sans-serif;
        font-size:80px; line-height:80px; font-weight:760; letter-spacing:-.045em; color:var(--graphite); }
      #hook-title span { display:block; }

      /* Captions ride over the footage in every shot. */
      .cap { position:absolute; left:56px; bottom:150px; max-width:608px; padding:10px 18px; border-radius:10px;
        background:rgba(32,36,38,.8); font-size:34px; line-height:44px; font-weight:600; }

      /* Phone filming the laptop: 941x1672 photo scaled to the frame; window mapped onto the screen. */
      .fit { position:absolute; left:0; top:0; width:941px; height:1672px; transform:scale(.76514); transform-origin:0 0; }
      .hand, .cam { position:absolute; inset:0; width:941px; height:1672px; }
      .photo { position:absolute; inset:0; width:941px; height:1672px; }
      .win { position:absolute; left:0; top:0; width:1000px; height:725px; transform-origin:0 0; border-radius:16px; overflow:hidden;
        box-shadow:0 30px 60px rgba(0,0,0,.35), 0 0 0 1px rgba(0,0,0,.12); filter:blur(.5px); }
      .glare { position:absolute; inset:0; background:linear-gradient(118deg, rgba(255,255,255,0) 30%, rgba(255,255,255,.08) 46%, rgba(255,255,255,0) 60%); }
      .vignette { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.3) 100%); }
      .grain { position:absolute; inset:-20px; opacity:.09; mix-blend-mode:overlay;
        background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }

      .bar { height:48px; display:flex; align-items:center; padding:0 20px; position:relative; font-size:19px; }
      .dot { width:14px; height:14px; border-radius:50%; margin-right:9px; }
      .bar .name { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); white-space:nowrap; }
      .light { background:#FFFFFF; color:#2B2F32; }
      .light .bar { background:#ECEEEF; border-bottom:1px solid #DADDDF; color:#6B7378; }
      .dark { background:#1B1E20; color:#E4E8E6; }
      .dark .bar { background:#26292C; border-bottom:1px solid #33373A; color:#9AA2A6; }
      .body { padding:34px 44px; }
      .mono { font-family:JBM, monospace; font-size:27px; line-height:40px; }
      .mono .dim { color:#8FA59A; } .mono .hash { color:#E8C57A; }
      .hl { background:rgba(120,170,140,.35); border-radius:6px; margin:0 -10px; padding:0 10px; }
      .md { font-size:27px; line-height:40px; }
      .md .meta { font-size:21px; color:#707A80; margin-bottom:10px; }
      .md h1 { font-family:Archivo, sans-serif; font-size:44px; line-height:50px; margin:0 0 18px; letter-spacing:-.02em; }
      .md h2 { font-family:Archivo, sans-serif; font-size:30px; margin:22px 0 8px; }
      .md p { margin:0 0 16px; }
      .md .blurred { filter:blur(6px); opacity:.8; }
      .md .term { margin-top:18px; padding:14px 18px; border-radius:10px; background:#1B1E20; color:#E4E8E6; font-family:JBM, monospace; font-size:24px; line-height:34px; }
      .md .term .hash { color:#E8C57A; }
      .swap { position:absolute; left:0; top:48px; right:0; bottom:0; background:#fff; }

      #question { position:absolute; left:56px; top:300px; margin:0; font-family:Archivo, sans-serif; font-size:62px; line-height:70px; font-weight:625; letter-spacing:-.045em; }
      #question .ql { display:block; white-space:nowrap; }
      #question .shift { color:var(--source); }
      .contact { position:absolute; left:56px; margin:0; white-space:nowrap; }
      #end { background:var(--proof); }
      #signature { top:760px; font-size:30px; font-weight:700; line-height:36px; letter-spacing:-.035em; font-family:Archivo, sans-serif; }
      .url { font-size:30px; font-weight:450; line-height:36px; }
      #website { top:822px; }
      #linkedin { top:870px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="how-i-build" data-start="0" data-width="720" data-height="1280" data-duration="{{DURATION}}">
      {{SCENES}}
      {{CAPTIONS}}
      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="36.058" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      // Map every 1000x725 laptop window onto the screen quad in the reference photo.
      const W = 1000, H = 725, QUAD = [[55, 470], [930, 527], [892, 1181], [25, 1100]];
      function homography(src, dst) {
        const A = [], b = [];
        for (let i = 0; i < 4; i++) { const [x, y] = src[i], [u, v] = dst[i];
          A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u); A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v); }
        for (let c = 0; c < 8; c++) { let p = c;
          for (let r = c + 1; r < 8; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
          [A[c], A[p]] = [A[p], A[c]]; [b[c], b[p]] = [b[p], b[c]];
          for (let r = 0; r < 8; r++) { if (r === c) continue; const f = A[r][c] / A[c][c];
            for (let k = c; k < 8; k++) A[r][k] -= f * A[c][k]; b[r] -= f * b[c]; } }
        return b.map((v, i) => v / A[i][i]);
      }
      const [a, bb, c, d, e, f, g, h] = homography([[0, 0], [W, 0], [W, H], [0, H]], QUAD);
      document.querySelectorAll(".win").forEach(el => { el.style.transform = `matrix3d(${a},${d},0,${g},${bb},${e},0,${h},0,0,1,0,${c},${f},0,1)`; });
      const project = (x, y) => { const w = g * x + h * y + 1; return [(a * x + bb * y + c) / w, (d * x + e * y + f) / w]; };
      const M = 12, clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
      // Camera framing that keeps the photo covering the frame: centre window point (lx, ly) at a scale.
      const frameAt = (lx, ly, scale, cy = 800) => { const [px, py] = project(lx, ly);
        return { scale, x: clamp(470 - scale * px, 941 - 941 * scale + M, -M), y: clamp(cy - scale * py, 1672 - 1672 * scale + M, -M) }; };
      document.querySelectorAll(".cam").forEach(el => { el.style.transformOrigin = "0 0"; });
{{MOTION}}
    </script>
  </body>
</html>
