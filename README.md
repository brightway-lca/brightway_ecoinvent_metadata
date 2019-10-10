# Brightway ecoinvent metadata

This package provides metadata based on the `ecoinvent database <https://www.ecoinvent.org/>`__ for life cycle assessment for use in the Brightway framework.

Uses ``brightway_projects`` and ``bw_default_backend``.

## Installation

Install via ``pip`` or ``conda`` (``conda install -c cmutel brightway_ecoinvent_metadata``).

## Usage

After first creating a new project:

    from brightway_ecoinvent_metadata import add_ecoinvent_metadata
    add_ecoinvent_metadata()

## Development

Check out the ``dev`` branch to see the source data files.

A complete source clone require `git large file storage <https://git-lfs.github.com/>`__.

To regenerate the metadata database, run the following in a new project:

    from brightway_ecoinvent_metadata import EcoinventMetadataImporter
    import bw_default_backend as backend
    from brightway_projects import projects

    # Change as desired
    temp_project = "__ecoinvent_metadata_temp__"
    projects.create(temp_project)
    version = "3.6" # Or whatever
    ei = EcoinventMetadataImporter(version=version)
    ei.apply_strategies()
    backend.create(ei.data)
