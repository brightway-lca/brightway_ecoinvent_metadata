from .lcia import get_lcia_units, get_lcia_cfs, get_lcia_categories
from .strategies import drop_selected_lci_results
from brightway_io.importers.base_lci import LCIImporter
from brightway_io.strategies import (
    drop_unspecified_subcategories,
    internal_linking,
    normalize_units,
    number_objects,
    drop_attribute,
    assign_no_uncertainty,
)
from brightway_io.utils import recursive_str_to_unicode, selection
from functools import partial
from lxml import objectify
from pathlib import Path


EMISSIONS_CATEGORIES = {"air": "emission", "soil": "emission", "water": "emission"}
SOURCE_DATA = Path(__file__, "..").resolve() / "source_data"


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

    def __init__(self, version, source_data=SOURCE_DATA):
        self.source_data = Path(source_data)
        self.version = version

        self.data["flows"] = self.extract_flows()
        self.data["collections"] = [{"id": 1, "name": f"ecoinvent {version} biosphere"}]
        self.data["methods"] = self.extract_methods()
        self.data["characterization factors"] = get_lcia_cfs(
            self.source_data, self.version
        )
        self.strategies = [
            drop_selected_lci_results,
            normalize_units,
            drop_unspecified_subcategories,
            partial(
                number_objects,
                key="characterization factors",
                sorting_fields=("method", "name", "categories"),
            ),
            partial(number_objects, key="methods", sorting_fields=("name",)),
            partial(number_objects, key="flows", sorting_fields=("name", "categories")),
            partial(
                number_objects,
                key="characterization factors",
                sorting_fields=("method_id", "flow_id"),
            ),
            partial(
                internal_linking,
                source_key="methods",
                target_key="characterization factors",
                link_field="method_id",
                source_fields=["name"],
                target_fields=["method"],
            ),
            partial(
                internal_linking,
                source_key="flows",
                target_key="characterization factors",
                link_field="flow_id",
                source_fields=["name", "categories"],
            ),
            partial(drop_attribute, key="characterization factors", attribute="method"),
            selection("characterization factors", assign_no_uncertainty),
        ]

    def extract_flows(self):
        fp = str(self.source_data / self.version / "ecoinvent elementary flows.xml")
        root = objectify.parse(open(fp, encoding="utf-8")).getroot()
        return recursive_str_to_unicode(
            [extract_flow_data(ds) for ds in root.iterchildren()]
        )

    def extract_methods(self):
        descriptions = {
            o["name"]: o["description"]
            for o in get_lcia_categories(self.source_data, self.version)
        }
        units = get_lcia_units(self.source_data, self.version)
        for obj in units:
            if obj["name"] in descriptions:
                obj["description"] = descriptions[obj["name"]]

        return units
