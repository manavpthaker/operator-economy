# Blueprint Cinema director packet: sequence-thesis-02

You are the senior motion-design director for one bounded Operator Economy sequence. Author precise scene direction only. Do not write renderer code, generate media, alter the narration, change claims, or edit canonical episode state.

Your result must make the viewer understand a causal relationship against the exact locked voiceover. This is not a request for a topical illustration, a slide, a node-map camera move, or generic "Vox-style" decoration. The transferable editorial-explainer behaviors are deliberate composition, restrained annotation, progressive disclosure, parameter-to-consequence evidence motion, and motivated continuity.

## Output contract

Author exactly one sequence object for `schemas/scene-directions.schema.json` and save it only to the path assigned by the orchestrator. It must contain shot-by-shot pixel geometry, exact text, word-cued motion, evidence choreography, and transition continuity. Return no approvals and make no canonical-state changes.

Episode: `EP006-direct-booking-recovery`
Sequence: `sequence-thesis-02`
Previous sequence: `sequence-thesis-01`
Next sequence: `sequence-thesis-03`
Time range: `67.057-106.132` seconds
Locked word range: `140-216`
Exact VO: `At a ten-to-forty-room hotel, no one person owns that whole journey. One person updates Google. Someone else handles the website. The front desk answers the phone when it can. Guest information sits in the booking system. And follow-up happens... if somebody remembers. It's less a system than a GROUP PROJECT where everyone assumes someone else did their part. So direct booking isn't really a website feature. It's what happens when all of those small jobs work together.`

Hash pins:
```json
{
  "input_lock": "e99b847c5b5a767d74ad4208738374ac191da3d9d4c3e3654098a6c08e725691",
  "episode_engine": "73b22204a8a19a9a71d420d6aef69218f717cdab804486175f2929922d4af543",
  "world": "512c8e4ac1b2648ca9d338a8a25ab2e943fc0890d71250a0c975972c2827823e",
  "visual_plan": "1ea1182ec9240d29914666b5b6f8eafc56bd827fd1401f5118c89f4226397407",
  "asset_tickets": "1e978e7d1c309852ac7d9ca9ad54c76ca30b856b9584f58bd97d03626b0ebd9c"
}
```

## Non-negotiable direction rules

1. Design the audience's frame, not a view of the master world model. Never show the complete node map by default.
2. Express one visual sentence at a time: subject -> relationship or business verb -> object -> visible consequence.
3. Use two to five meaningful objects per composition unless a real evidence source legitimately fills the frame.
4. Preserve recurring object identity and screen direction. State what is inherited, introduced, retired, and handed to the next sequence.
5. Give every shot exact 1920x1080 pixel bounds for every layer at its start and end. Do not use vague placement words such as "somewhere," "roughly," or "nearby."
6. Tie every motion beat to an exact locked word index and timestamp. Motion must communicate an operation, state change, transfer, comparison, failure, or consequence.
7. Specify every visible text string exactly, including capitalization, line count, size, alignment, and timed substring emphasis. Text labels or proves; it does not repeat the VO.
8. The default transition is a cut. Use a designed transition only when it preserves an object, extracts evidence into the system, follows a handoff, reveals accumulated state, or shows a route failing or changing.
9. Evidence must follow: source appears -> relevant element highlighted -> value extracted -> value attached to the system -> behavior changes. Never synthesize evidence or branded interfaces.
10. AI environmental plates may establish non-evidentiary reality only. Documents, figures, interfaces, prices, and proof must come from an authorized source or ticket and be composited accurately.
11. Keep the OE frame to Ink + Paper or Schematic Navy + one accent. No gradients, glass, decorative glow, generic icon clouds, transition-pack flourishes, or motion merely for energy.
12. The first frame, action frame, and exit frame must each be understandable without a production caption or mini-map.

## Required frame contract

```json
{
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "safe_area_px": {
    "top": 65,
    "right": 134,
    "bottom": 65,
    "left": 134
  },
  "type_scale_px": {
    "headline_min": 72,
    "headline_max": 108,
    "critical_number_min": 140,
    "critical_number_max": 240,
    "label_min": 44,
    "label_max": 60,
    "source_min": 26,
    "source_max": 34
  },
  "default_transition": "cut"
}
```

