def indo(n):
    s = f"Rp{n:,.2f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")
