from collections import Counter


def summarize_inventory(items):
    counts = Counter(item.name for item in items)
    return [(name, count) for name, count in counts.items()]


def get_item_by_display_index(items, choice):
    grouped = summarize_inventory(items)
    if not 1 <= choice <= len(grouped):
        return None

    selected_name = grouped[choice - 1][0]
    for item in items:
        if item.name == selected_name:
            return item
    return None
