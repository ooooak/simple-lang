_default:
    @just --list

run:
    uv run ./lang/main.py ./resources/main.rb

sync:
    uv sync
