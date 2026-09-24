# Blueprint Cinema director packet: sequence-thesis-01

You are the senior motion-design director for one bounded Operator Economy sequence. Author precise scene direction only. Do not write renderer code, generate media, alter the narration, change claims, or edit canonical episode state.

Your result must make the viewer understand a causal relationship against the exact locked voiceover. This is not a request for a topical illustration, a slide, a node-map camera move, or generic "Vox-style" decoration. The transferable editorial-explainer behaviors are deliberate composition, restrained annotation, progressive disclosure, parameter-to-consequence evidence motion, and motivated continuity.

## Output contract

Author exactly one sequence object for `schemas/scene-directions.schema.json` and save it only to the path assigned by the orchestrator. It must contain shot-by-shot pixel geometry, exact text, word-cued motion, evidence choreography, and transition continuity. Return no approvals and make no canonical-state changes.

Episode: `EP006-direct-booking-recovery`
Sequence: `sequence-thesis-01`
Previous sequence: `sequence-hook-01`
Next sequence: `sequence-thesis-02`
Time range: `27.733-67.057` seconds
Locked word range: `55-139`
Exact VO: `This is The Operator Economy, where we show you how to use AI and practical workflows to build and run a one-person business. Today, we're looking at direct-booking recovery. The idea isn't to replace Booking or Expedia. Small hotels need the reach. The opportunity is to help a hotel turn a guest it met through an OTA into a guest it can welcome back directly. Sure... the first booking may belong to the platform. But the relationship AFTER THE STAY should belong to the property.`

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
| 55 | 28.332 | 28.370 | This |
| 56 | 28.450 | 28.610 | is |
| 57 | 28.650 | 28.770 | The |
| 58 | 28.841 | 29.410 | Operator |
| 59 | 29.480 | 30.290 | Economy, |
| 60 | 30.330 | 30.530 | where |
| 61 | 30.610 | 30.770 | we |
| 62 | 30.818 | 31.010 | show |
| 63 | 31.050 | 31.170 | you |
| 64 | 31.210 | 31.330 | how |
| 65 | 31.357 | 31.410 | to |
| 66 | 31.490 | 31.730 | use |
| 67 | 31.943 | 32.370 | AI |
| 68 | 32.410 | 32.530 | and |
| 69 | 32.586 | 33.090 | practical |
| 70 | 33.162 | 33.810 | workflows |
| 71 | 33.863 | 33.970 | to |
| 72 | 34.063 | 34.530 | build |
| 73 | 34.570 | 34.690 | and |
| 74 | 34.810 | 35.170 | run |
| 75 | 35.210 | 35.250 | a |
| 76 | 35.330 | 36.050 | one-person |
| 77 | 36.112 | 36.690 | business. |
| 78 | 37.910 | 38.290 | Today, |
| 79 | 38.317 | 38.450 | we're |
| 80 | 38.490 | 38.770 | looking |
| 81 | 38.797 | 38.850 | at |
| 82 | 38.941 | 40.050 | direct-booking |
| 83 | 40.130 | 40.850 | recovery. |
| 84 | 42.115 | 42.130 | The |
| 85 | 42.226 | 42.610 | idea |
| 86 | 42.710 | 43.090 | isn't |
| 87 | 43.143 | 43.250 | to |
| 88 | 43.310 | 43.730 | replace |
| 89 | 43.810 | 44.370 | Booking |
| 90 | 44.423 | 44.530 | or |
| 91 | 44.610 | 45.330 | Expedia. |
| 92 | 45.477 | 46.210 | Small |
| 93 | 46.290 | 46.770 | hotels |
| 94 | 46.850 | 47.170 | need |
| 95 | 47.190 | 47.250 | the |
| 96 | 47.330 | 47.810 | reach. |
| 97 | 48.675 | 48.690 | The |
| 98 | 48.757 | 49.490 | opportunity |
| 99 | 49.570 | 49.730 | is |
| 100 | 49.757 | 49.810 | to |
| 101 | 49.874 | 50.130 | help |
| 102 | 50.170 | 50.210 | a |
| 103 | 50.277 | 50.610 | hotel |
| 104 | 50.722 | 51.170 | turn |
| 105 | 51.210 | 51.250 | a |
| 106 | 51.330 | 51.730 | guest |
| 107 | 51.810 | 51.970 | it |
| 108 | 52.070 | 52.370 | met |
| 109 | 52.400 | 52.610 | through |
| 110 | 52.663 | 52.770 | an |
| 111 | 52.930 | 53.410 | OTA |
| 112 | 53.602 | 54.370 | into |
| 113 | 54.410 | 54.450 | a |
| 114 | 54.517 | 54.850 | guest |
| 115 | 54.903 | 55.010 | it |
| 116 | 55.050 | 55.170 | can |
| 117 | 55.220 | 55.570 | welcome |
| 118 | 55.650 | 55.970 | back |
| 119 | 56.050 | 56.770 | directly. |
| 120 | 58.622 | 58.942 | Sure... |
| 121 | 58.982 | 59.102 | the |
| 122 | 59.155 | 59.422 | first |
| 123 | 59.482 | 59.902 | booking |
| 124 | 59.982 | 60.222 | may |
| 125 | 60.268 | 60.542 | belong |
| 126 | 60.595 | 60.702 | to |
| 127 | 60.722 | 60.782 | the |
| 128 | 60.853 | 61.582 | platform. |
| 129 | 62.462 | 62.472 | But |
| 130 | 62.492 | 62.552 | the |
| 131 | 62.614 | 63.352 | relationship |
| 132 | 63.472 | 64.072 | AFTER |
| 133 | 64.092 | 64.152 | THE |
| 134 | 64.232 | 64.712 | STAY |
| 135 | 64.769 | 65.112 | should |
| 136 | 65.158 | 65.432 | belong |
| 137 | 65.459 | 65.512 | to |
| 138 | 65.532 | 65.592 | the |
| 139 | 65.654 | 66.312 | property. |

