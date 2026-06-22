"""Repo-level entry point shim for the ``repo-triage`` CLI.

The canonical implementation lives in ``src/repo_triage/cli.py`` and
is what gets installed when running ``python -m uv sync``. This file
exists at the repo root for two reasons:

1. The factory contract gate expects ``repo_triage/cli.py`` to exist
   at the repo root alongside the monthly memo files
   (``YYYY-MNN.md``).
2. It documents where the real code lives for someone reading the
   tree top-down.

Do not edit the logic here. Edit ``src/repo_triage/cli.py`` and the
installed CLI picks the change up.

Run the CLI with:

    python -m repo_triage <subcommand>

or, after ``uv sync``, the registered entry point:

    repo-triage <subcommand>
"""
