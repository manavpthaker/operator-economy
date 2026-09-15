# Blueprint Cinema director packet: sequence-hook-01

You are the senior motion-design director for one bounded Operator Economy sequence. Author precise scene direction only. Do not write renderer code, generate media, alter the narration, change claims, or edit canonical episode state.

Your result must make the viewer understand a causal relationship against the exact locked voiceover. This is not a request for a topical illustration, a slide, a node-map camera move, or generic "Vox-style" decoration. The transferable editorial-explainer behaviors are deliberate composition, restrained annotation, progressive disclosure, parameter-to-consequence evidence motion, and motivated continuity.

## Output contract

Author exactly one sequence object for `schemas/scene-directions.schema.json` and save it only to the path assigned by the orchestrator. It must contain shot-by-shot pixel geometry, exact text, word-cued motion, evidence choreography, and transition continuity. Return no approvals and make no canonical-state changes.

Episode: `EP006-direct-booking-recovery`
Sequence: `sequence-hook-01`
Previous sequence: `none; establish the opening state`
Next sequence: `sequence-thesis-01`
Time range: `0.000-27.733` seconds
Locked word range: `0-54`
Exact VO: `Hotels keep paying to meet the SAME guest. More than 60 percent of independent-hotel reservations come through online travel agencies, or OTAs. A guest finds the property on Booking, has a beautiful stay... and returns to Booking next time. Today, I'll show you how an operator can help the hotel earn that return visit DIRECTLY.`

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
| 0 | 0.411 | 0.480 | Hotels |
| 1 | 0.544 | 0.800 | keep |
| 2 | 0.880 | 1.360 | paying |
| 3 | 1.413 | 1.520 | to |
| 4 | 1.568 | 1.760 | meet |
| 5 | 1.800 | 1.920 | the |
| 6 | 2.080 | 2.720 | SAME |
| 7 | 2.920 | 4.560 | guest. |
| 8 | 5.279 | 5.290 | More |
| 9 | 5.338 | 5.530 | than |
| 10 | 5.770 | 6.250 | 60 |
| 11 | 6.330 | 6.890 | percent |
| 12 | 6.970 | 7.130 | of |
| 13 | 7.183 | 8.250 | independent-hotel |
| 14 | 8.318 | 9.130 | reservations |
| 15 | 9.242 | 9.690 | come |
| 16 | 9.730 | 10.010 | through |
| 17 | 10.079 | 10.490 | online |
| 18 | 10.559 | 10.970 | travel |
| 19 | 11.059 | 12.090 | agencies, |
| 20 | 12.197 | 12.410 | or |
| 21 | 12.650 | 13.610 | OTAs. |
| 22 | 14.600 | 14.617 | A |
| 23 | 14.623 | 14.653 | guest |
| 24 | 14.720 | 15.053 | finds |
| 25 | 15.073 | 15.133 | the |
| 26 | 15.186 | 15.613 | property |
| 27 | 15.666 | 15.773 | on |
| 28 | 15.843 | 16.573 | Booking, |
| 29 | 16.633 | 16.813 | has |
| 30 | 16.853 | 16.893 | a |
| 31 | 16.965 | 17.613 | beautiful |
| 32 | 17.725 | 18.733 | stay... |
| 33 | 18.773 | 18.893 | and |
| 34 | 18.953 | 19.373 | returns |
| 35 | 19.400 | 19.453 | to |
| 36 | 19.493 | 19.773 | Booking |
| 37 | 19.837 | 20.093 | next |
| 38 | 20.157 | 20.813 | time. |
| 39 | 21.660 | 22.013 | Today, |
| 40 | 22.053 | 22.173 | I'll |
| 41 | 22.205 | 22.333 | show |
| 42 | 22.373 | 22.493 | you |
| 43 | 22.533 | 22.653 | how |
| 44 | 22.706 | 22.813 | an |
| 45 | 22.875 | 23.373 | operator |
| 46 | 23.453 | 23.693 | can |
| 47 | 23.741 | 23.933 | help |
| 48 | 23.953 | 24.013 | the |
| 49 | 24.080 | 24.413 | hotel |
| 50 | 24.493 | 24.813 | earn |
| 51 | 24.845 | 24.973 | that |
| 52 | 25.030 | 25.373 | return |
| 53 | 25.440 | 25.773 | visit |
| 54 | 25.910 | 27.133 | DIRECTLY. |

