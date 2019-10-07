from brightway_io.importers.base_lci import LCIImporter
from brightway_io.strategies import drop_unspecified_subcategories, normalize_units
from brightway_io.utils import recursive_str_to_unicode
from lxml import objectify
from pathlib import Path


from ..strategies import (
    drop_unspecified_subcategories,
    link_iterable_by_fields,
    normalize_units,
    rationalize_method_names,
    set_biosphere_type,
)
from numbers import Number
import warnings


EMISSIONS_CATEGORIES = {"air": "emission", "soil": "emission", "water": "emission"}


def extract_flow_data(o):
    ds = {
        "categories": (
            o.compartment.compartment.text,
            o.compartment.subcompartment.text,
        ),
        "uuid": o.get("id"),
        "name": o.name.text,
        "unit": o.unitName.text,
        "location": None,
        "collection": 1,
    }
    ds["kind"] = EMISSIONS_CATEGORIES.get(ds["categories"][0], ds["categories"][0])
    return ds


class EcoinventMetadataImporter(LCIImporter):
    format = "Ecoinvent XML"

    def __init__(self, source_data, version):
        self.source_data = Path(source_data)
        self.version = version

        self.data["flows"] = self.extract_flows()
        self.data["collections"] = [{"id": 1, "name": f"ecoinvent {version} biosphere"}]
        self.strategies = [
            normalize_units,
            drop_unspecified_subcategories,
            # functools.partial(link_iterable_by_fields,
            #     other=Database(config.biosphere),
            #     fields=('name', 'categories')
            # ),
        ]

    def extract_flows(self):
        fp = str(self.source_data / version / "ecoinvent elementary flows.xml")
        root = objectify.parse(open(fp, encoding="utf-8")).getroot()
        return recursive_str_to_unicode(
            [extract_flow_data(ds) for ds in root.iterchildren()]
        )

    def separate_methods(self):
        """Separate the list of CFs into distinct methods"""
        methods = {obj["method"] for obj in self.cf_data}
        metadata = {obj["name"]: obj for obj in self.csv_data}

        self.data = {}

        missing = set()

        for line in self.cf_data:
            if line["method"] not in self.units:
                missing.add(line["method"])

        if missing:
            _ = lambda x: sorted([str(y) for y in x])
            warnings.warn("Missing units for following:" + " | ".join(_(missing)))

        for line in self.cf_data:
            assert isinstance(line["amount"], Number)

            if line["method"] not in self.data:
                self.data[line["method"]] = {
                    "filename": self.file,
                    "unit": self.units.get(line["method"], ""),
                    "name": line["method"],
                    "description": "",
                    "exchanges": [],
                }

            self.data[line["method"]]["exchanges"].append(
                {
                    "name": line["name"],
                    "categories": line["categories"],
                    "amount": line["amount"],
                }
            )

        self.data = list(self.data.values())

        for obj in self.data:
            obj.update(metadata.get(obj["name"], {}))
