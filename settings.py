from typing import Literal

from pydantic import Field, validator

from openpype.lib.postgres import Postgres
from openpype.settings import BaseSettingsModel, ensure_unique_names, normalize_name


async def async_enum_resolver():
    """Return a list of project names."""
    return [row["name"] async for row in Postgres.iterate("SELECT name FROM projects")]


def enum_resolver():
    """Return a list of value/label dicts for the enumerator.

    Returning a list of dicts is used to allow for a custom label to be
    displayed in the UI.
    """
    return [{"value": f"value{i}", "label": f"Label {i}"} for i in range(10)]


class NestedSettings(BaseSettingsModel):
    """Nested settings without grouping

    Submodels also support docstrings, which are propagated
    to the frontend. Just be aware a description attribute on
    the parent field will override the docstring.

    Docstring can be splitted to multiple paragraph simply
    by adding an empty line.
    """

    spam: bool = Field(False, title="Spam")
    eggs: bool = Field(False, title="Eggs")
    bacon: bool = Field(False, title="Bacon")


class GroupedSettings(BaseSettingsModel):
    _isGroup = True
    your_name: str = Field("", title="Name")
    your_quest: str = Field("", title="Your quest")
    favorite_color: str = Field(
        "red",
        title="Favorite color",
        enum_resolver=lambda: ["red", "green", "blue"],
    )


class CompactListSubmodel(BaseSettingsModel):

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

    @validator("name")
    def validate_name(cls, value):
        """Ensure name does not contain weird characters"""
        return normalize_name(value)


class DictLikeSubmodel(BaseSettingsModel):
    _layout = "expanded"

    name: str = Field(..., title="Name")
    value1: str = Field("", title="Value 1")
    value2: str = Field("", title="Value 2")
    value3: str = Field("", title="Value 3")
    value4: str = Field("", title="Value 4")

    @validator("name")
    def validate_name(cls, value):
        """Ensure name does not contain weird characters"""
        return normalize_name(value)


class ExampleSettings(BaseSettingsModel):
    """Test addon settings"""

    folder_type: str = Field(
        "Asset",
        title="Folder type",
        description="""Type of the folder the addon operates on. 
        It can be any type of folder. Refer to the project anatomy for complete list.
        """
    )
    textarea: str = Field(
        "",
        title="Textarea",
        widget="textarea",
    )

    number: int = Field(
        1,
        title="Number",
        description="Positive integer 1-10",
        gt=0,  # greater than
        le=10,  # less or equal
    )

    # Simple enumerators can be defined using Literal type

    simple_enum: Literal["red", "green", "blue"] = Field(
        "red",
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
        enum_resolver=lambda: ["foo", "bar", "ba"],
    )

    # Enumerators can be defined using a list of dicts, where
    # each dict has "value" and "label" keys

    enum_with_labels: str = Field(
        "value1",
        title="Enum with labels",
        enum_resolver=enum_resolver,
    )

    list_of_strings: list[str] = Field(
        default_factory=list,
        title="List of strings",
    )

    # Settings models can be nested

    nested_settings: NestedSettings = Field(
        default_factory=NestedSettings,
        title="Nested settings",
    )

    grouped_settings: GroupedSettings = Field(
        default_factory=GroupedSettings,
        title="Grouped settings",
        description="Nested settings submodel with grouping",
    )

    list_of_submodels: list[CompactListSubmodel] = Field(
        default_factory=list,
        title="A list of compact objects",
    )

    dict_like_list: list[DictLikeSubmodel] = Field(
        default_factory=list,
        title="Dict-like list",
    )

    @validator("list_of_submodels", "dict_like_list")
    def ensure_unique_names(cls, value):
        """Ensure name fields within the lists have unique names."""
        ensure_unique_names(value)
        return value
