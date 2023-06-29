def export_csv(data):
    rows = []
    if isinstance(data, dict):
        row = []
        if "qid" in data:
            row.append(data["qid"])
        else:
            row.append("")
        if "details" in data:
            row.append(data["details"])
        else:
            row.append("")
        rows.append(row)
        for value in data.values():
            if isinstance(value, dict) or isinstance(value, list):
                rows.extend(export_csv(value))
            elif isinstance(value, str):
                rows[-1].append(value.encode("utf-8"))  # Encode the anstext field as bytes
    elif isinstance(data, list):
        for item in data:
            rows.extend(export_csv(item))
    return rows
