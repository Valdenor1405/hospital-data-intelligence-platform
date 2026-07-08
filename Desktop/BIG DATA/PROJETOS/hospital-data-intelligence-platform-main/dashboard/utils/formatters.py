def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(value):
    return f"{int(value):,}".replace(",", ".")


def format_percent(value):
    return f"{value:.2f}%"