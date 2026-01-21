__all__ = [
    "EXAMPLE_SIMPLE_ACTIONS",
    "handle_file_action",
    "handle_list_action",
]

from ayon_server.actions import SimpleActionManifest
from .file_action import handle_file_action
from .list_action import handle_list_action


EXAMPLE_SIMPLE_ACTIONS = [

    SimpleActionManifest(
        identifier="example-file-action",
        label="Example file action",
        category="server",
        order=100,
        icon={"type": "material-symbols", "name": "casino"},
        entity_type="folder",
        allow_multiselection=False,
    ),
    SimpleActionManifest(
        identifier="example-list-action-1",
        label="Example list action",
        category="server",
        order=100,
        icon={"type": "material-symbols", "name": "casino"},
        entity_type="list",
        entity_subtypes=None,
        allow_multiselection=False,
    ),

    SimpleActionManifest(
        identifier="example-list-action-2",
        label="Review action",
        category="server",
        order=100,
        icon={"type": "material-symbols", "name": "casino"},
        entity_type="list",
        entity_subtypes=["version:review-session"],
        allow_multiselection=False,
    ),

    SimpleActionManifest(
        identifier="example-list-action-3",
        label="Version and folder action",
        category="server",
        order=100,
        icon={"type": "material-symbols", "name": "casino"},
        entity_type="list",
        entity_subtypes=["version", "folder"],
        allow_multiselection=False,
    ),

    SimpleActionManifest(
        identifier="example-folder-action-1",
        label="Example folder action 1",
        category="server",
        order=100,
        icon={"type": "material-symbols", "name": "folder"},

        entity_type="folder",
        entity_subtypes=None,
        allow_multiselection=False,
    ),
    SimpleActionManifest(
        identifier="example-folder-action-2",
        label="Example folder action 2",
        category="admin",
        order=100,
        icon={"type": "material-symbols", "name": "delete"},

        entity_type="folder",
        entity_subtypes=None,
        allow_multiselection=False,
    ),
    SimpleActionManifest(
        identifier="example-task-action",
        label="Task Action",
        category="server",
        order=100,
        icon={"type": "material-symbols", "name": "task"},

        entity_type="task",
        entity_subtypes=None,
        allow_multiselection=False,
    ),
    SimpleActionManifest(
        identifier="launch-nuke",
        label="Launch Nuke",
        category="application",
        order=100,
        icon={"type": "url", "url": "{addon_url}/public/icons/nuke.png"},

        entity_type="task",
        entity_subtypes=["Compositing", "Roto", "Matchmove"],
        allow_multiselection=True,
    ),
]
