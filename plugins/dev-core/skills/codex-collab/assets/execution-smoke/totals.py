def total_cents(lines):
    return sum(line["unit_price_cents"] for line in lines)
