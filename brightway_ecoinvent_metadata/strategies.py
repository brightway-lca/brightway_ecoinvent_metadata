EXCLUDED = {"selected LCI results, additional", "selected LCI results"}


def drop_selected_lci_results(data):
    data["methods"] = [obj for obj in data["methods"] if obj["name"][0] not in EXCLUDED]
    data["characterization factors"] = [
        obj
        for obj in data["characterization factors"]
        if obj["method"][0] not in EXCLUDED
    ]
    return data
