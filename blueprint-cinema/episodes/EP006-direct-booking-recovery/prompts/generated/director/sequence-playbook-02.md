# Blueprint Cinema director packet: sequence-playbook-02

You are the senior motion-design director for one bounded Operator Economy sequence. Author precise scene direction only. Do not write renderer code, generate media, alter the narration, change claims, or edit canonical episode state.

Your result must make the viewer understand a causal relationship against the exact locked voiceover. This is not a request for a topical illustration, a slide, a node-map camera move, or generic "Vox-style" decoration. The transferable editorial-explainer behaviors are deliberate composition, restrained annotation, progressive disclosure, parameter-to-consequence evidence motion, and motivated continuity.

## Output contract

Author exactly one sequence object for `schemas/scene-directions.schema.json` and save it only to the path assigned by the orchestrator. It must contain shot-by-shot pixel geometry, exact text, word-cued motion, evidence choreography, and transition continuity. Return no approvals and make no canonical-state changes.

Episode: `EP006-direct-booking-recovery`
Sequence: `sequence-playbook-02`
Previous sequence: `sequence-playbook-01`
Next sequence: `sequence-playbook-03`
Time range: `559.336-585.884` seconds
Locked word range: `1199-1256`
Exact VO: `Next, fix where the guest lands. Search for the hotel on your phone. Compare its direct rate with the OTA rate. Try to book a room. Read the cancellation terms. Call after the desk gets busy. Don't send guests toward a direct path you haven't tested. More outreach will just show the same broken handoff to more people.`

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
| 1199 | 559.993 | 560.521 | Next, |
| 1200 | 560.621 | 560.921 | fix |
| 1201 | 560.961 | 561.161 | where |
| 1202 | 561.181 | 561.241 | the |
| 1203 | 561.308 | 561.641 | guest |
| 1204 | 561.734 | 562.281 | lands. |
| 1205 | 562.430 | 563.321 | Search |
| 1206 | 563.361 | 563.481 | for |
| 1207 | 563.501 | 563.561 | the |
| 1208 | 563.654 | 564.121 | hotel |
| 1209 | 564.174 | 564.281 | on |
| 1210 | 564.313 | 564.441 | your |
| 1211 | 564.508 | 564.921 | phone. |
| 1212 | 565.051 | 565.961 | Compare |
| 1213 | 566.001 | 566.121 | its |
| 1214 | 566.190 | 566.601 | direct |
| 1215 | 566.697 | 567.081 | rate |
| 1216 | 567.113 | 567.241 | with |
| 1217 | 567.281 | 567.401 | the |
| 1218 | 567.521 | 567.881 | OTA |
| 1219 | 567.961 | 568.441 | rate. |
| 1220 | 568.641 | 569.241 | Try |
| 1221 | 569.268 | 569.321 | to |
| 1222 | 569.369 | 569.561 | book |
| 1223 | 569.601 | 569.641 | a |
| 1224 | 569.737 | 570.601 | room. |
| 1225 | 570.697 | 571.081 | Read |
| 1226 | 571.101 | 571.161 | the |
| 1227 | 571.223 | 571.961 | cancellation |
| 1228 | 572.054 | 572.921 | terms. |
| 1229 | 573.049 | 573.561 | Call |
| 1230 | 573.614 | 573.881 | after |
| 1231 | 573.921 | 574.041 | the |
| 1232 | 574.089 | 574.281 | desk |
| 1233 | 574.329 | 574.521 | gets |
| 1234 | 574.601 | 575.001 | busy. |
| 1235 | 576.004 | 576.124 | Don't |
| 1236 | 576.188 | 576.444 | send |
| 1237 | 576.513 | 576.924 | guests |
| 1238 | 576.958 | 577.164 | toward |
| 1239 | 577.204 | 577.244 | a |
| 1240 | 577.301 | 577.644 | direct |
| 1241 | 577.740 | 578.124 | path |
| 1242 | 578.204 | 578.444 | you |
| 1243 | 578.484 | 578.764 | haven't |
| 1244 | 578.833 | 579.564 | tested. |
| 1245 | 580.578 | 580.604 | More |
| 1246 | 580.684 | 581.324 | outreach |
| 1247 | 581.372 | 581.564 | will |
| 1248 | 581.628 | 581.884 | just |
| 1249 | 581.932 | 582.124 | show |
| 1250 | 582.184 | 582.364 | the |
| 1251 | 582.444 | 582.764 | same |
| 1252 | 582.821 | 583.164 | broken |
| 1253 | 583.244 | 583.964 | handoff |
| 1254 | 583.991 | 584.044 | to |
| 1255 | 584.108 | 584.364 | more |
| 1256 | 584.444 | 585.324 | people. |

