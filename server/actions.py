from ayon_server.actions import SimpleActionManifest


EXAMPLE_SIMPLE_ACTIONS = [
    SimpleActionManifest(
        identifier="example-folder-action",
        label="Example Folder Action",
        category="Server",
        order=100,
        icon="{addon_url}/public/icons/maya.png",

        entity_type="folder",
        entity_subtypes=None,
        allow_multiselection=False,
    ),
    SimpleActionManifest(
        identifier="example-task-action",
        label="Example Task Action",
        category="Launcher",
        order=100,
        icon="{addon_url}/public/icons/nuke.png",

        entity_type="task",
        entity_subtypes=None,
        allow_multiselection=True,
    )
]
