from typing import Annotated

import pytest
from charmcli import Charmcli, CharmHelpFormatter, CommandInfo


class TestCharmcliFramework:
    def test_initialization(self):
        """Test basic initialization of Charmcli"""
        cli = Charmcli(help="Test help", epilog="Test epilog")
        assert cli.parser.description == "Test help"
        assert cli.parser.epilog == "Test epilog"
        assert isinstance(cli.parser.formatter_class, type(CharmHelpFormatter))
        assert len(cli.commands) == 0

    def test_command_registration(self):
        """Test that commands are properly registered"""
        cli = Charmcli()

        @cli.command()
        def test_command(arg1: str, arg2: int):
            pass

        assert "test-command" in cli.commands
        cmd_info = cli.commands["test-command"]
        assert isinstance(cmd_info, CommandInfo)
        assert cmd_info.name == "test-command"
        assert cmd_info.command == test_command

    def test_command_with_annotated_args(self):
        """Test command with Annotated type hints"""
        cli = Charmcli()

        @cli.command()
        def annotated_cmd(
            name: Annotated[str, "The name to use"],
            count: Annotated[int, "The count"] = 1,
        ):
            pass

        assert "annotated-cmd" in cli.commands

    def test_required_annotations(self):
        """Test that functions without annotations are rejected"""
        cli = Charmcli()

        with pytest.raises(ValueError, match="Function must have type annotations"):

            @cli.command()
            def no_annotations(arg):
                pass
