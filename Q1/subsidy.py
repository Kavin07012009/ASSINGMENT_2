"""Q1: Compare overlapping independent if statements with an exclusive chain."""


def separate_if(units: int, ration_card: bool, age_over_80: bool) -> list[str]:
    """Intentionally flawed version: broad conditions can award two benefits."""
    results = []
    if units <= 100:
        results.append("Full subsidy")
    if units <= 200 and ration_card:
        results.append("Partial subsidy")
    if units > 200 and age_over_80:
        results.append("Senior exception subsidy")
    if not results:
        results.append("No subsidy")
    return results


def exclusive_decision(units: int, ration_card: bool, age_over_80: bool) -> str:
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200 and ration_card:
        return "Partial subsidy"
    elif units > 200 and age_over_80:
        return "Senior exception subsidy"
    else:
        return "No subsidy"


def match_decision(units: int, ration_card: bool, age_over_80: bool) -> str:
    # Match guards retain the full meaning of the input conditions.
    match units:
        case n if n <= 100:
            return "Full subsidy"
        case n if 101 <= n <= 200 and ration_card:
            return "Partial subsidy"
        case n if n > 200 and age_over_80:
            return "Senior exception subsidy"
        case _:
            return "No subsidy"


def lookup_decision(units: int, ration_card: bool, age_over_80: bool) -> str:
    # Slab selection is O(k) in the number of entries; exception rules are guards.
    for upper, label in [(100, "Full subsidy"), (200, "Partial subsidy")]:
        if units <= upper:
            if upper == 100:
                return label
            return label if ration_card else "No subsidy"
    return "Senior exception subsidy" if age_over_80 else "No subsidy"


def main() -> None:
    cases = [
        (99, False, False), (100, True, False), (101, False, False),
        (101, True, False), (199, True, False), (200, False, False),
        (201, False, False), (201, False, True),
    ]
    print("units card age80 | separate-if | if-elif-else | match | lookup")
    for units, card, senior in cases:
        print(f"{units:>5} {str(card):>4} {str(senior):>6} | "
              f"{separate_if(units, card, senior)} | "
              f"{exclusive_decision(units, card, senior)} | "
              f"{match_decision(units, card, senior)} | "
              f"{lookup_decision(units, card, senior)}")


if __name__ == "__main__":
    main()
