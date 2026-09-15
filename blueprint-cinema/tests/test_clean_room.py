from __future__ import annotations

import copy

import pytest

from blueprint_cinema.validation import ValidationFailure, validate_clean_room


def test_current_episode_configuration_is_clean_room(current_artifacts):
    validate_clean_room(list(current_artifacts.values()))


@pytest.mark.parametrize(
    "reference",
    [
        "studio/originate/example/storyboard.json",
        "studio/originate/example/coverage_map.json",
        "studio/originate/example/render_data/blueprint.json",
        "studio/remotion/src/oe/OEOpeningPilot.tsx",
        "studio/originate/example/resolve_pilot/review.mp4",
    ],
)
def test_prohibited_legacy_references_fail(reference):
    with pytest.raises(ValidationFailure, match="prohibited legacy reference"):
        validate_clean_room({"input": reference})

