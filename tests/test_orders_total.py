"""Order line totals."""

from app import orders


def test_line_total_is_not_unit_prices_only():
    total = orders.calculate_total(
        [
            {"price": 10.0, "qty": 3},
            {"price": 2.5, "qty": 2},
        ]
    )
    # Summing unit prices and ignoring qty yields 12.5.
    assert total != 12.5