## Exact word timing

| Index | In | Out | Spoken word |
|---:|---:|---:|---|
| 140 | 67.802 | 67.855 | At |
| 141 | 67.895 | 67.935 | a |
| 142 | 68.035 | 69.215 | ten-to-forty-room |
| 143 | 69.295 | 70.255 | hotel, |
| 144 | 70.335 | 70.495 | no |
| 145 | 70.615 | 70.975 | one |
| 146 | 71.044 | 71.455 | person |
| 147 | 71.551 | 71.935 | owns |
| 148 | 71.983 | 72.175 | that |
| 149 | 72.228 | 72.495 | whole |
| 150 | 72.555 | 73.055 | journey. |
| 151 | 73.315 | 74.095 | One |
| 152 | 74.152 | 74.495 | person |
| 153 | 74.545 | 74.895 | updates |
| 154 | 74.964 | 75.455 | Google. |
| 155 | 75.555 | 76.255 | Someone |
| 156 | 76.319 | 76.575 | else |
| 157 | 76.625 | 76.975 | handles |
| 158 | 77.015 | 77.135 | the |
| 159 | 77.205 | 77.935 | website. |
| 160 | 78.075 | 78.495 | The |
| 161 | 78.548 | 78.815 | front |
| 162 | 78.911 | 79.295 | desk |
| 163 | 79.355 | 79.775 | answers |
| 164 | 79.795 | 79.855 | the |
| 165 | 79.908 | 80.175 | phone |
| 166 | 80.223 | 80.415 | when |
| 167 | 80.468 | 80.575 | it |
| 168 | 80.675 | 81.575 | can. |
| 169 | 81.675 | 82.175 | Guest |
| 170 | 82.235 | 82.895 | information |
| 171 | 82.975 | 83.295 | sits |
| 172 | 83.322 | 83.375 | in |
| 173 | 83.395 | 83.455 | the |
| 174 | 83.505 | 83.855 | booking |
| 175 | 83.924 | 84.415 | system. |
| 176 | 85.342 | 85.382 | And |
| 177 | 85.439 | 85.942 | follow-up |
| 178 | 86.032 | 87.222 | happens... |
| 179 | 87.302 | 87.462 | if |
| 180 | 87.524 | 88.022 | somebody |
| 181 | 88.094 | 88.822 | remembers. |
| 182 | 90.089 | 90.182 | It's |
| 183 | 90.262 | 90.582 | less |
| 184 | 90.662 | 90.742 | a |
| 185 | 90.822 | 91.302 | system |
| 186 | 91.366 | 91.622 | than |
| 187 | 91.662 | 91.702 | a |
| 188 | 91.782 | 92.182 | GROUP |
| 189 | 92.272 | 92.902 | PROJECT |
| 190 | 92.955 | 93.222 | where |
| 191 | 93.266 | 93.622 | everyone |
| 192 | 93.712 | 94.342 | assumes |
| 193 | 94.402 | 94.822 | someone |
| 194 | 94.886 | 95.142 | else |
| 195 | 95.202 | 95.382 | did |
| 196 | 95.409 | 95.542 | their |
| 197 | 95.638 | 96.182 | part. |
| 198 | 97.818 | 97.871 | So |
| 199 | 97.928 | 98.271 | direct |
| 200 | 98.331 | 98.751 | booking |
| 201 | 98.811 | 99.151 | isn't |
| 202 | 99.208 | 99.551 | really |
| 203 | 99.591 | 99.631 | a |
| 204 | 99.691 | 100.111 | website |
| 205 | 100.171 | 100.671 | feature. |
| 206 | 100.911 | 101.471 | It's |
| 207 | 101.503 | 101.631 | what |
| 208 | 101.691 | 102.111 | happens |
| 209 | 102.159 | 102.351 | when |
| 210 | 102.451 | 102.751 | all |
| 211 | 102.778 | 102.831 | of |
| 212 | 102.871 | 103.071 | those |
| 213 | 103.151 | 103.551 | small |
| 214 | 103.663 | 104.111 | jobs |
| 215 | 104.191 | 104.511 | work |
| 216 | 104.573 | 105.751 | together. |

## Approved visual-plan units

These state what must be communicated; they do not prescribe the finished layout.

