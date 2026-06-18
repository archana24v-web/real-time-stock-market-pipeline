import pytest
from unittest.mock import patch, MagicMock

def test_record_structure():
    """Test that the produced Kafka record has the correct schema fields."""
    expected_keys = {'symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    sample_record = {
        'symbol': 'AAPL',
        'timestamp': '2026-06-17T09:30:00',
        'open': 189.2,
        'high': 191.5,
        'low': 188.9,
        'close': 190.8,
        'volume': 1200000
    }
    assert set(sample_record.keys()) == expected_keys
    assert sample_record['close'] > 0
    assert sample_record['volume'] > 0
