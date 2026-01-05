"""
Property tests for development scripts.

Feature: project-initialization, Property 2: Script Executability
Validates: Requirements 6.6
"""

import os
import stat
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st


# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


def get_script_files() -> list[Path]:
    """Get all shell script files in the scripts directory."""
    scripts_dir = PROJECT_ROOT / "scripts"
    if not scripts_dir.exists():
        return []
    return [f for f in scripts_dir.iterdir() if f.suffix == ".sh" and f.is_file()]


def has_execute_permission(file_path: Path) -> bool:
    """Check if a file has execute permissions."""
    mode = file_path.stat().st_mode
    # Check if any execute bit is set (owner, group, or other)
    return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


class TestScriptExecutability:
    """Property tests for script executability."""

    # Feature: project-initialization, Property 2: Script Executability
    # Validates: Requirements 6.6
    @settings(max_examples=100)
    @given(script_index=st.integers(min_value=0, max_value=100))
    def test_all_scripts_are_executable(self, script_index: int) -> None:
        """
        For any shell script in the scripts/ directory, the file SHALL have
        execute permissions (mode includes 0o111).

        Property 2: Script Executability
        Validates: Requirements 6.6
        """
        scripts = get_script_files()
        if not scripts:
            pytest.skip("No scripts found in scripts/ directory")

        # Use modulo to select a script from the available ones
        script = scripts[script_index % len(scripts)]

        assert has_execute_permission(script), (
            f"Script {script.name} does not have execute permissions. "
            f"Current mode: {oct(script.stat().st_mode)}"
        )

    def test_expected_scripts_exist(self) -> None:
        """Verify all expected scripts are present."""
        expected_scripts = [
            "setup.sh",
            "run.sh",
            "test.sh",
            "migrate.sh",
            "terraform.sh",
        ]

        scripts_dir = PROJECT_ROOT / "scripts"
        assert scripts_dir.exists(), "scripts/ directory does not exist"

        for script_name in expected_scripts:
            script_path = scripts_dir / script_name
            assert script_path.exists(), f"Expected script {script_name} not found"

    def test_all_expected_scripts_are_executable(self) -> None:
        """Verify all expected scripts have execute permissions."""
        expected_scripts = [
            "setup.sh",
            "run.sh",
            "test.sh",
            "migrate.sh",
            "terraform.sh",
        ]

        scripts_dir = PROJECT_ROOT / "scripts"

        for script_name in expected_scripts:
            script_path = scripts_dir / script_name
            if script_path.exists():
                assert has_execute_permission(script_path), (
                    f"Script {script_name} does not have execute permissions"
                )

    def test_scripts_have_shebang(self) -> None:
        """Verify all scripts start with a proper shebang."""
        scripts = get_script_files()

        for script in scripts:
            content = script.read_text()
            assert content.startswith("#!/bin/bash"), (
                f"Script {script.name} does not start with #!/bin/bash shebang"
            )
