from typing import Literal
from pydantic import Field
from openpype.settings import BaseSettingsModel
from openpype.lib.postgres import Postgres


async def async_enum_resolver():
    """Return a list of project names."""
    return [row["name"] async for row in Postgres.iterate("SELECT name FROM projects")]


class ExampleSettingsSubmodel(BaseSettingsModel):

    # Compact layout is used, when a submodel has just a few
    # attributes, which may be displayed in a single row

    _layout = "compact"
    name: str = Field(..., title="Name")
    int_value: int = Field(..., title="Integer")
    enum: list[str] = Field(
        default_factory=list,
        title="Enum",
        enum_resolver=lambda: ["foo", "bar", "baz"],
    )


class ExampleSettings(BaseSettingsModel):
    """Test addon settings"""

    folder_type: str = Field(
        "Asset",
        title="Folder type",
    )
    textarea: str = Field(
        "",
        title="Textarea",
        widget="textarea",
    )

    # Simple enumerators can be defined using Literal type

    simple_enum: Literal["red", "green", "blue"] = Field(
        "foo",
        title="Simple enum",
    )

    # For more complex enumerators, use enum_resolver function
    # which returns a list of items. enum_resolver can be both
    # async or blocking.

    # section argument is used to visually separate fields of the form
    # a horizontal line with a label will be shown just above the field
    # with a section argument

    project: str | None = Field(
        None,
        enum_resolver=async_enum_resolver,
        title="Dynamic enum",
        section="Advanced types",
    )

    multiselect: list[str] = Field(
        default_factory=list,
        title="Multiselect",
        enum_resolver=lambda: ["foo", "bar", "baz"],
    )

    list_of_strings: list[str] = Field(
        default_factory=list,
        title="List of strings",
    )

    # Settings models can be nested

    list_of_submodels: list[ExampleSettingsSubmodel] = Field(
        default_factory=list,
        title="A list of compact objects",
    )
