def indo(n):
    s = f"{n:,.2f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")
