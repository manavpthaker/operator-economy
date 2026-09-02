(() => {
  "use strict";

  const audio = document.querySelector("#referenceAudio");
  const frame = document.querySelector("#motionFrame");
  const playButton = document.querySelector("#playButton");
  const restartButton = document.querySelector("#restartButton");
  const timeline = document.querySelector("#timeline");
  const timeOutput = document.querySelector("#timeOutput");
  const captionRail = document.querySelector("#captionRail");
  const captionText = document.querySelector("#captionText");
  const captionLive = document.querySelector("#captionLive");
  const phaseLabel = document.querySelector("#phaseLabel");
  const treatmentLabel = document.querySelector("#treatmentLabel");
  const textState = document.querySelector("#textState");
  const textHeadline = document.querySelector("#textHeadline");
  const textSupport = document.querySelector("#textSupport");
  const voiceState = document.querySelector("#voiceState");
  const traceBase = document.querySelector("#traceBase");
  const tracePlayed = document.querySelector("#tracePlayed");
  const playedTraceRect = document.querySelector("#playedTraceRect");
  const traceCursor = document.querySelector("#traceCursor");

  const copyByPhase = {
    human: {
      headline: "Go back to the guest.",
      support: "The relationship is the subject."
    },
    dependency: {
      headline: "First stay. Through the OTA.",
      support: "A useful introduction follows the current steel route."
    },
    permission: {
      headline: "Earn permission.",
      support: "No permission, no operator-controlled return path."
    },
    memory: {
      headline: "Remember what mattered.",
      support: "Context and a reason to return keep the relationship human."
    },
    return: {
      headline: "Next stay. Direct path.",
      support: "One oxide route changes the consequence."
    },
    fairness: {
      headline: "Keep the introduction.",
      support: "The platform can stay useful without owning every return."
    },
    thesis: {
      headline: "Don’t buy it twice.",
      support: "The model settles before the thesis is embedded."
    }
  };

  let specimenData = null;
  let envelopeData = null;
  let animationFrame = null;
  let previousCaption = "";

  function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainder = Math.max(0, seconds - minutes * 60);
    return `${String(minutes).padStart(2, "0")}:${remainder.toFixed(1).padStart(4, "0")}`;
  }

  function phaseAt(time) {
    if (!specimenData) return { id: "human", label: "Human context" };
    return specimenData.phases.find((phase) => time >= phase.start && time < phase.end)
      || specimenData.phases[specimenData.phases.length - 1];
  }

  function captionAt(time) {
    if (!specimenData) return null;
    return specimenData.captions.find((cue) => time >= cue.start && time < cue.end) || null;
  }

  function envelopeAt(time) {
    if (!envelopeData || !envelopeData.values.length) return 0;
    const index = Math.min(
      envelopeData.values.length - 1,
      Math.max(0, Math.floor((time * 1000) / envelopeData.extraction.windowMs))
    );
    return envelopeData.values[index] || 0;
  }

  function buildTrace(values) {
    if (!values.length) return "";
    return values.map((value, index) => {
      const x = (index / Math.max(1, values.length - 1)) * 1000;
      const y = 58 - value * 40;
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    }).join(" ");
  }

  function setPressed(buttons, activeButton) {
    buttons.forEach((button) => {
      button.setAttribute("aria-pressed", button === activeButton ? "true" : "false");
    });
  }

  function updateFrameLabel() {
    const treatment = frame.dataset.treatment === "text-led" ? "Text-led" : "Model-led";
    const format = frame.dataset.format === "portrait"
      ? "portrait"
      : frame.dataset.format === "square"
        ? "square"
        : "landscape";
    treatmentLabel.textContent = treatment;
    frame.setAttribute(
      "aria-label",
      `Boundary Ledger ${treatment.toLowerCase()} ${format} audio clip reference`
    );
  }

  function updateUI() {
    if (!specimenData || !envelopeData) return;

    const duration = specimenData.durationSeconds;
    const time = Math.min(duration, Number.isFinite(audio.currentTime) ? audio.currentTime : 0);
    const phase = phaseAt(time);
    const cue = captionAt(time);
    const embedded = frame.dataset.treatment === "text-led"
      && time >= specimenData.embeddedPhrase.start
      && time < specimenData.embeddedPhrase.end;
    const progress = Math.min(1, Math.max(0, time / duration));
    const x = progress * 1000;
    const amplitude = envelopeAt(time);
    const phaseCopy = copyByPhase[phase.id] || copyByPhase.human;

    frame.dataset.phase = phase.id;
    frame.dataset.embedded = embedded ? "true" : "false";
    phaseLabel.textContent = phase.label;
    textState.textContent = phase.label;
    textHeadline.textContent = phaseCopy.headline;
    textSupport.textContent = phaseCopy.support;
    voiceState.textContent = amplitude > 0.055 ? "Voice active" : "Hold";

    const visibleCaption = cue && !embedded ? cue.text : "";
    captionText.textContent = visibleCaption;
    captionRail.setAttribute("aria-hidden", embedded ? "true" : "false");

    if (cue && cue.text !== previousCaption) {
      captionLive.textContent = cue.text;
      previousCaption = cue.text;
    }

    timeline.value = String(time);
    playedTraceRect.setAttribute("width", x.toFixed(2));
    traceCursor.setAttribute("x1", x.toFixed(2));
    traceCursor.setAttribute("x2", x.toFixed(2));
    traceCursor.style.opacity = amplitude > 0.055 ? "1" : "0.42";
    timeOutput.textContent = `${formatTime(time)} / ${formatTime(duration)}`;
    playButton.textContent = audio.paused ? (time >= duration - 0.02 ? "Play again" : "Play excerpt") : "Pause";
  }

  function tick() {
    updateUI();
    if (!audio.paused && !audio.ended) {
      animationFrame = window.requestAnimationFrame(tick);
    } else {
      animationFrame = null;
    }
  }

  async function togglePlayback() {
    if (audio.ended || audio.currentTime >= (specimenData?.durationSeconds || 0) - 0.02) {
      audio.currentTime = 0;
    }

    if (audio.paused) {
      try {
        await audio.play();
        if (!animationFrame) animationFrame = window.requestAnimationFrame(tick);
      } catch (error) {
        console.error("Unable to play the reference audio.", error);
      }
    } else {
      audio.pause();
      updateUI();
    }
  }

  async function initialize() {
    try {
      const dataResponse = await fetch("./data/audio-return-loop.json");
      if (!dataResponse.ok) throw new Error(`Specimen data HTTP ${dataResponse.status}`);
      specimenData = await dataResponse.json();

      const envelopeUrl = new URL(specimenData.envelope, dataResponse.url);
      const envelopeResponse = await fetch(envelopeUrl);
      if (!envelopeResponse.ok) throw new Error(`Envelope data HTTP ${envelopeResponse.status}`);
      envelopeData = await envelopeResponse.json();

      timeline.max = String(specimenData.durationSeconds);
      const points = buildTrace(envelopeData.values);
      traceBase.setAttribute("points", points);
      tracePlayed.setAttribute("points", points);
      updateFrameLabel();
      updateUI();
    } catch (error) {
      console.error("Boundary Ledger specimen could not initialize.", error);
      playButton.disabled = true;
      restartButton.disabled = true;
      captionText.textContent = "The specimen data could not be loaded. Serve this package over HTTP.";
    }
  }

  playButton.addEventListener("click", togglePlayback);

  restartButton.addEventListener("click", () => {
    audio.currentTime = 0;
    updateUI();
  });

  timeline.addEventListener("input", () => {
    audio.currentTime = Number(timeline.value);
    updateUI();
  });

  audio.addEventListener("play", () => {
    if (!animationFrame) animationFrame = window.requestAnimationFrame(tick);
  });
  audio.addEventListener("pause", updateUI);
  audio.addEventListener("ended", updateUI);
  audio.addEventListener("loadedmetadata", updateUI);
  audio.addEventListener("seeked", updateUI);

  const treatmentButtons = [...document.querySelectorAll("button[data-treatment]")];
  treatmentButtons.forEach((button) => {
    button.addEventListener("click", () => {
      frame.dataset.treatment = button.dataset.treatment;
      setPressed(treatmentButtons, button);
      updateFrameLabel();
      updateUI();
    });
  });

  const formatButtons = [...document.querySelectorAll("button[data-format]")];
  formatButtons.forEach((button) => {
    button.addEventListener("click", () => {
      frame.dataset.format = button.dataset.format;
      setPressed(formatButtons, button);
      updateFrameLabel();
      updateUI();
    });
  });

  initialize();
})();
