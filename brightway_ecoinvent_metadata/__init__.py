__version__ = (0, 1)
__all__ = (
    "add_ecoinvent_metadata",
    "EcoinventMetadataImporter",
    "generate_ecoinvent_metadata",
)

from .importer import EcoinventMetadataImporter
from bw_projects import projects
from bw_default_backend.io import insert_existing_database
from pathlib import Path
import bw_default_backend as backend


LATEST = "3.6"


def add_ecoinvent_metadata(version=LATEST):
    assert backend.UncertaintyType.select().count(), "Must create project with `add_base_data=True`"
    filepath = (
        Path(__file__, "..").resolve() / "data" / f"ecoinvent_metadata.{version}.db"
    )
    insert_existing_database(filepath)


def generate_ecoinvent_metadata(
    version=LATEST, temp_project="__ecoinvent_metadata_temp__", source_data=None
):
    if not source_data:
        # Requires ``source_data`` branch checkout
        source_data = Path(__file__, "..").resolve() / "source_data"

    if temp_project in projects:
        projects.delete_project(temp_project)
    projects.create_project(temp_project, add_base_data=True)

    backend.Location.delete().execute()
    backend.Geocollection.delete().execute()

    ei = EcoinventMetadataImporter(source_data=source_data, version=version)
    ei.apply_strategies()
    backend.create(ei.data)
