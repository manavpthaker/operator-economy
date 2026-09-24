from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

from . import WORKFLOW_VERSION
from .board import build_board
from .generate import check_look_lock, generate, lock_look
from .hashes import sha256_file, write_json_atomic
from .input_lock import build_input_lock, stage_locked_audio
from .paths import (
    BLUEPRINT_ROOT,
    EPISODES_ROOT,
    RENDERER_ROOT,
    EpisodeIdentity,
    PathContractError,
    blueprint_relative,
    episode_dir,
    load_episode_identity,
)
from .render_data import compile_render_data, write_render_data
from .review import generate_reviews
from .scene_prompts import build_director_prompts, build_scene_prompts
from .state import initial_state, next_stage, record_approval, validate_state, validate_state_through
from .validation import (
    STAGES,
    ValidationFailure,
    load_json,
    validate_asset_tickets,
    validate_clean_room,
    validate_deliverable,
    validate_engine,
    validate_episode_project,
    validate_input_lock,
    validate_plan,
    validate_scene_directions,
    validate_schema,
    validate_work_order,
    validate_world,
)


def _context(identity: EpisodeIdentity, path: Path) -> None:
    print(f"Resolved episode: {identity.folder_name}")
    print(f"Episode path: {path}")
    print(f"Blueprint root: {BLUEPRINT_ROOT}")


def _resolved(folder: str) -> tuple[EpisodeIdentity, Path, dict]:
    identity, path, project = load_episode_identity(folder)
    validate_episode_project(project, identity)
    _context(identity, path)
    return identity, path, project


def _required_files(path: Path, names: list[str]) -> list[dict]:
    return [load_json(path / name) for name in names]


def _print_validation_blocker(
    identity: EpisodeIdentity,
    path: Path,
    validated_stage: str,
    approval_command: str,
) -> None:
    state = load_json(path / "production-state.json")
    try:
        validate_state(state, path, identity)
    except ValidationFailure:
        print(f"Blocking gate: {validated_stage} (run {approval_command})")
        return
    if validated_stage not in state.get("approvals", {}):
        print(f"Blocking gate: {validated_stage} (run {approval_command})")
        return
    current = state["current_stage"]
    print(f"Current production state: {current}")
    print(f"Blocking gate: {next_stage(current) or 'none'}")


def cmd_init(args: argparse.Namespace) -> int:
    identity = EpisodeIdentity.from_init(args.episode_code, args.slug)
    path = episode_dir(identity.folder_name)
    _context(identity, path)
    project_path = path / "episode.json"
    state_path = path / "production-state.json"
    if project_path.exists() or state_path.exists():
        raise ValidationFailure("init", ["episode project or production state already exists; refusing to overwrite"])
    for relative in (
        "inputs", "assets", "edit", "agents/work-orders", "agents/deliverables",
        "prompts/generated/director", "prompts/generated/build", "render-data", "review", "delivery",
    ):
        (path / relative).mkdir(parents=True, exist_ok=True)
    project = {
        "$schema": "../../schemas/episode-project.schema.json",
        "schema_version": "1.0.0",
        "workflow_version": WORKFLOW_VERSION,
        **identity.as_dict(),
        "upstream_workspace": f"studio/originate/{identity.slug}/",
        "status": "active",
    }
    validate_episode_project(project, identity)
    write_json_atomic(project_path, project)
    write_json_atomic(state_path, initial_state(identity.folder_name))
    print(f"Created: {project_path}")
    print(f"Created: {state_path}")
    print("Blocking gate: inputs_locked")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    state_path = path / "production-state.json"
    state = load_json(state_path)
    validate_state(state, path, identity)
    current = state["current_stage"]
    print(f"Current production state: {current}")
    print(f"Blocking gate: {next_stage(current) or 'none'}")
    for stage, approval in state.get("approvals", {}).items():
        print(f"Approval {stage}: {approval['approved_at']}")
    return 0


