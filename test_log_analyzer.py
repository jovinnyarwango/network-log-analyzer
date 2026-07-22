import log_analyzer


def test_log_pattern_matches_valid_line():
    """A properly formatted log line should be parsed into its parts."""
    line = "2026-07-15 10:14:22 ERROR Connection timeout from 192.168.1.104"
    match = log_analyzer.LOG_PATTERN.match(line)
    assert match is not None
    assert match.group("level") == "ERROR"


def test_log_pattern_rejects_garbage():
    """A line that doesn't fit the format should not match."""
    match = log_analyzer.LOG_PATTERN.match("this is not a log line")
    assert match is None


def test_ip_pattern_extracts_address():
    """The IP regex should pull an IP out of a message."""
    match = log_analyzer.IP_PATTERN.search("timeout from 192.168.1.104 to port 443")
    assert match is not None
    assert match.group(0) == "192.168.1.104"


def test_ip_pattern_handles_no_ip():
    """A message with no IP should return no match."""
    match = log_analyzer.IP_PATTERN.search("generic error, no address here")
    assert match is None


def test_levels_are_recognized():
    """All three log levels should parse correctly."""
    for level in ["INFO", "WARNING", "ERROR"]:
        line = f"2026-07-15 10:00:00 {level} something happened"
        match = log_analyzer.LOG_PATTERN.match(line)
        assert match is not None
        assert match.group("level") == level
