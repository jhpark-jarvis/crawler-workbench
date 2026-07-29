"""Shared SQLite connection and transaction helpers for crawler-workbench."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Any


def connect(database_path: str | Path, *, timeout_seconds: float = 5.0) -> sqlite3.Connection:
    """Open a SQLite connection configured for local crawler workloads."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path, timeout=timeout_seconds)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 5000")
    return connection


@contextmanager
def transaction(connection: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Commit on success and rollback when the caller raises an exception."""
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()


def execute(
    connection: sqlite3.Connection,
    statement: str,
    parameters: Sequence[Any] = (),
) -> sqlite3.Cursor:
    """Execute one parameterized SQL statement without implicitly committing."""
    return connection.execute(statement, parameters)


def execute_many(
    connection: sqlite3.Connection,
    statement: str,
    parameters: Sequence[Sequence[Any]],
) -> sqlite3.Cursor:
    """Execute one parameterized SQL statement for multiple rows."""
    return connection.executemany(statement, parameters)