```json
[
  {
    "action": "Inspect fragmented ownership across discovery, website, phone, booking, and post-stay work.",
    "asset_ticket_ids": [],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-system",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator",
      "recovered-loop-state"
    ],
    "evidence_ids": [],
    "focus": [
      "independent-hotel-operator"
    ],
    "id": "unit-011",
    "in": 67.057,
    "mode": "system",
    "motion_verb": "inspect",
    "narration_anchor": {
      "quote": "At a ten-to-forty-room hotel, no one person owns that whole journey. One person updates Google.",
      "word_end": 154,
      "word_start": 140
    },
    "narrative_state": "current_machine",
    "out": 75.505,
    "sequence_id": "sequence-thesis-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "independent-hotel-operator",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "independent-hotel-operator",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Route guest work between disconnected handoffs and expose the absence of one accountable owner.",
    "asset_ticket_ids": [],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-system",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator"
    ],
    "evidence_ids": [],
    "focus": [
      "system-zone"
    ],
    "id": "unit-012",
    "in": 75.505,
    "mode": "system",
    "motion_verb": "route",
    "narration_anchor": {
      "quote": "Someone else handles the website. The front desk answers the phone when it can. Guest information",
      "word_end": 170,
      "word_start": 155
    },
    "narrative_state": "current_machine",
    "out": 82.935,
    "sequence_id": "sequence-thesis-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "system-zone",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "system-zone",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Return an unowned handoff to the retry queue instead of hiding the operational failure.",
    "asset_ticket_ids": [],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-system",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator",
      "system-zone"
    ],
    "evidence_ids": [],
    "focus": [
      "repair-retry-queue"
    ],
    "id": "unit-013",
    "in": 82.935,
    "mode": "system",
    "motion_verb": "retry",
    "narration_anchor": {
      "quote": "sits in the booking system. And follow-up happens... if somebody remembers. It's less a system",
      "word_end": 185,
      "word_start": 171
    },
    "narrative_state": "current_machine",
    "out": 91.334,
    "sequence_id": "sequence-thesis-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "repair-retry-queue",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "repair-retry-queue",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Escalate unresolved ownership to the hotel operator as the human control point.",
    "asset_ticket_ids": [],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-system",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator",
      "repair-retry-queue"
    ],
    "evidence_ids": [],
    "focus": [
      "sensitive-case-escalation"
    ],
    "id": "unit-014",
    "in": 91.334,
    "mode": "system",
    "motion_verb": "escalate",
    "narration_anchor": {
      "quote": "than a GROUP PROJECT where everyone assumes someone else did their part. So direct booking isn't",
      "word_end": 201,
      "word_start": 186
    },
    "narrative_state": "current_machine",
    "out": 99.179,
    "sequence_id": "sequence-thesis-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "sensitive-case-escalation",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "sensitive-case-escalation",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Resolve the current-machine view around one accountable operating journey rather than a website feature.",
    "asset_ticket_ids": [],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-system",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator",
      "sensitive-case-escalation"
    ],
    "evidence_ids": [],
    "focus": [
      "independent-hotel-operator"
    ],
    "id": "unit-015",
    "in": 99.179,
    "mode": "system",
    "motion_verb": "measure",
    "narration_anchor": {
      "quote": "really a website feature. It's what happens when all of those small jobs work together.",
      "word_end": 216,
      "word_start": 202
    },
    "narrative_state": "current_machine",
    "out": 106.132,
    "sequence_id": "sequence-thesis-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "independent-hotel-operator",
        "state": "resolved"
      }
    ],
    "world_state_before": [
      {
        "object_id": "independent-hotel-operator",
        "state": "active"
      }
    ]
  }
]
```

## Available persistent-world slice

Use only these approved IDs unless the orchestrator explicitly expands the slice. A state-marker label is an internal concept; prefer showing the operation that produces it.

