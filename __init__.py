from typing import Any, Type

from fastapi import Depends
from pydantic import Field

from openpype.addons import BaseServerAddon
from openpype.api.dependencies import dep_project_name, dep_current_user
from openpype.entities import FolderEntity, UserEntity
from openpype.exceptions import NotFoundException
from openpype.lib.postgres import Postgres
from openpype.settings import BaseSettingsModel



class ExampleSettings(BaseSettingsModel):
    """Test addon settings"""

    folder_type: str = Field("Asset", title="Folder type")


class ExampleAddon(BaseServerAddon):
    name = "example"
    title = "Example addon"
    version = "1.0.0"
    settings_model: Type[ExampleSettings] = ExampleSettings
    frontend_scopes: dict[str, Any] = {"project": {"sidebar": "hierarchy"}}

    def setup(self):
        self.add_endpoint(
            "get-random-folder/{project_name}",
            self.get_random_folder,
            method="GET",
        )

    async def get_random_folder(
        self,
        user: UserEntity = Depends(dep_current_user),
        project_name: str = Depends(dep_project_name),
    ):
        """Return a random folder from the database"""

        settings = await self.get_project_settings(project_name)
        assert settings is not None  # Keep mypy happy

        #
        # Get a random folder id from the project
        #

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

        #
        # Load the folder and return it
        #

        folder = await FolderEntity.load(project_name, folder_id)
        return folder.payload

        # Optionally you can use:
        #
        # folder.ensure_read_access(user)
        # return folder.as_user(user)
