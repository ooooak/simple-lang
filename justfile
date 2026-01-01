_default:
    @just --list

run:
    uv run main.py ./resources/main.rb

sync:
    uv sync