```json
{
  "objects": [
    {
      "id": "system-zone",
      "kind": "zone",
      "label": "Recovery system",
      "description": "Persistent operating model for audit, repair, consent, qualification, review, and return routing.",
      "zone_id": "system-zone",
      "position": {
        "x": 960,
        "y": 110
      },
      "states": [
        {
          "id": "initial",
          "label": "Dormant"
        },
        {
          "id": "active",
          "label": "Running"
        },
        {
          "id": "failed",
          "label": "Broken"
        },
        {
          "id": "resolved",
          "label": "Recovered"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "hotel-stay-node",
      "kind": "node",
      "label": "Hotel and completed stay",
      "description": "The property delivers the actual stay and earns the opportunity to request a relationship.",
      "zone_id": "reality-zone",
      "position": {
        "x": 400,
        "y": 250
      },
      "states": [
        {
          "id": "initial",
          "label": "Not arrived"
        },
        {
          "id": "active",
          "label": "Stay in progress"
        },
        {
          "id": "resolved",
          "label": "Stay completed"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "stay-key-tag",
      "kind": "token",
      "label": "Physical stay key tag",
      "description": "A recurring physical token for the completed stay; it is not yet a permissioned guest record.",
      "zone_id": "reality-zone",
      "position": {
        "x": 160,
        "y": 480
      },
      "states": [
        {
          "id": "initial",
          "label": "No stay"
        },
        {
          "id": "active",
          "label": "OTA stay completed"
        },
        {
          "id": "failed",
          "label": "Relationship leaked"
        },
        {
          "id": "suppressed",
          "label": "No contact"
        },
        {
          "id": "resolved",
          "label": "Eligible return connected"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "independent-hotel-operator",
      "kind": "actor",
      "label": "Independent hotel operator",
      "description": "The owner or general manager accountable for the direct path, judgment, exceptions, and result.",
      "zone_id": "reality-zone",
      "position": {
        "x": 400,
        "y": 480
      },
      "states": [
        {
          "id": "initial",
          "label": "Fragmented ownership"
        },
        {
          "id": "active",
          "label": "Reviewing"
        },
        {
          "id": "failed",
          "label": "Capacity exceeded"
        },
        {
          "id": "resolved",
          "label": "Accountable owner"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "direct-path-audit",
      "kind": "node",
      "label": "Direct-path audit",
      "description": "The operator checks rate, mobile booking, policy clarity, calls, baseline mix, and handoffs before outreach.",
      "zone_id": "system-zone",
      "position": {
        "x": 630,
        "y": 440
      },
      "states": [
        {
          "id": "initial",
          "label": "Not checked"
        },
        {
          "id": "active",
          "label": "Audit running"
        },
        {
          "id": "failed",
          "label": "Leak found"
        },
        {
          "id": "resolved",
          "label": "Baseline recorded"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "direct-path-repair",
      "kind": "node",
      "label": "Direct-path repair",
      "description": "The broken destination or handoff is repaired and retested before any eligible guest is contacted.",
      "zone_id": "system-zone",
      "position": {
        "x": 860,
        "y": 440
      },
      "states": [
        {
          "id": "initial",
          "label": "Not repaired"
        },
        {
          "id": "active",
          "label": "Repair in progress"
        },
        {
          "id": "failed",
          "label": "Retest failed"
        },
        {
          "id": "resolved",
          "label": "Direct path works"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "permission-gate",
      "kind": "gate",
      "label": "Affirmative permission gate",
      "description": "The hotel requests and records permission; declined, revoked, expired, and ambiguous cases stop.",
      "zone_id": "system-zone",
      "position": {
        "x": 1090,
        "y": 440
      },
      "states": [
        {
          "id": "initial",
          "label": "Not requested"
        },
        {
          "id": "active",
          "label": "Permission requested"
        },
        {
          "id": "failed",
          "label": "Declined or ambiguous"
        },
        {
          "id": "suppressed",
          "label": "Revoked or expired"
        },
        {
          "id": "resolved",
          "label": "Affirmative consent"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "return-qualification-gate",
      "kind": "gate",
      "label": "Return qualification",
      "description": "A relevant reason to return, timing, eligibility, and property fit are checked rather than assumed.",
      "zone_id": "system-zone",
      "position": {
        "x": 630,
        "y": 660
      },
      "states": [
        {
          "id": "initial",
          "label": "Unqualified"
        },
        {
          "id": "active",
          "label": "Qualification running"
        },
        {
          "id": "failed",
          "label": "Not relevant"
        },
        {
          "id": "suppressed",
          "label": "Sensitive or excluded"
        },
        {
          "id": "resolved",
          "label": "Appropriate return"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "human-review-gate",
      "kind": "gate",
      "label": "Mandatory human judgment",
      "description": "Every outbound route passes operator review for voice, relevance, offer, timing, and sensitive exceptions.",
      "zone_id": "system-zone",
      "position": {
        "x": 860,
        "y": 660
      },
      "states": [
        {
          "id": "initial",
          "label": "Unreviewed"
        },
        {
          "id": "active",
          "label": "Human reviewing"
        },
        {
          "id": "failed",
          "label": "Rejected"
        },
        {
          "id": "suppressed",
          "label": "Escalated or stopped"
        },
        {
          "id": "resolved",
          "label": "Approved to send"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "relevant-follow-up",
      "kind": "node",
      "label": "Relevant follow-up",
      "description": "A restrained, approved message reflects the actual stay and a relevant reason to return.",
      "zone_id": "system-zone",
      "position": {
        "x": 1320,
        "y": 220
      },
      "states": [
        {
          "id": "initial",
          "label": "Not queued"
        },
        {
          "id": "active",
          "label": "Approved follow-up"
        },
        {
          "id": "failed",
          "label": "Delivery failed"
        },
        {
          "id": "suppressed",
          "label": "Stopped"
        },
        {
          "id": "resolved",
          "label": "Follow-up delivered"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "direct-booking-confirmation",
      "kind": "outcome",
      "label": "Direct booking confirmation",
      "description": "The guest-facing confirmation visibly closes an appropriate direct return without pretending to prove commission.",
      "zone_id": "reality-zone",
      "position": {
        "x": 400,
        "y": 710
      },
      "states": [
        {
          "id": "initial",
          "label": "Absent"
        },
        {
          "id": "active",
          "label": "Reservation processing"
        },
        {
          "id": "failed",
          "label": "Not confirmed"
        },
        {
          "id": "resolved",
          "label": "Direct booking confirmed"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "relationship-leak-state",
      "kind": "state_marker",
      "label": "Relationship leak",
      "description": "The same guest returns through the paid gate because no bounded relationship path exists.",
      "zone_id": "system-zone",
      "position": {
        "x": 860,
        "y": 220
      },
      "states": [
        {
          "id": "initial",
          "label": "Latent"
        },
        {
          "id": "active",
          "label": "Return leaked"
        },
        {
          "id": "failed",
          "label": "Repeated commission"
        },
        {
          "id": "resolved",
          "label": "Leak interrupted"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "recovered-loop-state",
      "kind": "state_marker",
      "label": "Recovered return loop",
      "description": "The first booking remains OTA-acquired while an appropriate second booking completes directly.",
      "zone_id": "system-zone",
      "position": {
        "x": 1090,
        "y": 220
      },
      "states": [
        {
          "id": "initial",
          "label": "Incomplete"
        },
        {
          "id": "active",
          "label": "Loop running"
        },
        {
          "id": "failed",
          "label": "Return unresolved"
        },
        {
          "id": "resolved",
          "label": "Loop recovered"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "sensitive-case-escalation",
      "kind": "gate",
      "label": "Sensitive-case exception",
      "description": "Ambiguous consent, complaints, accessibility, safety, bereavement, and other sensitive cases stop or escalate.",
      "zone_id": "system-zone",
      "position": {
        "x": 1320,
        "y": 660
      },
      "states": [
        {
          "id": "initial",
          "label": "No exception"
        },
        {
          "id": "active",
          "label": "Escalated"
        },
        {
          "id": "suppressed",
          "label": "Outbound stopped"
        },
        {
          "id": "resolved",
          "label": "Human disposition recorded"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "repair-retry-queue",
      "kind": "node",
      "label": "Repair retry queue",
      "description": "A failed direct-path test returns to audit with an accountable owner or escalates instead of being hidden.",
      "zone_id": "system-zone",
      "position": {
        "x": 630,
        "y": 850
      },
      "states": [
        {
          "id": "initial",
          "label": "Empty"
        },
        {
          "id": "active",
          "label": "Retry assigned"
        },
        {
          "id": "failed",
          "label": "Retry exhausted"
        },
        {
          "id": "resolved",
          "label": "Retest passed"
        }
      ],
      "initial_state": "initial"
    }
  ],
  "edges": [
    {
      "id": "edge-hotel-stay",
      "from": "hotel-stay-node",
      "to": "stay-key-tag",
      "kind": "handoff",
      "label": "complete physical stay",
      "states": [
        {
          "id": "initial",
          "label": "Pending"
        },
        {
          "id": "active",
          "label": "Key tag handed off"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-stay-leak",
      "from": "stay-key-tag",
      "to": "relationship-leak-state",
      "kind": "failure",
      "label": "lose post-stay relationship",
      "states": [
        {
          "id": "initial",
          "label": "Contained"
        },
        {
          "id": "active",
          "label": "Leak active"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-stay-audit",
      "from": "stay-key-tag",
      "to": "direct-path-audit",
      "kind": "audit",
      "label": "audit before outreach",
      "states": [
        {
          "id": "initial",
          "label": "Blocked"
        },
        {
          "id": "active",
          "label": "Audit opened"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-human-exception",
      "from": "human-review-gate",
      "to": "sensitive-case-escalation",
      "kind": "escalation",
      "label": "escalate or stop sensitive case",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Exception escalated"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-confirm-loop",
      "from": "direct-booking-confirmation",
      "to": "recovered-loop-state",
      "kind": "return",
      "label": "resolve recovered loop",
      "states": [
        {
          "id": "initial",
          "label": "Incomplete"
        },
        {
          "id": "active",
          "label": "Loop closed"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-repair-retry",
      "from": "direct-path-repair",
      "to": "repair-retry-queue",
      "kind": "failure",
      "label": "queue failed retest",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Retry queued"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-repair-operator-escalation",
      "from": "direct-path-repair",
      "to": "independent-hotel-operator",
      "kind": "escalation",
      "label": "assign failed repair to operator",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Operator escalation"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-retry-audit",
      "from": "repair-retry-queue",
      "to": "direct-path-audit",
      "kind": "retry",
      "label": "return to accountable audit",
      "states": [
        {
          "id": "initial",
          "label": "Waiting"
        },
        {
          "id": "active",
          "label": "Audit retried"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-audit-exception",
      "from": "direct-path-audit",
      "to": "sensitive-case-escalation",
      "kind": "escalation",
      "label": "escalate unresolved ownership",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Owner escalation"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-permission-exception",
      "from": "permission-gate",
      "to": "sensitive-case-escalation",
      "kind": "escalation",
      "label": "escalate ambiguous consent",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Consent escalated"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-qualification-exception",
      "from": "return-qualification-gate",
      "to": "sensitive-case-escalation",
      "kind": "escalation",
      "label": "escalate sensitive qualification",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Case escalated"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-followup-operator-escalation",
      "from": "relevant-follow-up",
      "to": "independent-hotel-operator",
      "kind": "escalation",
      "label": "escalate delivery failure to operator",
      "states": [
        {
          "id": "initial",
          "label": "Clear"
        },
        {
          "id": "active",
          "label": "Operator escalation"
        }
      ],
      "initial_state": "initial"
    }
  ]
}
```

