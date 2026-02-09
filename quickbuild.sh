uv venv
uv sync
python3 -m build
uv pip install dist/dinodex-0.1.0-py3-none-any.whl
uv run dinodex --help