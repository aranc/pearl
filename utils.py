def extract_func_and_args(s):
    if "(" not in s:
        return s, None
    if ")" not in s:
        return s, None

    a = s.index("(") + 1
    b = s.rindex(")")

    assert b >= a

    if a == b or s[a, b].strip() == "":
        return s[:s.index("(")], None

    return s[:s.index("(")], s[a,b]
