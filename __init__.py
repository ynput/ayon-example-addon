from typing import Any, Type

from fastapi import Depends

from openpype.addons import BaseServerAddon
from openpype.api.dependencies import dep_current_user, dep_project_name
from openpype.entities import FolderEntity, UserEntity
from openpype.exceptions import NotFoundException
from openpype.lib.postgres import Postgres

from .settings import ExampleSettings


class ExampleAddon(BaseServerAddon):
    name = "example"
    title = "Example addon"
    version = "1.0.0"
    settings_model: Type[ExampleSettings] = ExampleSettings

    # frontend_scopes defines, where the web frontend of the addon
    # should be displayed in openpype web app. Currently only "project"
    # is supported. Additional arguments may be passed (in this case)
    # to show the project hierarchy sidebar. This feature is not yet
    # fully functional and will be changed in the future.

    frontend_scopes: dict[str, Any] = {"project": {"sidebar": "hierarchy"}}
    services = {
        "SplinesReticulator" : {"image": "bfirsh/reticulate-splines"}
    }

    # Setup method is called during the addon initialization
    # You can use it to register its custom REST endpoints

    def setup(self):
        self.add_endpoint(
            "get-random-folder/{project_name}",
            self.get_random_folder,
            method="GET",
        )

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

        folder.ensure_read_access(user)

        # FolderEntity.as_user returns the folder (similarly to folder.payload)
        # but it respects the user access level (so it may hide certain attributes)
        return folder.as_user(user)
