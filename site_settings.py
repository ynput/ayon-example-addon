from pydantic import Field

from ayon_server.settings import BaseSettingsModel
from ayon_server.settings.enum import folder_types_enum


class ExampleSiteSettings(BaseSettingsModel):
    chair_orientation: str = Field(
        "north",
        title="Chair orientation",
        description="The orientation of the chair",
        enum_resolver=lambda: ["north", "south", "east", "west"],
    )

    floor_material: str = Field(
        "wood",
        title="Floor material",
        description="The material of the floor",
    )
