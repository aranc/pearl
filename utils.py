def extract_func_and_args(s):
    if "(" not in s:
        return s.strip(), None
    if ")" not in s:
        return s.strip(), None

    a = s.index("(") + 1
    b = s.rindex(")")

    assert b >= a

    if a == b or s[a:b].strip() == "":
        return s[:s.index("(")].strip(), None

    return s[:s.index("(")].strip(), s[a:b].strip()