## Approved visual-plan units

These state what must be communicated; they do not prescribe the finished layout.

```json
[
  {
    "action": "Establish one specific guest completing a physical stay at the independent inn.",
    "asset_ticket_ids": [
      "ticket-inn-reality"
    ],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-human",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator"
    ],
    "evidence_ids": [],
    "focus": [
      "stay-key-tag"
    ],
    "id": "unit-001",
    "in": 0.0,
    "mode": "reality",
    "motion_verb": "welcome",
    "narration_anchor": {
      "quote": "Hotels keep paying to meet the SAME guest. More than 60 percent of independent-hotel",
      "word_end": 13,
      "word_start": 0
    },
    "narrative_state": "tension",
    "out": 8.284,
    "sequence_id": "sequence-hook-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "stay-key-tag",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "stay-key-tag",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Open the exact vendor-source ticket for the spoken OTA-share claim without inventing source text.",
    "asset_ticket_ids": [
      "ticket-cloudbeds-source"
    ],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-proof",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator"
    ],
    "evidence_ids": [
      "evidence-ota-share"
    ],
    "focus": [
      "ota-booking-gate"
    ],
    "id": "unit-002",
    "in": 8.284,
    "mode": "proof",
    "motion_verb": "inspect",
    "narration_anchor": {
      "quote": "reservations come through online travel agencies, or OTAs. A guest finds the property on",
      "word_end": 27,
      "word_start": 14
    },
    "narrative_state": "tension",
    "out": 15.808,
    "sequence_id": "sequence-hook-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "ota-booking-gate",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "ota-booking-gate",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Route the same stay token back toward the useful paid gate to expose the relationship leak.",
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
      "ota-booking-gate"
    ],
    "evidence_ids": [],
    "focus": [
      "relationship-leak-state"
    ],
    "id": "unit-003",
    "in": 15.808,
    "mode": "system",
    "motion_verb": "route",
    "narration_anchor": {
      "quote": "Booking, has a beautiful stay... and returns to Booking next time. Today, I'll",
      "word_end": 40,
      "word_start": 28
    },
    "narrative_state": "tension",
    "out": 22.189,
    "sequence_id": "sequence-hook-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "relationship-leak-state",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "relationship-leak-state",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Reveal the counter-system by opening the direct-path audit before any outreach can begin.",
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
      "relationship-leak-state"
    ],
    "evidence_ids": [],
    "focus": [
      "direct-path-audit"
    ],
    "id": "unit-004",
    "in": 22.189,
    "mode": "system",
    "motion_verb": "audit",
    "narration_anchor": {
      "quote": "show you how an operator can help the hotel earn that return visit DIRECTLY.",
      "word_end": 54,
      "word_start": 41
    },
    "narrative_state": "tension",
    "out": 27.733,
    "sequence_id": "sequence-hook-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "direct-path-audit",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "direct-path-audit",
        "state": "initial"
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
      "id": "market-discovery",
      "kind": "node",
      "label": "Guest discovery",
      "description": "The guest discovers a specific independent property through a useful market surface.",
      "zone_id": "reality-zone",
      "position": {
        "x": 160,
        "y": 250
      },
      "states": [
        {
          "id": "initial",
          "label": "No discovery"
        },
        {
          "id": "active",
          "label": "Interest present"
        },
        {
          "id": "resolved",
          "label": "Property chosen"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "ota-booking-gate",
      "kind": "gate",
      "label": "Useful OTA booking gate",
      "description": "The platform supplies discovery and a trusted checkout for the first reservation.",
      "zone_id": "system-zone",
      "position": {
        "x": 630,
        "y": 220
      },
      "states": [
        {
          "id": "initial",
          "label": "Available"
        },
        {
          "id": "active",
          "label": "First booking routed"
        },
        {
          "id": "resolved",
          "label": "Stay acquired"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "first-booking-money-flow",
      "kind": "money_flow",
      "label": "First-booking money flow",
      "description": "Room revenue and platform commission are separated for operator-side accounting.",
      "zone_id": "proof-zone",
      "position": {
        "x": 1570,
        "y": 250
      },
      "states": [
        {
          "id": "initial",
          "label": "Unmeasured"
        },
        {
          "id": "active",
          "label": "Commission applied"
        },
        {
          "id": "resolved",
          "label": "Cost recorded"
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
      "id": "edge-discovery-ota",
      "from": "market-discovery",
      "to": "ota-booking-gate",
      "kind": "discovery",
      "label": "discover through OTA",
      "states": [
        {
          "id": "initial",
          "label": "Idle"
        },
        {
          "id": "active",
          "label": "Discovery routed"
        }
      ],
      "initial_state": "initial"
    },
    {
      "id": "edge-ota-money",
      "from": "ota-booking-gate",
      "to": "first-booking-money-flow",
      "kind": "money",
      "label": "apply first-booking commission",
      "states": [
        {
          "id": "initial",
          "label": "Idle"
        },
        {
          "id": "active",
          "label": "Commission flowing"
        }
      ],
      "initial_state": "initial"
    },
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
      "id": "edge-leak-ota",
      "from": "relationship-leak-state",
      "to": "ota-booking-gate",
      "kind": "return",
      "label": "repurchase the introduction",
      "states": [
        {
          "id": "initial",
          "label": "Idle"
        },
        {
          "id": "active",
          "label": "Guest returns via OTA"
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
[
  {
    "id": "evidence-ota-share",
    "label": "Vendor-published OTA booking share",
    "target_ids": [
      "ota-booking-gate",
      "relationship-leak-state"
    ],
    "claim_ids": [
      "claim-ota-share"
    ],
    "parameter_ids": [
      "parameter-ota-booking-share"
    ],
    "source_path": "studio/originate/direct-booking-recovery/research.md",
    "source_sha256": "61a1ed53bafa657266c7ad6b27af9069d2a75ad05f885f987776f9d781e6076e",
    "status": "locked_source"
  }
]
```

