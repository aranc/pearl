def extract_func_and_args(s):
    if "(" not in s:
        return None
    if ")" not in s:
        return None

    return s[:s.index("(")], s[s.index("("), s.rindex(")")]
