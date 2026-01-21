from pydantic import ValidationError, validator

from ayon_server.settings import BaseSettingsModel, SettingsField


class ExampleSiteSettings(BaseSettingsModel):
    chair_orientation: str = SettingsField(
        "north",
        title="Chair orientation",
        description="The orientation of the chair",
        enum_resolver=lambda: ["north", "south", "east", "west"],
    )

    floor_material: str = SettingsField(
        "wood",
        title="Floor material",
        description="The material of the floor",
    )


    @validator("chair_orientation")
    @classmethod
    def validate_chair_orientation(cls, value):
        if value == "east":
            raise ValueError("East orientation is not allowed for the chair.")
        return value

