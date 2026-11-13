"""Q5: Mutable defaults, independent orders, returns, and Python scope."""


def add_item_buggy(item: str, order: list[str] = []) -> list[str]:
    order.append(item)
    return order


def add_item(item: str, order: list[str] | None = None) -> list[str]:
    if order is None:
        order = []
    order.append(item)
    return order


def price_order(items: list[tuple[str, float]], *, gst_rate: float = 0.05) -> tuple[float, float]:
    subtotal = sum(price for _, price in items)
    gst = subtotal * gst_rate
    return subtotal + gst, gst


def scope_demo() -> tuple[int, int, int]:
    global GLOBAL_ORDERS
    GLOBAL_ORDERS += 1

    value = 10
    def outer() -> int:
        value = 20
        def inner() -> None:
            nonlocal value
            value += 1
        inner()
        return value
    return GLOBAL_ORDERS, value, outer()


GLOBAL_ORDERS = 0


def main() -> None:
    print("Buggy default shared across calls:", add_item_buggy("tea"), add_item_buggy("sandwich"))
    print("__defaults__ after calls:", add_item_buggy.__defaults__)
    customers = [
        add_item("tea"),
        add_item("coffee", order=[]),
        add_item(item="juice"),
    ]
    for number, order in enumerate(customers, start=1):
        print(f"customer {number}: {order}")
    print("total and GST:", price_order([("tea", 20.0), ("snack", 30.0)], gst_rate=0.05))
    print("global, local, nonlocal demo:", scope_demo())


if __name__ == "__main__":
    main()