## Approved visual-plan units

These state what must be communicated; they do not prescribe the finished layout.

```json
[
  {
    "action": "Establish the OTA gate as useful acquisition rather than a villain or removable dependency.",
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
      "ota-booking-gate"
    ],
    "id": "unit-005",
    "in": 27.733,
    "mode": "system",
    "motion_verb": "establish",
    "narration_anchor": {
      "quote": "This is The Operator Economy, where we show you how to use AI and",
      "word_end": 68,
      "word_start": 55
    },
    "narrative_state": "current_machine",
    "out": 32.558,
    "sequence_id": "sequence-thesis-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "ota-booking-gate",
        "state": "resolved"
      }
    ],
    "world_state_before": [
      {
        "object_id": "ota-booking-gate",
        "state": "active"
      }
    ]
  },
  {
    "action": "Complete the first booking through the OTA path and preserve its discovery job.",
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
      "first-booking-money-flow"
    ],
    "id": "unit-006",
    "in": 32.558,
    "mode": "system",
    "motion_verb": "book",
    "narration_anchor": {
      "quote": "practical workflows to build and run a one-person business. Today, we're looking at direct-booking",
      "word_end": 82,
      "word_start": 69
    },
    "narrative_state": "current_machine",
    "out": 40.09,
    "sequence_id": "sequence-thesis-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "first-booking-money-flow",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "first-booking-money-flow",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Carry the acquired guest through a capable, human hotel stay.",
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
      "independent-hotel-operator",
      "first-booking-money-flow"
    ],
    "evidence_ids": [],
    "focus": [
      "hotel-stay-node"
    ],
    "id": "unit-007",
    "in": 40.09,
    "mode": "reality",
    "motion_verb": "welcome",
    "narration_anchor": {
      "quote": "recovery. The idea isn't to replace Booking or Expedia. Small hotels need the reach.",
      "word_end": 96,
      "word_start": 83
    },
    "narrative_state": "current_machine",
    "out": 48.242,
    "sequence_id": "sequence-thesis-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "hotel-stay-node",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "hotel-stay-node",
        "state": "initial"
      }
    ]
  },
  {
    "action": "Hold the completed stay as a physical token without treating it as permissioned memory.",
    "asset_ticket_ids": [],
    "audio_state": {
      "music": false,
      "narration": true,
      "sound_design": false
    },
    "camera_anchor": "camera-human",
    "carry": [
      "stay-key-tag",
      "independent-hotel-operator",
      "hotel-stay-node"
    ],
    "evidence_ids": [],
    "focus": [
      "stay-key-tag"
    ],
    "id": "unit-008",
    "in": 48.242,
    "mode": "reality",
    "motion_verb": "remember",
    "narration_anchor": {
      "quote": "The opportunity is to help a hotel turn a guest it met through an OTA",
      "word_end": 111,
      "word_start": 97
    },
    "narrative_state": "current_machine",
    "out": 53.506,
    "sequence_id": "sequence-thesis-01",
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
        "state": "active"
      }
    ]
  },
  {
    "action": "Show the unresolved return falling toward the paid gate while the property lacks a relationship path.",
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
      "relationship-leak-state"
    ],
    "id": "unit-009",
    "in": 53.506,
    "mode": "system",
    "motion_verb": "route",
    "narration_anchor": {
      "quote": "into a guest it can welcome back directly. Sure... the first booking may belong",
      "word_end": 125,
      "word_start": 112
    },
    "narrative_state": "current_machine",
    "out": 60.569,
    "sequence_id": "sequence-thesis-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "relationship-leak-state",
        "state": "failed"
      }
    ],
    "world_state_before": [
      {
        "object_id": "relationship-leak-state",
        "state": "active"
      }
    ]
  },
  {
    "action": "Preview the bounded recovered loop while keeping every gate visibly closed.",
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
      "relationship-leak-state"
    ],
    "evidence_ids": [],
    "focus": [
      "recovered-loop-state"
    ],
    "id": "unit-010",
    "in": 60.569,
    "mode": "system",
    "motion_verb": "recover",
    "narration_anchor": {
      "quote": "to the platform. But the relationship AFTER THE STAY should belong to the property.",
      "word_end": 139,
      "word_start": 126
    },
    "narrative_state": "current_machine",
    "out": 67.057,
    "sequence_id": "sequence-thesis-01",
    "status": "greybox",
    "world_state_after": [
      {
        "object_id": "recovered-loop-state",
        "state": "active"
      }
    ],
    "world_state_before": [
      {
        "object_id": "recovered-loop-state",
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
      "id": "ota-settlement-ledger",
      "kind": "ledger",
      "label": "Operator settlement ledger",
      "description": "An operator-side statement records platform commission and cancellation consequence; it is not guest-facing proof.",
      "zone_id": "proof-zone",
      "position": {
        "x": 1570,
        "y": 500
      },
      "states": [
        {
          "id": "initial",
          "label": "Unopened"
        },
        {
          "id": "active",
          "label": "Commission line visible"
        },
        {
          "id": "failed",
          "label": "Unverified entry"
        },
        {
          "id": "resolved",
          "label": "Economic parameter pinned"
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
      "id": "edge-money-hotel",
      "from": "first-booking-money-flow",
      "to": "hotel-stay-node",
      "kind": "booking",
      "label": "deliver booked stay",
      "states": [
        {
          "id": "initial",
          "label": "Pending"
        },
        {
          "id": "active",
          "label": "Stay funded"
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
      "id": "edge-first-ledger",
      "from": "first-booking-money-flow",
      "to": "ota-settlement-ledger",
      "kind": "money",
      "label": "record operator settlement",
      "states": [
        {
          "id": "initial",
          "label": "Unrecorded"
        },
        {
          "id": "active",
          "label": "Ledger entry posted"
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
