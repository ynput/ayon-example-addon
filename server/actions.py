from ayon_server.actions import SimpleActionManifest


EXAMPLE_SIMPLE_ACTIONS = [
    SimpleActionManifest(
        identifier="example-folder-action",
        label="Example Folder Action",
        position=[],
        order=100,
        icon="maya",

        entity_type="folder",
        entity_subtypes=None,
        allow_multiselection=False,
    ),
    SimpleActionManifest(
        identifier="example-task-action",
        label="Example Task Action",
        position=[],
        order=100,
        icon="nuke",

        entity_type="task",
        entity_subtypes=None,
        allow_multiselection=True,
    )
]
