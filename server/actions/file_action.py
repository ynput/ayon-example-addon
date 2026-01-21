from ayon_server.forms import SimpleForm
from ayon_server.actions import (
    ActionExecutor,
    ExecuteResponseModel,
)


async def handle_file_action(executor: ActionExecutor) -> ExecuteResponseModel:
    form_data = executor.context.form_data or {}

    #
    # File has been already cached, retrieve it from cache
    #

    if "file_id" in form_data:
        file_id = form_data["file_id"]
        cached_file = await executor.context.get_cached_file(file_id)
        file_size = len(cached_file.get_bytes())

        return await executor.get_simple_response(
            message=f"File with ID {file_id} retrieved from cache. Size: {file_size} bytes"
        )

    #
    # File was not uploaded yet, show the form
    #

    if "example_file" not in form_data:
        form = SimpleForm()
        form.file(name="example_file", label="Example File")
        return await executor.get_form_response("Upload File", form)

    #
    # Intermediate step (show upload file info and cache the file)
    # Just for lolz
    #

    form_file = await executor.context.get_form_file("example_file", cache=True)

    # Show the form with file info

    form = SimpleForm()
    form.label("File uploaded successfully!", highlight="info")
    form.label(f"Cached file ID: {form_file.cache_key}")
    form.label(f"File size: {len(form_file.get_bytes())} bytes")

    # add file id to the form response to identify the cached file later
    # (and to avaid re-uploading)

    form.hidden(name="file_id", value=form_file.cache_key)

    return await executor.get_form_response(
        "File Uploaded",
        form,
        submit_label="Use File",
    )

