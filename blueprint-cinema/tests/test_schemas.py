from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from blueprint_cinema.paths import SCHEMAS_ROOT
from blueprint_cinema.validation import load_json, schema_errors


def test_every_schema_is_a_valid_draft_2020_12_contract():
    schema_paths = sorted(SCHEMAS_ROOT.glob("*.schema.json"))
    assert len(schema_paths) >= 10
    for schema_path in schema_paths:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_current_episode_project_state_and_authored_instances_match_schemas(episode_path):
    contracts = {
        "episode.json": "episode-project.schema.json",
        "input-lock.json": "input-lock.schema.json",
        "production-state.json": "production-state.schema.json",
        "episode-engine.json": "episode-engine.schema.json",
        "world.json": "world.schema.json",
        "visual-plan.json": "visual-plan.schema.json",
        "asset-tickets.json": "asset-ticket.schema.json",
    }
    for instance_name, schema_name in contracts.items():
        assert not schema_errors(load_json(episode_path / instance_name), schema_name)


def test_current_agent_fixtures_match_packet_schemas(episode_path):
    for work_path in (episode_path / "agents" / "work-orders").glob("*.json"):
        work = load_json(work_path)
        assert not schema_errors(work, "agent-work-order.schema.json")
        packet_path = episode_path / "agents" / "deliverables" / work["work_order_id"] / "deliverable.json"
        assert not schema_errors(load_json(packet_path), "agent-deliverable.schema.json")

