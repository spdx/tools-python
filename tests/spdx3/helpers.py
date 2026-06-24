from re import sub


def domain_enum_to_binding_name(enum_name: str) -> str:
    return sub(r"_+([a-z])", lambda m: m.group(1).upper(), enum_name.strip("_").lower())
