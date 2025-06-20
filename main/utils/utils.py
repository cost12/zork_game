def list_to_str(lis:list[str]) -> str:
    if len(lis) == 0:
        return ""
    if len(lis) == 1:
        return lis[0]
    if len(lis) == 2:
        return f"{lis[0]} and {lis[1]}"
    return ", ".join(lis[:-1]) + f", and {lis[-1]}"