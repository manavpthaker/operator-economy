# EP007-AVATAR-V5-VIEWER

Prepared review.html for the orchestrator to install. No server, original V4 file, provider, UI, or canonical state was changed.

HTML SHA-256: 33fc6c969a11c8f0f4958f0ea64c3d1358ec6e5e20e0b10b7b84439e2df4b8ca

The page keeps the existing dark, phone-responsive layout and native video controls. V5 is the first comparison, labeled a new candidate awaiting review. V4 is accepted for wider framing only; V3 remains the accepted delivery baseline. All three use the same EP007 opening. Playback of one pauses the others.

Route contract:
- /gestures.mp4 is attached only after status.json reports gestures_available === true.
- /wide.mp4 is attached only after wide_available === true.
- /previous.mp4 loads as the known baseline route.
- The optional /new.mp4 link appears only when edited_available === true.
- The page reports loading until the video emits canplay. A status-file existence flag alone never becomes “ready.”
- Refresh checks every 30 seconds and on demand. It does not reload a healthy attached player or interrupt its position; it retries failed loads.

The existing V4 server needs the gestures route and gestures_available status flag before V5 can appear. Missing/false gestures_available leaves it preparing. No poster is used, so the accepted still cannot be mistaken for a loaded V5 frame.

Validation: JavaScript syntax and a Node DOM-stub execution passed availability gating, ready-after-canplay, exclusive playback, preserving loaded media on refresh, load-error retry, and optional-link visibility. No browser, phone, actual media decoding, or playback test was performed. Root owns installation and live validation.

Read-only source fingerprints:
- V4 review.html: 9f54d95194c6db1069a75f51897a3edd71c978404b819599d7367314568d0376
- V4 review_server.py: 017f2525e15501d9c9d3186e2e18e06be2369cec38e4dd3cf9a04ebcbfb09c2a

The deliverable manifest uses lowercase ep007-avatar-v5-viewer for the existing schema; the assigned uppercase output folder and display ID are preserved.

