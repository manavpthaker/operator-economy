<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=720, height=1280" />
    <title>Week 3 R14: could I sell this</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face { font-family: Archivo; src: url("assets/Archivo-variable.ttf") format("truetype"); font-weight: 100 900; font-display: block; }
      @font-face { font-family: Atkinson; src: url("assets/AtkinsonHyperlegibleNext-variable.ttf") format("truetype"); font-weight: 200 800; font-display: block; }
      @font-face { font-family: JBM; src: url("assets/JetBrainsMono-Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
      @font-face { font-family: JBM; src: url("assets/JetBrainsMono-Bold.ttf") format("truetype"); font-weight: 700; font-display: block; }
      :root { --graphite:#202426; }
      * { box-sizing: border-box; }
      html, body { margin:0; width:720px; height:1280px; background:#111; overflow:hidden; }
      #root { position:relative; width:720px; height:1280px; overflow:hidden; background:#111; font-family:Atkinson, sans-serif; }
      #base { position:absolute; inset:0; width:720px; height:1280px; object-fit:cover; z-index:0; }

      /* Hook: Counterproof proof ground, presenter inset, title behind the head; then cut to full frame. */
      #hook-ground { position:absolute; inset:0; background:#F3F6F5; z-index:1; }
      #hook-plate, #hook-matte { position:absolute; left:94px; top:333px; width:533px; height:947px; object-fit:cover; }
      #hook-plate { z-index:2; clip-path:inset(170px 0 0 0); }
      #hook-title { position:absolute; left:40px; top:226px; width:660px; margin:0; z-index:3; font-family:Archivo, sans-serif;
        font-size:116px; line-height:112px; font-weight:780; letter-spacing:-.05em; color:var(--graphite); }
      #hook-title span { display:block; }
      #hook-matte { z-index:4; -webkit-mask-image:linear-gradient(to bottom, transparent 0, transparent 66px, #000 90px); mask-image:linear-gradient(to bottom, transparent 0, transparent 66px, #000 90px); }

      .scene { position:absolute; inset:0; overflow:hidden; background:#111; z-index:5; }
      .fit { position:absolute; left:0; top:0; width:941px; height:1672px; transform:scale(.76514); transform-origin:0 0; }
      .hand, .cam { position:absolute; inset:0; width:941px; height:1672px; }
      .photo { position:absolute; inset:0; width:941px; height:1672px; }
      .win { position:absolute; left:0; top:0; width:1000px; height:725px; transform-origin:0 0; border-radius:16px; overflow:hidden;
        box-shadow:0 30px 60px rgba(0,0,0,.35), 0 0 0 1px rgba(0,0,0,.12); filter:blur(.45px); }
      .glare { position:absolute; inset:0; background:linear-gradient(118deg, rgba(255,255,255,0) 30%, rgba(255,255,255,.07) 46%, rgba(255,255,255,0) 60%); }
      .vignette { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.28) 100%); }
      .grain { position:absolute; inset:-20px; opacity:.09; mix-blend-mode:overlay;
        background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }
      .dot { display:inline-block; width:16px; height:16px; border-radius:50%; margin-right:10px; }

      /* Warp + Claude Code, same window as the full-06 insert, one run later. */
      .warp { background:#181a1f; color:#e6e6e6; font-family:JBM, monospace; }
      .warp .bar { height:52px; background:#22252b; border-bottom:1px solid #30333a; position:relative; padding:18px 22px; display:flex; }
      .warp .bar .name { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); font-size:21px; color:#aeb3bc; }
      .warp .body { padding:30px 38px; }
      .warp .head { font-size:22px; color:#8b9099; margin-bottom:22px; }
      .warp .head b { color:#d97757; }
      .warp .out { font-size:28px; line-height:42px; white-space:nowrap; }
      .warp .bullet { display:inline-block; width:16px; height:16px; border-radius:50%; background:#4fb477; margin-right:18px; vertical-align:2px; }
      .warp .bullet.bad { background:#e5534b; }
      .warp .arg { color:#c9ccd2; }
      .warp .res { color:#7f848d; padding-left:12px; }
      .warp .res.err { color:#f27a72; }
      .warp .elbow { display:inline-block; width:16px; height:20px; border-left:2px solid #7f848d; border-bottom:2px solid #7f848d; margin-right:18px; vertical-align:10px; }
      .warp .box { margin-top:34px; border:2px solid #5b606b; border-radius:12px; padding:16px 20px; font-size:28px; line-height:42px; white-space:nowrap; }
      .warp .gt { color:#8b9099; }
      .warp .caret { display:inline-block; width:17px; height:36px; background:#e6e6e6; vertical-align:-7px; margin-left:2px; }

      /* Finder icon view, moved by hand. */
      .finder { background:#fff; color:#1D1D1F; font-family:Atkinson, sans-serif; }
      .finder .fbar { height:56px; background:#ECECEE; border-bottom:1px solid #D6D6D8; position:relative; font-size:20px; line-height:56px; font-weight:700; padding-left:250px; }
      .finder .fbar .dots { position:absolute; left:20px; top:20px; display:flex; }
      .finder .fside { position:absolute; left:0; top:56px; bottom:0; width:210px; background:#EDEDF0; padding:18px 18px; font-size:18px; line-height:34px; color:#3A3A3C; }
      .finder .fside b { font-size:14px; color:#98989D; letter-spacing:.04em; font-weight:600; }
      .finder .grid { position:absolute; left:210px; right:0; top:56px; bottom:0; }
      .item { position:absolute; width:170px; text-align:center; font-size:19px; }
      .item .lbl { margin-top:10px; padding:2px 8px; border-radius:6px; display:inline-block; }
      .folder { width:120px; height:92px; margin:0 auto; position:relative; }
      .folder::before { content:""; position:absolute; left:0; top:0; width:50px; height:20px; border-radius:8px 8px 0 0; background:#5DA9E9; }
      .folder::after { content:""; position:absolute; left:0; top:12px; width:120px; height:80px; border-radius:6px 10px 10px 10px; background:linear-gradient(#7CC0F5, #4E9BE0); }
      .file { width:80px; height:100px; margin:0 auto; background:#fff; border:2px solid #D5D5D8; border-radius:4px 22px 4px 4px; position:relative; }
      .file i { position:absolute; left:16px; right:16px; height:4px; background:#D5D5D8; }
      .file.pdf::after { content:"PDF"; position:absolute; left:10px; bottom:10px; font-size:14px; font-weight:700; color:#fff; background:#E5484D; padding:1px 6px; border-radius:3px; }
      .ghost { position:absolute; opacity:0; width:170px; text-align:center; }
      .ptr { position:absolute; left:0; top:0; width:34px; height:50px; z-index:5; }

      /* Cursor with the research report open. */
      .cursor { background:#181818; color:#CCCCCC; font-family:JBM, monospace; }
      .cursor .cbar { height:44px; background:#1F1F1F; border-bottom:1px solid #2B2B2B; font-size:17px; line-height:44px; text-align:center; color:#8B8B8B; }
      .cursor .side { position:absolute; left:0; top:44px; bottom:0; width:240px; background:#1F1F1F; border-right:1px solid #2B2B2B; padding:14px 14px; font-size:16px; line-height:28px; color:#9D9D9D; white-space:nowrap; }
      .cursor .side .on { background:#37373D; color:#fff; border-radius:4px; padding:0 6px; }
      .cursor .tab { position:absolute; left:240px; right:0; top:44px; height:44px; background:#181818; border-bottom:1px solid #2B2B2B; font-size:16px; line-height:44px; }
      .cursor .tab span { display:inline-block; padding:0 18px; background:#1F1F1F; border-top:2px solid #6A8DFF; color:#fff; }
      .cursor .code { position:absolute; left:240px; right:0; top:88px; bottom:0; overflow:hidden; }
      .cursor .scroll { padding:14px 16px 0 0; font-size:18px; line-height:29px; }
      .cursor .cl { white-space:pre-wrap; padding-left:74px; text-indent:-74px; border-radius:4px; color:#D4D4D4; }
      .cursor .cl .c { color:#6A9955; } .cursor .cl .s { color:#CE9178; } .cursor .cl .k { color:#C586C0; } .cursor .cl .n { color:#B5CEA8; } .cursor .cl .u { color:#4FC1FF; }
      .cursor .ln { display:inline-block; width:52px; text-align:right; color:#5A5A5A; margin-right:22px; text-indent:0; }
      .cursor .h { color:#6A8DFF; font-weight:700; } .cursor .t { color:#D4D4D4; } .cursor .bl { color:#D4D4D4; filter:blur(3.5px); }

      .warp .ok { color:#4fb477; } .warp .dim { color:#7f848d; } .warp .key { display:inline-block; width:150px; color:#8b9099; }
      .warp .opt { display:inline-block; padding:0 12px; margin-right:6px; border-radius:8px; color:#aeb3bc; }
      .finder .grid .item { width:190px; }

      .cap { position:absolute; left:56px; bottom:150px; max-width:608px; padding:10px 18px; border-radius:10px; z-index:20;
        background:rgba(32,36,38,.8); color:#fff; font-size:34px; line-height:44px; font-weight:600; }
    </style>
  </head>
  <body>
{{BODY}}
    <script>
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
      const frameAt = (lx, ly, scale, cy = 800) => { const [px, py] = project(lx, ly);
        return { scale, x: clamp(470 - scale * px, 941 - 941 * scale + M, -M), y: clamp(cy - scale * py, 1672 - 1672 * scale + M, -M) }; };
      document.querySelectorAll(".cam").forEach(el => { el.style.transformOrigin = "0 0"; });

{{MOTION}}
    </script>
  </body>
</html>
