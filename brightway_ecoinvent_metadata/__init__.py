__version__ = (0, 1)
__all__ = (
    "add_ecoinvent_metadata",
    "EcoinventMetadataImporter",
    "generate_ecoinvent_metadata",
)

from .importer import EcoinventMetadataImporter
from pathlib import Path
from bw_default_backend.io import insert_existing_database

LATEST = "3.6"


def add_ecoinvent_metadata(version=LATEST):
    filepath = (
        Path(__file__, "..").resolve() / "data" / f"ecoinvent_metadata.{version}.db"
    )
    insert_existing_database(filepath)


def generate_ecoinvent_metadata(
    version=LATEST, temp_project="__ecoinvent_metadata_temp__", source_data=None
):
    import bw_default_backend as backend
    from brightway_projects import projects

    if not source_data:
        # Requires ``source_data`` branch checkout
        source_data = Path(__file__, "..").resolve() / "source_data"

    assert temp_project not in projects
    projects.create(temp_project)

    backend.Location.delete().execute()
    backend.Geocollection.delete().execute()

    ei = EcoinventMetadataImporter(source_data=source_data, version=version)
    ei.apply_strategies()
    backend.create(ei.data)
