<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=720, height=1280" />
    <title>Week 2 full-07: worth automating</title>
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

      /* Hook: the presenter steps back so the title can sit behind the head. */
      #hook-fill { position:absolute; left:-40px; top:-40px; width:800px; height:1360px; object-fit:cover; filter:blur(26px) brightness(1.04); z-index:1; }
      #hook-plate, #hook-matte { position:absolute; left:72px; top:256px; width:576px; height:1024px; object-fit:cover; }
      #hook-plate { z-index:2; -webkit-mask-image:linear-gradient(to right, transparent 0, #000 60px, #000 516px, transparent 576px), linear-gradient(to bottom, transparent 0, #000 90px);
        -webkit-mask-composite: source-in; mask-image:linear-gradient(to right, transparent 0, #000 60px, #000 516px, transparent 576px), linear-gradient(to bottom, transparent 0, #000 90px); mask-composite:intersect; }
      #hook-title { position:absolute; left:40px; top:92px; width:660px; margin:0; z-index:3; font-family:Archivo, sans-serif;
        font-size:116px; line-height:112px; font-weight:780; letter-spacing:-.05em; color:var(--graphite); }
      #hook-title span { display:block; }
      #hook-matte { z-index:4; }

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

      .cap { position:absolute; left:56px; bottom:150px; max-width:608px; padding:10px 18px; border-radius:10px; z-index:20;
        background:rgba(32,36,38,.8); color:#fff; font-size:34px; line-height:44px; font-weight:600; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="week2-full07" data-start="0" data-width="720" data-height="1280" data-duration="{{DURATION}}">
      <video id="base" class="clip" src="assets/base.mp4" data-start="0" data-duration="{{DURATION}}" data-track-index="0" muted playsinline></video>
      <video id="hook-fill" class="clip" src="assets/hook-fill.mp4" data-start="0" data-duration="{{HOOK_END}}" data-track-index="1" muted playsinline></video>
      <video id="hook-plate" class="clip" src="assets/hook.mp4" data-start="0" data-duration="{{HOOK_END}}" data-track-index="2" muted playsinline></video>
      <div id="hook-title" class="clip" data-start="0" data-duration="{{HOOK_END}}" data-track-index="3" data-layout-allow-overlap><span>Worth</span><span>automating?</span></div>
      <video id="hook-matte" class="clip" src="assets/hook-matte.webm" data-start="0" data-duration="{{HOOK_END}}" data-track-index="4" muted playsinline></video>

      <section id="fix" class="clip scene" data-start="{{FIX_START}}" data-duration="{{FIX_DUR}}" data-track-index="5">
        <div class="fit"><div class="hand"><div class="cam"><img class="photo" src="assets/macbook-reference.png" alt="" />
          <div class="win warp"><div class="bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="name">claude — ~/Example</span></div>
            <div class="body"><div class="head"><b>Claude Code</b> &nbsp;·&nbsp; ~/Example</div>
              <div class="out" data-layout-allow-overlap>
                <div><span class="bullet"></span><b>Bash</b><span class="arg">(mv notes.txt Sources/)</span></div>
                <div class="res"><span class="elbow"></span>moved</div>
                <div id="fx-r2"><span class="bullet bad"></span><b>Bash</b><span class="arg">(mv *.png Assets/)</span></div>
                <div id="fx-r2b" class="res err"><span class="elbow"></span>mv: Assets/: No such file or directory</div>
              </div>
              <div class="box" data-layout-allow-overlap><span class="gt">&gt; </span><span id="fx-typed"></span><span id="fx-caret" class="caret"></span></div>
            </div></div>
          <div class="glare"></div></div></div></div><div class="vignette"></div><div class="grain"></div>
      </section>

      <section id="manual" class="clip scene" data-start="{{MANUAL_START}}" data-duration="{{MANUAL_DUR}}" data-track-index="5">
        <div class="fit"><div class="hand"><div class="cam"><img class="photo" src="assets/macbook-reference.png" alt="" />
          <div class="win finder"><div class="fbar"><div class="dots"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></div>Example project</div>
            <div class="fside"><b>FAVORITES</b><br/>Recents<br/>Applications<br/>Desktop<br/>Documents<br/>Downloads<br/><b>LOCATIONS</b><br/>iCloud Drive</div>
            <div class="grid" data-layout-allow-overlap>
              <div class="item" id="m-sources" style="left:60px;top:70px"><div class="folder"></div><div class="lbl">Sources</div></div>
              <div class="item" id="m-images" style="left:290px;top:70px"><div class="folder"></div><div class="lbl">Images</div></div>
              <div class="item" id="m-archive" style="left:520px;top:70px"><div class="folder"></div><div class="lbl">Archive</div></div>
              <div class="item" id="m-brief" style="left:60px;top:330px"><div class="file pdf"><i style="top:24px"></i><i style="top:38px"></i><i style="top:52px"></i></div><div class="lbl">brief-v2.pdf</div></div>
              <div class="item" id="m-notes" style="left:290px;top:330px"><div class="file"><i style="top:24px"></i><i style="top:38px"></i><i style="top:52px"></i><i style="top:66px"></i></div><div class="lbl">call-notes.txt</div></div>
              <div class="item" id="m-shot" style="left:520px;top:330px"><div class="file"><i style="top:24px;height:40px;background:#CFE3F5"></i></div><div class="lbl">hero.png</div></div>
              <svg class="ptr" id="m-ptr" viewBox="0 0 34 50"><path d="M2 2 L2 40 L12 31 L19 47 L26 44 L19 28 L32 28 Z" fill="#000" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>
            </div></div>
          <div class="glare"></div></div></div></div><div class="vignette"></div><div class="grain"></div>
      </section>

      {{CAPTIONS}}
    </div>
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

      const text = "I renamed Assets to Images, update the rule";
      const typed = document.getElementById("fx-typed");
      typed.innerHTML = [...text].map(ch => `<span class="ch" style="display:none">${ch === " " ? "&nbsp;" : ch}</span>`).join("");

      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["week2-full07"] = tl;

      // Hook title rises in behind the head.
      tl.fromTo("#hook-title span", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .45, stagger: .12, ease: "power3.out" }, .15);

      // Fix: the run fails on the renamed folder, then the request to update the rule.
      const F0 = {{FIX_START}}, FD = {{FIX_DUR}};
      tl.set("#fix .cam", frameAt(330, 250, 1.5, 760), F0);
      tl.fromTo("#fx-r2", { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: .16 }, F0 + .05);
      tl.fromTo("#fx-r2b", { opacity: 0 }, { opacity: 1, duration: .12 }, F0 + .3);
      tl.to("#fix .cam", { ...frameAt(420, 330, 1.3, 800), duration: 1.2, ease: "power2.inOut" }, F0 + 1.0);
      tl.to("#fix .ch", { display: "inline", duration: .001, stagger: .03, ease: "none" }, F0 + 1.2);
      tl.fromTo("#fix .hand", { x: 0, y: 0, rotation: 0 }, { x: -6, y: 5, rotation: .3, duration: FD / 2, ease: "sine.inOut" }, F0);
      tl.to("#fix .hand", { x: 5, y: -3, rotation: -.2, duration: FD / 2, ease: "sine.inOut" }, F0 + FD / 2);

      // Manual: drag two files into folders by hand.
      const M0 = {{MANUAL_START}}, MD = {{MANUAL_DUR}};
      const at = (id, dx = 95, dy = 55) => { const el = document.getElementById(id); return { x: parseFloat(el.style.left) + dx, y: parseFloat(el.style.top) + dy }; };
      const sel = (id, t) => tl.to(`#${id} .lbl`, { backgroundColor: "#0A64D8", color: "#fff", duration: .05 }, t);
      const drop = (file, folder, t0) => {
        const f = at(file), to = at(folder);
        tl.to("#m-ptr", { ...f, duration: .55, ease: "power2.inOut" }, t0);
        sel(file, t0 + .6);
        tl.to(`#${file}`, { x: to.x - f.x, y: to.y - f.y, scale: .7, opacity: .75, duration: .9, ease: "power1.inOut" }, t0 + .7);
        tl.to("#m-ptr", { ...to, duration: .9, ease: "power1.inOut" }, t0 + .7);
        tl.to(`#${folder} .folder`, { scale: 1.08, filter: "brightness(1.1)", duration: .12 }, t0 + 1.45);
        tl.to(`#${file}`, { opacity: 0, duration: .08 }, t0 + 1.62);
        tl.to(`#${folder} .folder`, { scale: 1, filter: "brightness(1)", duration: .18 }, t0 + 1.7);
      };
      tl.set("#m-ptr", { x: 700, y: 520 }, M0);
      tl.set("#manual .cam", frameAt(500, 330, 1.12, 780), M0);
      drop("m-brief", "m-archive", M0 + .35);
      drop("m-notes", "m-sources", M0 + 2.55);
      tl.to("#manual .cam", { ...frameAt(460, 300, 1.26, 780), duration: MD, ease: "sine.inOut" }, M0);
      tl.fromTo("#manual .hand", { x: 0, y: 0, rotation: 0 }, { x: 7, y: -5, rotation: -.3, duration: MD / 2, ease: "sine.inOut" }, M0);
      tl.to("#manual .hand", { x: -4, y: 4, rotation: .2, duration: MD / 2, ease: "sine.inOut" }, M0 + MD / 2);

      {{CAPTION_MOTION}}
    </script>
  </body>
</html>
