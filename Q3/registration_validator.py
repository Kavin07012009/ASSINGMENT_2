"""Q3: Normalize and validate Indian-style registration strings without regex."""


def normalize(raw: str) -> str:
    # Permitted separators are spaces and hyphens; split/join removes all spaces.
    compact = "".join(raw.strip().upper().replace("-", " ").split())
    return compact


def is_valid(raw: str) -> bool:
    reg = normalize(raw)
    if len(reg) not in (9, 10):
        return False
    series_length = len(reg) - 8
    return (
        reg[0:2].isalpha()
        and reg[2:4].isdigit()
        and reg[4:4 + series_length].isalpha()
        and reg[-4:].isdigit()
    )


def receipt_format(raw: str) -> str:
    reg = normalize(raw)
    if not is_valid(reg):
        raise ValueError(f"Invalid registration: {raw!r}")
    series_end = len(reg) - 4
    return f"{reg[:2]} {reg[2:4]} {reg[4:series_end]} {reg[-4:]}"


def main() -> None:
    samples = ["tn 09 ab 1234", "TN-09-AB-1234", "Tn09Ab1234",
               "MH 12 C 9876", "A 09 AB 1234", "TN-9-AB-1234"]
    print("input | normalized | valid | receipt")
    for sample in samples:
        reg = normalize(sample)
        print(f"{sample!r} | {reg} | {is_valid(sample)} | "
              f"{receipt_format(sample) if is_valid(sample) else '-'}")
    nine = "TN09A1234"
    ten = "TN09AB1234"
    print("9-char suffix/prefix:", nine[-4:], nine[4:-4])
    print("10-char suffix/prefix:", ten[-4:], ten[4:-4])
    text = "tn09ab1234"
    text.upper()
    print("upper() without reassignment:", text)


if __name__ == "__main__":
    main()
