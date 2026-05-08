"""Tests for logging configuration side effects."""

from pathlib import Path

from perplexity.logger import setup_logger


def test_setup_logger_does_not_create_cwd_log_file(tmp_path, monkeypatch) -> None:
    print("console.log -> ensuring default logger does not create cwd log file")
    monkeypatch.chdir(tmp_path)

    logger = setup_logger("perplexity.test.no_file")
    logger.info("hello")

    assert not Path("perplexity.log").exists()


def test_setup_logger_can_write_explicit_log_file(tmp_path) -> None:
    print("console.log -> ensuring explicit log file still works")
    log_file = tmp_path / "custom.log"

    logger = setup_logger("perplexity.test.file", log_file=str(log_file), console=False)
    logger.info("hello")

    assert log_file.exists()
    assert "hello" in log_file.read_text(encoding="utf-8")
