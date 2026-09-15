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

      /* App skins */
      .app { position:absolute; inset:0; }
      .chrome { height:74px; background:#DEE1E6; position:relative; }
      .chrome .tabs { position:absolute; left:110px; top:10px; height:32px; padding:0 22px; background:#fff; border-radius:10px 10px 0 0; font-size:17px; line-height:32px; color:#3C4043; white-space:nowrap; }
      .chrome .dots { position:absolute; left:18px; top:18px; display:flex; }
      .chrome .url { position:absolute; left:14px; right:14px; top:42px; height:28px; background:#fff; border-radius:14px; font-size:16px; line-height:28px; padding-left:18px; color:#5F6368; }
      .gdocs { background:#F9FBFD; }
      .gdocs .gbar { height:70px; background:#F9FBFD; position:relative; border-bottom:1px solid #E3E6EA; }
      .gdocs .gicon { position:absolute; left:18px; top:14px; width:28px; height:38px; background:#4285F4; border-radius:3px; }
      .gdocs .gicon::after { content:""; position:absolute; left:6px; right:6px; top:12px; height:3px; background:#fff; box-shadow:0 7px 0 #fff, 0 14px 0 #fff; }
      .gdocs .gtitle { position:absolute; left:60px; top:8px; font-size:22px; color:#1F1F1F; }
      .gdocs .gmenu { position:absolute; left:60px; top:40px; font-size:16px; color:#444; word-spacing:14px; }
      .gdocs .gshare { position:absolute; right:22px; top:18px; padding:6px 18px; border-radius:18px; background:#C2E7FF; font-size:17px; color:#001D35; }
      .gdocs .gtool { height:40px; margin:8px 16px; border-radius:20px; background:#EDF2FA; }
      .gdocs .page { position:absolute; left:110px; right:110px; top:210px; bottom:-40px; background:#fff; box-shadow:0 1px 3px rgba(60,64,67,.3); padding:46px 56px; font-family:Arial, Atkinson, sans-serif; color:#202124; font-size:24px; line-height:34px; }
      .gdocs .page h1 { font-family:Arial, Atkinson, sans-serif; font-size:40px; margin:0 0 4px; font-weight:700; }
      .gdocs .page .meta { font-size:18px; color:#5F6368; margin-bottom:16px; }
      .gdocs .page h2 { font-size:24px; margin:10px 0 4px; border-bottom:1px solid #DADCE0; padding-bottom:4px; }
      .gdocs .page .blurred { filter:blur(6px); opacity:.8; }
      .cursor { background:#181818; color:#CCCCCC; font-family:JBM, monospace; }
      .cursor .cbar { height:40px; background:#1F1F1F; border-bottom:1px solid #2B2B2B; font-size:15px; line-height:40px; text-align:center; color:#8B8B8B; }
      .cursor .side { position:absolute; left:0; top:40px; bottom:0; width:220px; background:#1F1F1F; border-right:1px solid #2B2B2B; padding:14px 12px; font-size:15px; line-height:26px; color:#9D9D9D; }
      .cursor .side .on { background:#37373D; color:#fff; border-radius:4px; padding:0 6px; margin:0 -6px; }
      .cursor .tab { position:absolute; left:220px; right:0; top:40px; height:40px; background:#181818; border-bottom:1px solid #2B2B2B; font-size:15px; line-height:40px; }
      .cursor .tab span { display:inline-block; padding:0 18px; background:#1F1F1F; border-top:2px solid #6A8DFF; color:#fff; }
      .cursor .code { position:absolute; left:220px; right:0; top:80px; bottom:0; padding:18px 0; font-size:21px; line-height:34px; }
      .cursor .ln { display:inline-block; width:56px; text-align:right; color:#5A5A5A; margin-right:22px; }
      .cursor .h { color:#6A8DFF; font-weight:700; } .cursor .b { color:#E6C07B; } .cursor .t { color:#D4D4D4; }
      .github { background:#fff; color:#1F2328; }
      .github .ghead { height:52px; background:#F6F8FA; border-bottom:1px solid #D1D9E0; font-size:19px; line-height:52px; padding-left:24px; }
      .github .ghead b { font-weight:600; }
      .github .box { margin:20px 24px; border:1px solid #D1D9E0; border-radius:8px; overflow:hidden; }
      .github .boxhead { height:48px; background:#F6F8FA; border-bottom:1px solid #D1D9E0; font-size:17px; line-height:48px; padding-left:16px; }
      .github .boxhead .pill { display:inline-block; padding:0 12px; line-height:30px; border-radius:6px; background:#fff; border:1px solid #D1D9E0; margin-right:6px; }
      .github .md { padding:26px 34px; font-size:23px; line-height:34px; }
      .github .md h1 { font-size:34px; margin:0 0 10px; padding-bottom:8px; border-bottom:1px solid #D1D9E0; font-family:Atkinson, sans-serif; font-weight:700; }
      .github .md h2 { font-size:27px; margin:14px 0 6px; padding-bottom:6px; border-bottom:1px solid #D1D9E0; font-family:Atkinson, sans-serif; }
      .github .md .meta { font-size:19px; color:#59636E; }
      .github .diff { font-family:JBM, monospace; font-size:18px; line-height:27px; }
      .github .diff div { padding:0 14px; white-space:pre; }
      .github .diff .del { background:#FFEBE9; color:#82071E; }
      .github .diff .ctx { color:#59636E; background:#F6F8FA; }
      .github .commits .row { padding:14px 18px; border-bottom:1px solid #D1D9E0; font-size:21px; }
      .github .commits .row .sha { float:right; font-family:JBM, monospace; font-size:17px; color:#59636E; }
      .github .commits .row.hl { background:#FFF8C5; }
      .warp { background:#16171B; color:#E6E6E6; font-family:JBM, monospace; }
      .warp .wbar { height:46px; background:#202227; border-bottom:1px solid #2C2F36; font-size:16px; line-height:46px; text-align:center; color:#9AA0AA; position:relative; }
      .warp .cc { padding:26px 34px; font-size:22px; line-height:36px; }
      .warp .cc .orange { color:#D97757; font-weight:700; }
      .warp .cc .box { border:2px solid #5B606B; border-radius:10px; padding:8px 16px; margin:16px 0; }
      .warp .cc .dim { color:#8B9099; }
      .warp .cc .green { color:#4FB477; }
      .warp .cc .hl { background:rgba(120,170,140,.35); border-radius:6px; padding:0 8px; margin:0 -8px; }
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
