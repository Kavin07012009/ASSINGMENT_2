"""Q2: OTP attempt loops, control statements, loop-else, and recursion."""

OTP = "482913"


def verify_while(entries: list[str], otp: str = OTP) -> tuple[bool, int, bool]:
    attempts = 0
    index = 0
    locked = False
    while attempts < 3:
        if index >= len(entries):
            break
        entered = entries[index]
        index += 1
        if entered.strip() == "":
            print("Blank entry: not counted")
            continue
        attempts += 1
        if entered == otp:
            print(f"Verified on attempt {attempts}")
            break
        print(f"Wrong OTP ({attempts}/3)")
    else:
        locked = True
        print("Loop else: account locked for 30 minutes")
    return attempts > 0 and index > 0 and any(e == otp for e in entries[:index]), attempts, locked


def verify_for(entries: list[str], otp: str = OTP) -> tuple[bool, int, bool]:
    attempts = 0
    index = 0
    locked = False
    for _ in range(3):
        if index >= len(entries):
            break
        entered = entries[index]
        index += 1
        if entered.strip() == "":
            print("Blank entry: not counted")
            continue
        attempts += 1
        if entered == otp:
            print(f"Verified on attempt {attempts}")
            break
        print(f"Wrong OTP ({attempts}/3)")
    else:
        locked = True
        print("Loop else: account locked for 30 minutes")
    # pass is a legal no-op for a deliberately empty policy branch.
    if not locked:
        pass
    return any(e == otp for e in entries[:index]), attempts, locked


def verify_with_security(entries: list[str], security_answer: str, otp: str = OTP) -> tuple[bool, int, bool]:
    """After three failures, a correct answer unlocks two additional attempts."""
    attempts = 0
    index = 0
    max_attempts = 3
    unlocked = False
    while attempts < max_attempts:
        if index >= len(entries):
            break
        entered = entries[index]
        index += 1
        if not entered.strip():
            continue
        attempts += 1
        if entered == otp:
            return True, attempts, False
        if attempts == 3 and security_answer.lower() == "blue":
            max_attempts += 2
            unlocked = True
            print("Security answer accepted: two extra attempts")
    else:
        return False, attempts, True
    return False, attempts, False


def verify_recursive(entries: list[str], index: int = 0, attempts: int = 0,
                     otp: str = OTP) -> tuple[bool, int, bool]:
    if attempts >= 3:
        return False, attempts, True
    if index >= len(entries):
        return False, attempts, False
    entered = entries[index]
    if not entered.strip():
        return verify_recursive(entries, index + 1, attempts, otp)
    if entered == otp:
        return True, attempts + 1, False
    return verify_recursive(entries, index + 1, attempts + 1, otp)


def main() -> None:
    print("WHILE: blank, wrong, wrong, correct")
    print("result:", verify_while(["", "111111", "000000", OTP]))
    print("FOR: three wrong")
    print("result:", verify_for(["111111", "000000", "222222"]))
    print("Changed rule:", verify_with_security(["1", "2", "3", "4", OTP], "blue"))
    print("Recursive three wrong:", verify_recursive(["1", "2", "3"]))


if __name__ == "__main__":
    main()