def cmd_lock_inputs(args: argparse.Namespace) -> int:
    identity, path, project = _resolved(args.episode)
    lock = build_input_lock(identity, project)
    validate_input_lock(lock, identity)
    lock_path = path / "input-lock.json"
    existing = load_json(lock_path) if lock_path.is_file() else None
    if existing:
        comparable_existing = copy.deepcopy({key: value for key, value in existing.items() if key != "locked_at"})
        comparable_new = copy.deepcopy({key: value for key, value in lock.items() if key != "locked_at"})
        for artifact in comparable_existing.get("artifacts", []):
            artifact.pop("locked_at", None)
        for artifact in comparable_new.get("artifacts", []):
            artifact.pop("locked_at", None)
        if comparable_existing == comparable_new:
            lock = existing
            print("Input lock is already current; preserving its timestamp and approvals.")
        else:
            write_json_atomic(lock_path, lock)
    else:
        write_json_atomic(lock_path, lock)
    approval_paths = {"episode:input-lock.json": lock_path}
    for artifact in lock["artifacts"]:
        approval_paths[f"repo:{artifact['path']}"] = BLUEPRINT_ROOT.parent / artifact["path"]
    state = record_approval(path / "production-state.json", path, identity, "inputs_locked", approval_paths)
    print(f"Locked input manifest: {lock_path}")
    print(f"Approved script SHA-256: {lock['approved_script_sha256']}")
    print(f"Locked VO duration: {lock['audio_duration_seconds']:.3f}s")
    print(f"Current production state: {state['current_stage']}")
    print("Blocking gate: episode_engine_approved")
    return 0


