def camelize(data: dict | list):
    if isinstance(data, list):
        new_data = []

        for v in data:
            if isinstance(v, dict | list):
                v = camelize(v)

            new_data.append(v)
    else:
        new_data = {} # type: ignore
        for k, v in data.items():
            parts = k.split("_")

            k = f"{parts[0]}{''.join(p.title() for p in parts[1:])}"

            if isinstance(v, dict | list):
                v = camelize(v)

            new_data[k] = v

    return new_data
