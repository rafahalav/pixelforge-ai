import pytest

from core.prompt_engine import PromptEngineer


def test_build_complete_prompt():

    prompt = PromptEngineer.build_prompt(
        subject="A futuristic digital art studio",
        composition="Wide horizontal composition",
        style="Premium cinematic digital art",
        lighting="Soft neon lighting",
        colors="Dark navy, cyan and electric blue",
        required_elements="Glowing digital core and neural networks"
    )

    assert "Subject:" in prompt
    assert "Composition:" in prompt
    assert "Visual style:" in prompt
    assert "Lighting and atmosphere:" in prompt
    assert "Color palette:" in prompt
    assert "Required elements:" in prompt


def test_build_partial_prompt():

    prompt = PromptEngineer.build_prompt(
        subject="A futuristic city",
        style="Cyberpunk"
    )

    assert "Subject:" in prompt
    assert "Visual style:" in prompt
    assert "Composition:" not in prompt


def test_subject_is_required():

    with pytest.raises(ValueError):
        PromptEngineer.build_prompt(
            subject=""
        )


def test_prompt_length_limit():

    with pytest.raises(ValueError):
        PromptEngineer.build_prompt(
            subject="A" * 2100
        )