def cmd_validate_engine(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(load_json(path / "production-state.json"), path, identity, "inputs_locked")
    engine_path = path / "episode-engine.json"
    validate_engine(load_json(engine_path), identity)
    print(f"Validated engine: {engine_path}")
    print(f"SHA-256: {sha256_file(engine_path)}")
    _print_validation_blocker(identity, path, "episode_engine_approved", "approve-engine")
    return 0


def cmd_approve_engine(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    cmd_validate_engine(argparse.Namespace(episode=args.episode))
    state = record_approval(
        path / "production-state.json", path, identity, "episode_engine_approved",
        {"episode:input-lock.json": path / "input-lock.json", "episode:episode-engine.json": path / "episode-engine.json"},
    )
    generate_reviews(path)
    print(f"Current production state: {state['current_stage']}")
    print("Blocking gate: world_approved")
    return 0


def cmd_validate_world(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(load_json(path / "production-state.json"), path, identity, "episode_engine_approved")
    world_path = path / "world.json"
    validate_world(load_json(world_path), identity)
    print(f"Validated world: {world_path}")
    print(f"SHA-256: {sha256_file(world_path)}")
    _print_validation_blocker(identity, path, "world_approved", "approve-world")
    return 0


def cmd_approve_world(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    cmd_validate_world(argparse.Namespace(episode=args.episode))
    state = record_approval(
        path / "production-state.json", path, identity, "world_approved",
        {
            "episode:input-lock.json": path / "input-lock.json",
            "episode:episode-engine.json": path / "episode-engine.json",
            "episode:world.json": path / "world.json",
        },
    )
    generate_reviews(path)
    print(f"Current production state: {state['current_stage']}")
    print("Blocking gate: visual_plan_approved")
    return 0


def _validate_plan_files(identity: EpisodeIdentity, path: Path) -> tuple[dict, dict, dict, dict, dict]:
    lock, engine, world, plan, tickets = _required_files(
        path, ["input-lock.json", "episode-engine.json", "world.json", "visual-plan.json", "asset-tickets.json"]
    )
    validate_asset_tickets(tickets, world, identity)
    validate_plan(
        plan, lock, engine, world, tickets, identity,
        lock_hash=sha256_file(path / "input-lock.json"),
        engine_hash=sha256_file(path / "episode-engine.json"),
        world_hash=sha256_file(path / "world.json"),
    )
    validate_clean_room([plan, tickets], "visual_plan_approved")
    return lock, engine, world, plan, tickets


def cmd_validate_plan(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(load_json(path / "production-state.json"), path, identity, "world_approved")
    _, _, _, plan, _ = _validate_plan_files(identity, path)
    print(f"Validated visual plan: {path / 'visual-plan.json'}")
    print(f"Units: {len(plan['units'])}; coverage: {plan['audio_duration_seconds']:.3f}s")
    print(f"SHA-256: {sha256_file(path / 'visual-plan.json')}")
    _print_validation_blocker(identity, path, "visual_plan_approved", "approve-plan")
    return 0


def cmd_approve_plan(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    cmd_validate_plan(argparse.Namespace(episode=args.episode))
    state = record_approval(
        path / "production-state.json", path, identity, "visual_plan_approved",
        {
            "episode:input-lock.json": path / "input-lock.json",
            "episode:episode-engine.json": path / "episode-engine.json",
            "episode:world.json": path / "world.json",
            "episode:visual-plan.json": path / "visual-plan.json",
            "episode:asset-tickets.json": path / "asset-tickets.json",
        },
    )
    generate_reviews(path)
    print(f"Current production state: {state['current_stage']}")
    print("Blocking gate: greybox_ready")
    return 0


def cmd_build_greybox_data(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    state = load_json(path / "production-state.json")
    validate_state_through(state, path, identity, "visual_plan_approved")
    lock, _, world, plan, tickets = _validate_plan_files(identity, path)
    data = compile_render_data(identity, path, lock, world, plan, tickets)
    render_path = path / "render-data" / "greybox.json"
    digest = write_render_data(render_path, data)
    state = record_approval(
        path / "production-state.json", path, identity, "greybox_ready",
        {
            "episode:input-lock.json": path / "input-lock.json",
            "episode:episode-engine.json": path / "episode-engine.json",
            "episode:world.json": path / "world.json",
            "episode:visual-plan.json": path / "visual-plan.json",
            "episode:asset-tickets.json": path / "asset-tickets.json",
            "episode:render-data/greybox.json": render_path,
        },
    )
    generate_reviews(path)
    print(f"Generated deterministic render data: {render_path}")
    print(f"SHA-256: {digest}")
    print(f"Current production state: {state['current_stage']}")
    print("Blocking gate: greybox_approved (smoke-render does not approve it)")
    return 0


def cmd_smoke_render(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(load_json(path / "production-state.json"), path, identity, "greybox_ready")
    render_path = path / "render-data" / "greybox.json"
    data = load_json(render_path)
    validate_schema(data, "render-data.schema.json", "smoke_render")
    validate_clean_room(data, "smoke_render")
    lock = load_json(path / "input-lock.json")
    staged_audio = RENDERER_ROOT / "public" / "generated" / identity.folder_name / "full-episode.mp3"
    stage_locked_audio(lock, staged_audio)
    output = path / "review" / "generated" / "representative-frame.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    if not (RENDERER_ROOT / "node_modules").is_dir():
        raise ValidationFailure("smoke_render", [f"renderer dependencies missing; run: cd {RENDERER_ROOT} && npm install"])
    command = [
        "npx", "remotion", "still", "src/index.ts", "BlueprintCinema", str(output),
        f"--props={render_path}", "--frame=450", "--overwrite",
    ]
    result = subprocess.run(command, cwd=RENDERER_ROOT, check=False)
    if result.returncode != 0 or not output.is_file():
        raise ValidationFailure("smoke_render", ["representative Remotion frame failed"])
    generate_reviews(path)
    print(f"Staged verified audio: {staged_audio}")
    print(f"Rendered representative frame: {output}")
    print("Blocking gate: greybox_approved (no approval recorded by smoke render)")
    return 0


def cmd_build_director_prompts(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(
        load_json(path / "production-state.json"), path, identity, "visual_plan_approved"
    )
    lock, engine, world, plan, tickets = _validate_plan_files(identity, path)
    outputs = build_director_prompts(
        identity,
        path,
        lock,
        engine,
        world,
        plan,
        tickets,
        sequence_ids=args.sequence,
    )
    print(f"Generated director prompt manifest: {outputs[0]}")
    print(f"Director packets: {len(outputs) - 1}")
    print("Production state unchanged; prompts do not constitute scene direction or approval.")
    return 0


def _validated_scene_directions(identity: EpisodeIdentity, path: Path) -> dict:
    lock, engine, world, plan, tickets = _validate_plan_files(identity, path)
    directions_path = path / "scene-directions.json"
    directions = load_json(directions_path)
    validate_scene_directions(
        directions,
        lock,
        engine,
        world,
        plan,
        tickets,
        identity,
        lock_hash=sha256_file(path / "input-lock.json"),
        engine_hash=sha256_file(path / "episode-engine.json"),
        world_hash=sha256_file(path / "world.json"),
        plan_hash=sha256_file(path / "visual-plan.json"),
    )
    return directions


def cmd_validate_scene_directions(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(
        load_json(path / "production-state.json"), path, identity, "visual_plan_approved"
    )
    directions = _validated_scene_directions(identity, path)
    shot_count = sum(len(sequence["shots"]) for sequence in directions["sequences"])
    print(f"Validated scene directions: {path / 'scene-directions.json'}")
    print(f"Sequences: {len(directions['sequences'])}; shots: {shot_count}")
    print("Production state unchanged; this validation does not approve a greybox.")
    return 0


def cmd_build_scene_prompts(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state_through(
        load_json(path / "production-state.json"), path, identity, "visual_plan_approved"
    )
    directions = _validated_scene_directions(identity, path)
    outputs = build_scene_prompts(identity, path, directions)
    print(f"Generated build prompt manifest: {outputs[0]}")
    print(f"Shot build packets: {len(outputs) - 1}")
    print("Production state unchanged; build packets do not authorize media generation or canonical edits.")
    return 0


def _load_work(path: Path, work_id: str) -> dict:
    return load_json(path / "agents" / "work-orders" / f"{work_id}.json")


def cmd_validate_work_order(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    work = _load_work(path, args.work_order_id)
    validate_state_through(load_json(path / "production-state.json"), path, identity, work["required_gate"])
    validate_work_order(work, path)
    print(f"Validated work order: {path / 'agents' / 'work-orders' / (args.work_order_id + '.json')}")
    print("Blocking gate: worker packet validation; work order cannot advance canonical state")
    return 0


def cmd_validate_deliverable(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    work = _load_work(path, args.work_order_id)
    validate_state_through(load_json(path / "production-state.json"), path, identity, work["required_gate"])
    validate_work_order(work, path)
    deliverable_path = path / "agents" / "deliverables" / args.work_order_id / "deliverable.json"
    validate_deliverable(load_json(deliverable_path), work, path)
    print(f"Validated deliverable packet: {deliverable_path}")
    print("Blocking gate: serial root merge and canonical validation; no approval recorded")
    return 0


def cmd_work_status(args: argparse.Namespace) -> int:
    _, path, _ = _resolved(args.episode)
    orders = sorted((path / "agents" / "work-orders").glob("*.json"))
    if not orders:
        print("No work orders issued.")
        return 0
    failed = False
    for order_path in orders:
        work = load_json(order_path)
        work_id = work.get("work_order_id", order_path.stem)
        try:
            validate_work_order(work, path)
            order_status = "valid"
        except ValidationFailure as error:
            order_status = "invalid: " + "; ".join(error.errors)
            failed = True
        deliverable_path = path / "agents" / "deliverables" / work_id / "deliverable.json"
        if deliverable_path.is_file():
            try:
                validate_deliverable(load_json(deliverable_path), work, path)
                packet_status = "packet valid; no gate advanced"
            except ValidationFailure as error:
                packet_status = "packet rejected: " + "; ".join(error.errors)
                failed = True
        else:
            packet_status = "packet pending"
        print(f"{work_id}: {order_status}; {packet_status}")
    if failed:
        raise ValidationFailure("agent_packets", ["one or more work orders or packets failed"])
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    identity, path, _ = _resolved(args.episode)
    validate_state(load_json(path / "production-state.json"), path, identity)
    for output in generate_reviews(path):
        print(f"Review artifact: {output}")
    print(f"Current production state: {load_json(path / 'production-state.json')['current_stage']}")
    return 0


def cmd_lock_look(args: argparse.Namespace) -> int:
    episode = Path(args.episode_dir).resolve()
    references = []
    for value in args.ref:
        path, separator, url = value.partition("=")
        if not separator:
            raise ValueError(f"--ref must be path=url: {value}")
        references.append((Path(path).resolve(), url))
    lock = lock_look(episode, references, args.location, args.outfit, args.locked_by, args.supersede)
    print(f"Locked presenter look v{lock['version']}: {lock['location']} / {lock['outfit']}")
    print(f"Lock: {episode / 'presenter' / 'LOOK-LOCK.json'}")
    return 0


def cmd_look_status(args: argparse.Namespace) -> int:
    episode = Path(args.episode_dir).resolve()
    lock = check_look_lock(episode, {})
    print(f"Presenter look v{lock['version']} locked {lock['locked_at']} by {lock['locked_by']}")
    print(f"{lock['location']} / {lock['outfit']} ({len(lock['references'])} reference(s), all hashes match)")
    for old in lock.get("history", []):
        print(f"Superseded v{old['version']}: {old['reason']} ({old['presenter_jobs_orphaned']} presenter job(s) orphaned)")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    episode = Path(args.episode_dir).resolve()
    arguments = json.loads(Path(args.args[1:]).read_text() if args.args.startswith("@") else args.args)
    out_dir = Path(args.out).resolve() if args.out else episode / args.lane / "generated"
    result = generate(
        episode, args.provider, args.model, arguments, args.lane, args.item, args.reason,
        args.est_usd, out_dir, dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2))
    return 0


def cmd_board(args: argparse.Namespace) -> int:
    board = build_board(
        Path(args.build).resolve(), Path(args.plan).resolve(), Path(args.transcript).resolve(),
        Path(args.direction).resolve(), [Path(p).resolve() for p in args.lock or []],
        Path(args.out).resolve(), args.title,
    )
    states = {state: sum(1 for row in board["rows"] if row["state"] == state) for state in ("locked", "flagged", "unreviewed")}
    print(f"Board: {Path(args.out).resolve()} ({len(board['rows'])} segments; {states})")
    print(f"Board digest: {board['digest']}")
    return 0


def cmd_test(_: argparse.Namespace) -> int:
    print(f"Blueprint root: {BLUEPRINT_ROOT}")
    command = [sys.executable, "-m", "pytest", "-q"]
    result = subprocess.run(command, cwd=BLUEPRINT_ROOT, check=False)
    if result.returncode != 0:
        raise ValidationFailure("tests", [f"pytest exited {result.returncode}"])
    print("Blocking gate: none in test fixtures")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="oe-cinema")
    sub = root.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("episode_code")
    init.add_argument("slug")
    init.set_defaults(func=cmd_init)
    commands = {
        "status": cmd_status,
        "lock-inputs": cmd_lock_inputs,
        "validate-engine": cmd_validate_engine,
        "approve-engine": cmd_approve_engine,
        "validate-world": cmd_validate_world,
        "approve-world": cmd_approve_world,
        "validate-plan": cmd_validate_plan,
        "approve-plan": cmd_approve_plan,
        "build-greybox-data": cmd_build_greybox_data,
        "smoke-render": cmd_smoke_render,
        "validate-scene-directions": cmd_validate_scene_directions,
        "build-scene-prompts": cmd_build_scene_prompts,
        "work-status": cmd_work_status,
        "review": cmd_review,
    }
    for name, function in commands.items():
        command = sub.add_parser(name)
        command.add_argument("episode")
        command.set_defaults(func=function)
    director = sub.add_parser("build-director-prompts")
    director.add_argument("episode")
    director.add_argument(
        "--sequence",
        action="append",
        help="Generate only this exact sequence ID; repeat to select multiple sequences.",
    )
    director.set_defaults(func=cmd_build_director_prompts)
    for name, function in (("validate-work-order", cmd_validate_work_order), ("validate-deliverable", cmd_validate_deliverable)):
        command = sub.add_parser(name)
        command.add_argument("episode")
        command.add_argument("work_order_id")
        command.set_defaults(func=function)
    look = sub.add_parser("lock-look", help="Owner locks the episode's presenter look before any presenter generation.")
    look.add_argument("episode_dir")
    look.add_argument("--ref", action="append", required=True, help="Local reference image and its hosted URL: path=url.")
    look.add_argument("--location", required=True)
    look.add_argument("--outfit", required=True)
    look.add_argument("--locked-by", required=True)
    look.add_argument("--supersede", help="Reason for replacing an existing lock. Orphaned presenter jobs are recorded.")
    look.set_defaults(func=cmd_lock_look)
    look_status = sub.add_parser("look-status")
    look_status.add_argument("episode_dir")
    look_status.set_defaults(func=cmd_look_status)
    gen = sub.add_parser("generate", help="Run one gated, capped, ledgered Higgsfield or fal job.")
    gen.add_argument("episode_dir")
    gen.add_argument("--provider", required=True, choices=["higgsfield", "fal"])
    gen.add_argument("--model", required=True, help="Provider endpoint, e.g. fal-ai/veo3.1/fast.")
    gen.add_argument("--args", required=True, help="Provider arguments as JSON, or @file.json.")
    gen.add_argument("--lane", required=True, help="presenter, film, thumbnail, ... presenter requires a look lock.")
    gen.add_argument("--item", required=True, help="Stable output name, e.g. P03-take1.")
    gen.add_argument("--reason", required=True)
    gen.add_argument("--est-usd", type=float, required=True)
    gen.add_argument("--out", help="Output folder. Default: <episode_dir>/<lane>/generated.")
    gen.add_argument("--dry-run", action="store_true", help="Run the gates and cap check without spending.")
    gen.set_defaults(func=cmd_generate)
    board = sub.add_parser("board", help="Write one review page: the cut beside its plan, words, sources and status.")
    board.add_argument("--build", required=True, help="Assembly BUILD.json with per-segment rows and the output video.")
    board.add_argument("--plan", required=True, help="SHOT-PLAN.json.")
    board.add_argument("--transcript", required=True, help="Word transcript timed to the build's output.")
    board.add_argument("--direction", required=True, help="DIRECTION-PLAN.md with scene jobs and segment forms.")
    board.add_argument("--lock", action="append", help="Owner lock JSON whose protected ranges the board marks. Repeatable.")
    board.add_argument("--out", required=True, help="HTML path. A .json record with the digest is written beside it.")
    board.add_argument("--title", default="Episode review board")
    board.set_defaults(func=cmd_board)
    test = sub.add_parser("test")
    test.set_defaults(func=cmd_test)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (ValidationFailure, PathContractError, ValueError, OSError) as error:
        gate = getattr(error, "gate", args.command)
        print(f"FAILED — blocking gate: {gate}", file=sys.stderr)
        if isinstance(error, ValidationFailure):
            for item in error.errors:
                print(f"- {item}", file=sys.stderr)
        else:
            print(f"- {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
