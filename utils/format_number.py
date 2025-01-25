from decimal import Decimal, ROUND_HALF_UP

def format_number(obj: Decimal) -> str:
    return str(obj.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