## Approved visual-plan units

These state what must be communicated; they do not prescribe the finished layout.

```json
[
  {
    "action": "Open the installation retest with audit, repair, destination, and retry states closed again.",
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
      "direct-path-audit"
    ],
    "evidence_ids": [],
    "focus": [
      "direct-path-audit"
    ],
    "id": "unit-096",
    "in": 559.336,
    "mode": "reset",
    "motion_verb": "reset",
    "narration_anchor": {
      "quote": "Next, fix where the guest lands. Search for",
      "word_end": 1206,
      "word_start": 1199
    },
    "narrative_state": "installation",
    "out": 563.491,
    "sequence_id": "sequence-playbook-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-path-audit",
        "state": "initial"
      },
      {
        "object_id": "direct-path-repair",
        "state": "initial"
      },
      {
        "object_id": "direct-booking-destination",
        "state": "initial"
      },
      {
        "object_id": "repair-retry-queue",
        "state": "initial"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-path-audit",
        "state": "resolved"
      },
      {
        "object_id": "direct-path-repair",
        "state": "resolved"
      },
      {
        "object_id": "direct-booking-destination",
        "state": "resolved"
      },
      {
        "object_id": "repair-retry-queue",
        "state": "active"
      }
    ]
  },
  {
    "action": "Complete the search, comparison, booking, terms, and phone audit from the guest side.",
    "asset_ticket_ids": [
      "ticket-direct-path-test"
    ],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-system",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator",
      "direct-path-audit"
    ],
    "evidence_ids": [],
    "focus": [
      "direct-path-audit"
    ],
    "id": "unit-097",
    "in": 563.491,
    "mode": "system",
    "motion_verb": "audit",
    "narration_anchor": {
      "quote": "the hotel on your phone. Compare its direct rate",
      "word_end": 1215,
      "word_start": 1207
    },
    "narrative_state": "installation",
    "out": 567.097,
    "sequence_id": "sequence-playbook-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-path-audit",
        "state": "resolved"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-path-audit",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Expose rate or policy mismatch at the direct destination before outreach.",
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
      "direct-path-audit"
    ],
    "evidence_ids": [],
    "focus": [
      "direct-booking-destination"
    ],
    "id": "unit-098",
    "in": 567.097,
    "mode": "system",
    "motion_verb": "compare",
    "narration_anchor": {
      "quote": "with the OTA rate. Try to book a",
      "word_end": 1223,
      "word_start": 1216
    },
    "narrative_state": "installation",
    "out": 569.689,
    "sequence_id": "sequence-playbook-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-booking-destination",
        "state": "failed"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-booking-destination",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Repair each failed handoff and assign a real owner.",
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
      "direct-booking-destination"
    ],
    "evidence_ids": [],
    "focus": [
      "direct-path-repair"
    ],
    "id": "unit-099",
    "in": 569.689,
    "mode": "system",
    "motion_verb": "repair",
    "narration_anchor": {
      "quote": "room. Read the cancellation terms. Call after the",
      "word_end": 1231,
      "word_start": 1224
    },
    "narrative_state": "installation",
    "out": 574.065,
    "sequence_id": "sequence-playbook-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-path-repair",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-path-repair",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Retest the repaired path and route any failure back through audit.",
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
      "direct-path-repair"
    ],
    "evidence_ids": [],
    "focus": [
      "repair-retry-queue"
    ],
    "id": "unit-100",
    "in": 574.065,
    "mode": "system",
    "motion_verb": "retry",
    "narration_anchor": {
      "quote": "desk gets busy. Don't send guests toward a",
      "word_end": 1239,
      "word_start": 1232
    },
    "narrative_state": "installation",
    "out": 577.272,
    "sequence_id": "sequence-playbook-02",
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
    "action": "Resolve the repair only after the repeated guest-side path passes.",
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
      "direct-path-repair"
    ],
    "id": "unit-101",
    "in": 577.272,
    "mode": "system",
    "motion_verb": "repair",
    "narration_anchor": {
      "quote": "direct path you haven't tested. More outreach will just",
      "word_end": 1248,
      "word_start": 1240
    },
    "narrative_state": "installation",
    "out": 581.908,
    "sequence_id": "sequence-playbook-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-path-repair",
        "state": "resolved"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-path-repair",
        "state": "active"
      }
    ]
  },
  {
    "action": "Activate the direct destination only after the complete guest path passes.",
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
      "direct-path-repair"
    ],
    "evidence_ids": [],
    "focus": [
      "direct-booking-destination"
    ],
    "id": "unit-102",
    "in": 581.908,
    "mode": "system",
    "motion_verb": "resolve",
    "narration_anchor": {
      "quote": "show the same broken handoff to more people.",
      "word_end": 1256,
      "word_start": 1249
    },
    "narrative_state": "installation",
    "out": 585.884,
    "sequence_id": "sequence-playbook-02",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-booking-destination",
        "state": "resolved"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-booking-destination",
        "state": "failed"
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
      "id": "direct-booking-destination",
      "kind": "destination",
      "label": "Repaired direct destination",
      "description": "The hotel's own tested booking path, with understandable rate, policy, mobile flow, and help route.",
      "zone_id": "reality-zone",
      "position": {
        "x": 160,
        "y": 710
      },
      "states": [
        {
          "id": "initial",
          "label": "Unverified"
        },
        {
          "id": "active",
          "label": "Return visit routed"
        },
        {
          "id": "failed",
          "label": "Booking path failed"
        },
        {
          "id": "resolved",
          "label": "Direct booking accepted"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "return-booking-money-flow",
      "kind": "money_flow",
      "label": "Return-booking money flow",
      "description": "The later appropriate reservation flows through the direct path and is measured separately.",
      "zone_id": "proof-zone",
      "position": {
        "x": 1780,
        "y": 250
      },
      "states": [
        {
          "id": "initial",
          "label": "No return"
        },
        {
          "id": "active",
          "label": "Direct value routed"
        },
        {
          "id": "failed",
          "label": "Return not completed"
        },
        {
          "id": "resolved",
          "label": "Direct value recorded"
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
      "id": "edge-audit-repair",
      "from": "direct-path-audit",
      "to": "direct-path-repair",
      "kind": "repair",
      "label": "repair documented leaks",
      "states": [
        {
          "id": "initial",
          "label": "Blocked"
        },
        {
          "id": "active",
          "label": "Repair authorized"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-repair-permission",
      "from": "direct-path-repair",
      "to": "permission-gate",
      "kind": "permission",
      "label": "enable permission request only after retest",
      "states": [
        {
          "id": "initial",
          "label": "Blocked"
        },
        {
          "id": "active",
          "label": "Permission stage enabled"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-followup-direct",
      "from": "relevant-follow-up",
      "to": "direct-booking-destination",
      "kind": "outbound",
      "label": "route return to repaired destination",
      "states": [
        {
          "id": "initial",
          "label": "Idle"
        },
        {
          "id": "active",
          "label": "Return visit routed"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-direct-return-money",
      "from": "direct-booking-destination",
      "to": "return-booking-money-flow",
      "kind": "money",
      "label": "route direct return value",
      "states": [
        {
          "id": "initial",
          "label": "Pending"
        },
        {
          "id": "active",
          "label": "Direct value flowing"
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
[
  {
    "id": "ticket-direct-path-test",
    "story_role": "process",
    "narration_anchor": "Search on a phone, compare the direct rate, try to book, read the terms, and call when the desk is busy.",
    "required_semantic_content": "An original, authorized process capture of a real property's mobile direct path and call handoff, with current terms and property identity reviewed before use.",
    "preferred_source_route": "original_capture",
    "evidence_ids": [],
    "claim_ids": [],
    "rights_requirements": [
      "property authorization",
      "interface capture permission",
      "private data excluded"
    ],
    "provenance_requirements": [
      "canonical URL",
      "property",
      "capture operator",
      "capture date",
      "checksum",
      "source in and out",
      "crop",
      "timeline use"
    ],
    "synthetic_status": "prohibited",
    "status": "ticketed_placeholder",
    "placeholder_behavior": "Show a neutral phone-outline slate labeled TICKET: DIRECT-PATH TEST; do not draw or infer an interface from narration."
  }
]
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
