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
      :root { --proof:#F3F6F5; --graphite:#202426; --sage:#A9C1B2; --source:#31584D; --carbon:#2457D6; --veil:#DCE4E2; --steel:#5F6E75; --muted:#9DADB5; }
      * { box-sizing: border-box; }
      html, body { margin:0; width:720px; height:1280px; background:var(--proof); overflow:hidden; }
      #root { position:relative; width:720px; height:1280px; overflow:hidden; background:var(--proof); color:var(--graphite); font-family:Atkinson, sans-serif; }
      .scene { position:absolute; inset:0; overflow:hidden; background:var(--proof); }

      #hook-video, #hook-matte { position:absolute; left:0; top:0; width:720px; height:1280px; object-fit:cover; }
      #hook-title { position:absolute; left:56px; top:64px; width:620px; margin:0; font-family:Archivo, sans-serif;
        font-size:80px; line-height:80px; font-weight:760; letter-spacing:-.045em; color:var(--graphite); }
      #hook-title span { display:block; }

      .cap { position:absolute; left:56px; font-weight:600; }
      .cap-over { bottom:112px; max-width:608px; padding:10px 18px; border-radius:10px; background:rgba(32,36,38,.78); font-size:34px; line-height:44px; }
      .cap-under { top:980px; width:620px; font-size:38px; line-height:50px; }

      .step-no { position:absolute; left:56px; top:218px; font-size:30px; font-weight:700; color:var(--carbon); }
      .step-head { position:absolute; left:56px; top:256px; margin:0; font-family:Archivo, sans-serif; font-size:66px; line-height:70px; font-weight:740; letter-spacing:-.04em; }
      .screen { position:absolute; left:56px; top:400px; width:820px; background:#fff; border:1px solid var(--veil); border-right:0;
        border-radius:16px 0 0 16px; box-shadow:0 24px 60px rgba(32,36,38,.10); overflow:hidden; }
      .terminal { height:430px; background:#1B1E20; border-color:#1B1E20; padding:40px 36px; font-family:JBM, monospace; font-size:21px; line-height:30px; color:#E4E8E6; }
      .terminal .prompt { color:#8FA59A; margin-bottom:22px; }
      .terminal .row { padding:10px 12px; margin:0 -12px 6px; border-radius:6px; white-space:nowrap; }
      .terminal .hash { color:#E8C57A; }
      .terminal .date { color:#8FA59A; }
      .doc { height:440px; padding:44px 46px; font-size:25px; line-height:37px; color:#2c3134; }
      .doc h4 { margin:0 0 8px; font-family:Archivo, sans-serif; font-size:21px; font-weight:600; color:var(--steel); }
      .doc h3 { margin:0 0 24px; font-family:Archivo, sans-serif; font-size:40px; line-height:44px; font-weight:720; letter-spacing:-.03em; color:var(--graphite); max-width:620px; }
      .doc h5 { margin:0 0 8px; font-family:Archivo, sans-serif; font-size:24px; font-weight:680; color:var(--graphite); }
      .doc p { margin:0 0 18px; max-width:610px; }
      .doc b { font-weight:700; }
      .doc .commit { margin-top:18px; max-width:620px; padding:14px 18px; border-radius:10px; background:#1B1E20; color:#E4E8E6; font-family:JBM, monospace; font-size:20px; line-height:28px; }
      .doc .commit .hash { color:#E8C57A; }
      .tag { position:absolute; left:56px; top:862px; font-size:22px; line-height:28px; font-weight:600; color:var(--source); }

      .turn-lead { position:absolute; left:56px; top:120px; width:608px; margin:0; font-family:Archivo, sans-serif; font-size:50px; line-height:56px; font-weight:700; letter-spacing:-.035em; }
      .sage { position:absolute; left:0; top:352px; width:392px; height:640px; background:var(--sage); overflow:hidden; }
      .sage p { position:absolute; left:56px; top:48px; width:300px; margin:0; font-family:Archivo, sans-serif; font-size:44px; line-height:50px; font-weight:720; letter-spacing:-.035em; color:var(--source); }
      .sameday { top:392px; height:420px; }
      .resume h3 { font-size:44px; margin-bottom:6px; }
      .resume h4 { margin-bottom:26px; }
      .resume .role { margin-bottom:10px; }
      .resume .blurred { filter: blur(5px); opacity:.8; }
      .callback { left:420px; top:392px; width:620px; height:300px; }
      .callback h3 { font-size:34px; line-height:40px; max-width:260px; }
      .shot { top:392px; width:620px; height:560px; }
      .shot img { display:block; width:1000px; margin:-18px 0 0 -40px; }
      #t-tag { top:830px; }

      #question { position:absolute; left:56px; top:300px; margin:0; font-family:Archivo, sans-serif; font-size:62px; line-height:70px; font-weight:625; letter-spacing:-.045em; }
      #question .ql { display:block; white-space:nowrap; }
      #question .shift { color:var(--source); }
      .contact { position:absolute; left:56px; margin:0; white-space:nowrap; }
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
{{MOTION}}
    </script>
  </body>
</html>
