from typing import Any, Type

from fastapi import Depends
from nxtools import logging

from ayon_server.addons import BaseServerAddon, AddonLibrary
from ayon_server.api.dependencies import dep_current_user, dep_project_name
from ayon_server.entities import FolderEntity, UserEntity
from ayon_server.exceptions import NotFoundException
from ayon_server.lib.postgres import Postgres

from .settings import ExampleSettings
from .site_settings import ExampleSiteSettings


class ExampleAddon(BaseServerAddon):
    name = "example"
    title = "Example addon"
    version = "1.0.0"
    settings_model: Type[ExampleSettings] = ExampleSettings
    site_settings_model: Type[ExampleSiteSettings] = ExampleSiteSettings

    # frontend_scopes defines, where the web frontend of the addon
    # should be displayed in openpype web app. Currently only "project"
    # is supported. Additional arguments may be passed (in this case)
    # to show the project hierarchy sidebar. This feature is not yet
    # fully functional and will be changed in the future.

    frontend_scopes: dict[str, Any] = {"project": {"sidebar": "hierarchy"}}
    services = {"SplinesReticulator": {"image": "bfirsh/reticulate-splines"}}

    # intitalize method is called during the addon initialization
    # You can use it to register its custom REST endpoints

    def initialize(self):
        logging.info("Example addon INIT")
        self.add_endpoint(
            "get-random-folder/{project_name}",
            self.get_random_folder,
            method="GET",
        )

    async def setup(self):
        """Setup method is called after the addon is registered"""
        logging.info("Example addon is ready to use")
        all_addons: list[str] = [name for name, _ in AddonLibrary.items()]
        logging.info(f"All addons as example addons sees them: {all_addons}")

        # If the addon makes a change in server configuration,
        # e.g. adding a new attribute, you may trigger a server
        # restart by calling self.restart_server()
        # Use it with caution and only when necessary!
        # You don't want to restart the server every time the addon is loaded.

        # self.request_server_restart()

    # Example REST endpoint
    # Depends(dep_current_user) ensures the request is authenticated

    async def get_random_folder(
        self,
        user: UserEntity = Depends(dep_current_user),
        project_name: str = Depends(dep_project_name),
    ):
        """Return a random folder from the database"""

        settings = await self.get_project_settings(project_name)
        assert settings is not None  # Keep mypy happy

        # Get a random folder id from the project
        try:
            result = await Postgres.fetch(
                f"""
                SELECT id FROM project_{project_name}.folders
                WHERE folder_type = $1
                ORDER BY RANDOM() LIMIT 1
                """,
                settings.folder_type,
            )
        except Postgres.UndefinedTableError:
            raise NotFoundException(f"Project {project_name} not found")

        try:
            folder_id = result[0]["id"]
        except IndexError:
            raise NotFoundException("No folder found")

        # Load the folder entity

        folder = await FolderEntity.load(project_name, folder_id)

        # ensure_read_access method raises ForbiddenException, when the user
        # does not have rights to view the folder.

        await folder.ensure_read_access(user)

        # FolderEntity.as_user returns the folder (similarly to folder.payload)
        # but it respects the user access level (so it may hide certain attributes)
        return folder.as_user(user)
