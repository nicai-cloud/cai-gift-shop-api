from decimal import Decimal, ROUND_HALF_UP

def format_number(price: Decimal) -> str:
    price_with_decimal = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{price_with_decimal:,.2f}"