## Asset tickets available to this sequence

```json
[
  {
    "id": "ticket-cloudbeds-source",
    "story_role": "proof",
    "narration_anchor": "Cloudbeds looked at roughly ninety million bookings and found more than sixty percent came through OTAs.",
    "required_semantic_content": "A canonical capture of the exact vendor-published source context with publisher, page title, access date, highlighted claim, caveat, and enough surrounding text to avoid misleading extraction.",
    "preferred_source_route": "original_capture",
    "evidence_ids": [
      "evidence-ota-share",
      "evidence-cancellation-gap"
    ],
    "claim_ids": [
      "claim-ota-share",
      "claim-cancellation-rate-gap"
    ],
    "rights_requirements": [
      "source quotation limits",
      "editorial fair-use review",
      "canonical URL retained"
    ],
    "provenance_requirements": [
      "canonical source",
      "publisher",
      "page title",
      "check date",
      "capture date",
      "checksum",
      "source context",
      "timeline use"
    ],
    "synthetic_status": "prohibited",
    "status": "ticketed_placeholder",
    "placeholder_behavior": "Show an unmistakable neutral proof-ticket slate pinned to the affected nodes; do not synthesize source text or figures."
  },
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
  },
  {
    "id": "ticket-inn-reality",
    "story_role": "human_context",
    "narration_anchor": "A guest finds the property, has a beautiful stay, and the operator later reviews the journey.",
    "required_semantic_content": "One specific modest independent inn, one recurring capable operator, one recurring guest, and a physical key-tag handoff that establishes a completed stay without implying consent.",
    "preferred_source_route": "original_capture",
    "evidence_ids": [],
    "claim_ids": [],
    "rights_requirements": [
      "property permission",
      "recognizable-person release",
      "location-use record"
    ],
    "provenance_requirements": [
      "canonical source",
      "creator",
      "capture date",
      "checksum",
      "face review",
      "timeline use",
      "crop",
      "focal point"
    ],
    "synthetic_status": "not_planned",
    "status": "ticketed_placeholder",
    "placeholder_behavior": "Show a high-contrast neutral slate labeled TICKET: INN REALITY with the story job and no attractive proxy image."
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
