# R35 avatar integration proposal and risk review

All four issued input hashes match. This is a structural proposal from the existing DOM, GSAP, and take plan; no generated take or integrated output was inspected. The pinned take plan retains its historical prepared/not-submitted status. Current generation authorization is owned by the root's separate record, not established by this worker packet.

## Least-invasive integration

Add one opaque, full-frame presenter sub-composition above the existing listing composition, starting at review 195.125 for exactly 5 seconds. Leave `listing.html`, its host duration, and `listing-narration` unchanged. The old final title can continue behind the opaque presenter without changing earlier listing behavior. Give the new host track 3 and place it after the listing host in the root DOM. Verify the result visually; track placement and an opacity assumption alone do not prove compositing.

Use an aligned, silent, 120-frame proxy only after the actual restored/native source offset has been measured. With that derived proxy, the source in is zero. If mounting an untrimmed provider source instead, substitute its measured source in and retain at least five seconds after that point. Do not assume zero insertion offset, trust the requested six-second provider duration, or duplicate the narration audio.

Proposed root insertion:

```html
<div id="r35-default-outcome-host"
     data-composition-id="r35-default-outcome"
     data-composition-src="compositions/presenter-default-outcome.html"
     data-start="195.125" data-duration="5" data-track-index="3"
     data-width="1280" data-height="720"></div>
```

Proposed new sub-composition (the media path is an intended derived artifact, not an existing source claim):

```html
<template>
<div id="r35-default-outcome-root"
     data-composition-id="r35-default-outcome" data-start="0" data-duration="5"
     data-width="1280" data-height="720"
     style="position:relative;width:1280px;height:720px;overflow:hidden;opacity:0">
  <style>
    .r35-default-outcome-fill{position:absolute;inset:0;background:#F5F0E6}
    .r35-default-outcome-viewport{position:absolute;inset:0;width:1280px;height:720px;overflow:hidden}
    .r35-default-outcome-framing{position:absolute;inset:0;width:1280px;height:720px;transform-origin:0 0}
    .r35-default-outcome-media{position:absolute;inset:0;width:1280px;height:720px;object-fit:cover}
  </style>
  <div class="r35-default-outcome-fill"></div>
  <div class="r35-default-outcome-viewport">
    <div id="r35-default-outcome-framing" class="r35-default-outcome-framing" data-layout-allow-overflow="">
      <video id="r35-default-outcome-speaking" class="clip r35-default-outcome-media"
             src="public/media/default-outcome-r35-aligned.mp4"
             data-start="0" data-duration="5" data-media-start="0" data-track-index="1"
             muted playsinline
             aria-label="Continuous V5 presenter delivering the default-outcome interpretation with original narration"></video>
    </div>
  </div>
  <script>
    window.__timelines=window.__timelines||{};
    const defaultOutcomeTimeline=gsap.timeline({paused:true});
    defaultOutcomeTimeline.set('#r35-default-outcome-root',{opacity:1},0);
    defaultOutcomeTimeline.set('#r35-default-outcome-framing',
      {scale:1.12,x:-76.8,y:-9,transformOrigin:'0 0'},0);
    defaultOutcomeTimeline.to('#r35-default-outcome-framing',
      {scale:1.42,x:-268.8,y:-22,duration:8/24,ease:'power2.inOut'},3.75);
    window.__timelines['r35-default-outcome']=defaultOutcomeTimeline;
  </script>
</div>
</template>
```

This follows the existing question template while adding the planned continuous push. Only the inner wrapper receives transform animation; HyperFrames retains ownership of timed media playback and visibility. Root title/composition identity may identify R35, but existing root timing and earlier GSAP values must remain unchanged. The overall end remains 200.125.

## Exact edit clocks

| Event | Review time | Root frame, 24 fps | New clip local time |
|---|---:|---:|---:|
| Last frame before presenter | 195.083333333 | 4682 | — |
| Presenter enters | 195.125 | 4683 | 0 |
| Push starts | 198.875 | 4773 | 3.75 |
| Push midpoint | 199.041666667 | 4777 | 3.916666667 |
| Push ends | 199.208333333 | 4781 | 4.083333333 |
| Last output frame | 200.083333333 | 4802 | 4.958333333 |
| Exclusive outpoint | 200.125 | 4803 | 5 |

The original listing audio remains at review 157.5–200.125 on track 100. The presenter picture selects master 198.125–203.125 under the existing minus-three clock map. The continuous picture must match the original words; its source trim and performance cannot be certified from the take plan. Do not use the older unused `section-out` value 42.791666667 inside `listing.html` to extend this edit: current root duration and approved outpoint are 200.125.

## Material risks and minimum QA

1. **Source alignment and mouth motion:** compare measured source insertion offset with the five-second original audio, then watch the complete restored phrase at normal speed. A correlation offset alone does not prove correct phonemes, natural mouth opening, or stable gaze. Confirm the final word and closed-mouth tail survive the measured trim.
2. **Layer leak or blank entry:** sample frames 4682, 4683, and 4684. The outgoing model should be followed directly by the new presenter, with no source-card text showing through and no undecoded first frame. Seek directly into the new clip as well as playing across its start.
3. **Push behavior:** sample 4772, 4773, 4777, and 4781 and watch the move with audio. Source performance must remain continuous; no clip restart, freeze, duplicated frame sequence, camera jump, or extra source cut should coincide with the push.
4. **Actual crop:** the proposed 1.12 and 1.42 crops remain conditional on the generated frame. Check forehead, chin, shoulders, visible hands during the wide part, and consistency with accepted V5 identity/neighboring takes. Do not force the numbers if the source framing differs.
5. **End and preserved prefix:** inspect frame 4802 and original audio at the end. Compare all inherited asset/sub-composition hashes with R34 and confirm every pre-existing start/duration/media-in value and root GSAP keyframe remains unchanged. Only the root insertion/identity and the new presenter files should change in this least-invasive treatment.

Run the current pinned HyperFrames strict check for the changed interval and a short original-audio review spanning the incoming cut, the full five-second phrase, and the outpoint. These checks establish integration and performance evidence; they do not supply owner acceptance.
