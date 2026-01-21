import random

from ayon_server.entity_lists import EntityList
from ayon_server.forms import SimpleForm
from ayon_server.helpers.get_entity_class import get_entity_class
from ayon_server.actions import (
    ActionExecutor,
    ExecuteResponseModel,
)

async def handle_list_action(executor: ActionExecutor) -> ExecuteResponseModel:
    """
    Handle the list action.
    This is a simple example of how to handle a list action.
    The list action is executed on the server side and returns a list of items.
    The items are then displayed in the browser.
    """

    # Get the context
    context = executor.context
    list_id = context.entity_ids[0]
    project_name = context.project_name

    l = await EntityList.load(project_name, list_id)

    item = random.choice(l.items)
    item_class = get_entity_class(l.entity_type)
    entity = await item_class.load(project_name, item.entity_id)
    
    info = (
        f"You have a very nice list! {l.payload.label} is the best! \n\n"
        f"I can see you have {len(l.payload.items)} items here. \n\n"
        f"Especially, I like {entity.name} \n\n"
    ) 

    form = (
        SimpleForm()
        .label(info, highlight="info")
    )

    return await executor.get_form_response(
        title="List action",
        fields=form,
        submit_label="Roll a dice again",
        submit_icon="casino",
    )