## Evidence available to this sequence

```json
[]
```

## Asset tickets available to this sequence

```json
[]
```

## Episode mechanic and guardrails

```json
{
  "visual_mechanic": {
    "name": "relationship leak and recovery loop",
    "behavior": "A guest discovers and completes a first stay through a useful OTA gate. The physical stay token either leaks back toward the paid gate or, only after destination audit, repair, consent, qualification, suppression checks, and human review, enters a permissioned return loop owned by the hotel.",
    "why_honest": "The machine never treats all prior guests as return prospects and never frames the OTA as a villain. It preserves the useful first booking, exposes the operator-side settlement consequence, makes disqualification and exceptions visible, and represents success only as an appropriate direct return confirmed by the property.",
    "before": "The first OTA discovery and booking work, but the direct destination may be broken, the stay context is not permissioned memory, and an eligible returning guest can fall back through the same paid gate.",
    "after": "The OTA remains a useful first-booking route while a repaired direct destination, explicit permission, qualification, suppression, human judgment, relevant follow-up, and measurement create a bounded recovery path for the appropriate subset."
  },
  "motion_verbs": [
    "discover",
    "route",
    "book",
    "welcome",
    "audit",
    "compare",
    "repair",
    "request_permission",
    "recognize",
    "remember",
    "qualify",
    "suppress",
    "review",
    "approve",
    "escalate",
    "follow_up",
    "retry",
    "fail",
    "recover",
    "confirm",
    "measure"
  ],
  "guardrails": [
    "The first OTA booking remains useful acquisition; only a later appropriate booking is a recovery opportunity.",
    "A completed OTA-acquired stay is the input, not an assumption that the guest already wants to return.",
    "The direct booking destination is audited and repaired before any guest outreach activates.",
    "Permission is requested explicitly and never replaced by the shorthand capture.",
    "Qualification, suppression, human review, and sensitive-case exceptions remain visible stages.",
    "The physical key tag becomes guest memory only after the consent handoff.",
    "An operator settlement statement or commission ledger shows economic consequence; the guest confirmation does not.",
    "A direct booking confirmation is the visible outcome, not a guaranteed attribution or income promise.",
    "Evidence enters as a sourced parameter attached to what it supports, never as decorative or synthetic proof.",
    "No stock guest, generated person, platform reconstruction, or prior visual assignment is represented as a factual case."
  ],
  "reality_world": {
    "environment": "A bright, specific independent inn with a modest lobby, guestroom threshold, breakfast or courtyard detail, and a small operator workspace embedded in the property rather than a corporate office.",
    "people": "One recurring innkeeper and one recurring guest appear as capable adults making reasonable choices inside an incomplete system; neither is a caricature, victim, platform villain, or claimed factual case study.",
    "lens": "Natural 35-to-50-millimeter observational framing for human interactions, with restrained close details for the physical key tag, operator ledger, phone, and confirmation.",
    "lighting": "Bright natural morning and late-afternoon light with soft contrast, lived-in warmth, and no generic luxury-ad gloss, noir mood, or dark cyberpunk treatment.",
    "palette": "Warm cream, wood, linen, green, and daylight neutrals, oriented by the existing OE ink, schematic navy, drafting blue, ledger gold, and status sage roles.",
    "texture": "Tactile paper, a physical key tag, wood, fabric, and lightly printed operator-ledger marks; texture supports continuity and never disguises a placeholder as evidence.",
    "camera": "Human views remain mostly locked or follow a physical handoff. System views move only to trace work, expose a failure, inspect evidence, or reveal accumulated state; screen direction is preserved from OTA entry through hotel and return.",
    "motif": "The physical key tag represents only the completed stay. At the explicit consent handoff it resolves into a restrained permissioned guest-memory record; an operator-side settlement statement shows commission consequence, while a separate direct booking confirmation remains the outcome object.",
    "forbidden": [
      "masked hospitality staff",
      "generic luxury resort wallpaper",
      "corporate front-desk business imagery",
      "melodramatic peril or platform villain framing",
      "faceless mannequin people",
      "dark cyberpunk or generic AI imagery",
      "generated platform interfaces, text, logos, or evidence",
      "guest-facing receipts presented as hotel commission proof"
    ]
  }
}
```

## Required authoring decisions

Before returning the JSON, make and encode every one of these decisions:

- The single audience inference this sequence must create.
- The visual sentence: subjects, relationship, objects, visible consequence, before state, and after state.
- The minimum number of shots needed; narration units are not automatically shots.
- Each shot's production lane: motion graphics, evidence capture, B-roll edit, AI environmental plate, or hybrid composite.
- Exact start and end time for every shot, with contiguous coverage of the sequence.
- Exact layer rectangles at shot start and end, z-order, opacity, role, and state.
- Primary subject and visual hierarchy; do not distribute attention equally.
- Exact visible text and every timed word or number highlight.
- Every motion beat's cue word index, cue timestamp, duration, property change, easing, and explanatory purpose.
- Transition in and out, including which objects survive across the cut or transformation.
- Evidence source/highlight/extract/attach/change steps whenever proof appears.
- What is inherited from the prior sequence and the precise exit frame handed to the next.
- At least three explicit things this sequence must not do.
- At least five observable review checks that can pass or fail from the animatic.

If the approved inputs do not support an honest visual decision, stop and report the exact missing evidence, ticket, object, or upstream decision. Do not fill the gap with generic imagery.
