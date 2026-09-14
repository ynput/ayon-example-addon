from ayon_server.actions import ActionExecutor, ExecuteResponseModel
from ayon_server.forms import QueryCondition, QueryFilter, SimpleForm
from ayon_server.helpers.get_entity_class import get_entity_class
from ayon_server.lib.postgres import Postgres


async def handle_attribute_action(executor: ActionExecutor) -> ExecuteResponseModel:
    """
    Set an attribute value on a folder, picking both the attribute and its
    new value through two chained form fields.

    This demonstrates the SimpleForm conditionals/templating additions:

    - `enumResolver` / `enumResolverParams`: the "value" field's options are
      fetched live from /api/enum (the "attrib" resolver) instead of being
      baked into the form.
    - `{{fieldName}}` templating: "value"'s enumResolverParams reference the
      "attribute" field's own submitted value, so the resolver call is
      re-parametrized as the user changes their pick.
    - `rules`: "value" is read-only and cleared while "attribute" is unset -
      without this, the frontend would call the "attrib" resolver with a
      missing `name` param, which it rejects outright.
    """
    context = executor.context
    form_data = context.form_data or {}


    attrib_options = []
    for row in await Postgres.fetch(
        """
        SELECT name, data
        FROM attributes
        WHERE data->'enum' IS NOT NULL
        """
    ):
        attrib_options.append(
            {
                "value": row["name"],
                "label": row["data"].get("label", row["name"]),
            }
        )

    if "attribute" not in form_data:
        form = SimpleForm()

        form.select(
            "attribute",
            options=attrib_options,
            label="Attribute",
        )

        form.select(
            "value",
            label="Value",
            enumResolver="attrib",
            enumResolverParams={
                "project_name": context.project_name,
                "name": "{{attribute}}",
            },
            rules=[
                {
                    "when": QueryFilter(
                        conditions=[
                            QueryCondition(key="attribute", operator="isnull"),
                        ]
                    ),
                    "set": {"readOnly": True, "value": None},
                }
            ],
        )

        return await executor.get_form_response(
            title="Set attribute value",
            fields=form,
            submit_label="Set value",
        )

    #
    # Form submitted - apply the change
    #

    attribute = form_data.get("attribute")
    value = form_data.get("value")
    assert attribute, "Missing 'attribute' in submitted form data"

    entity_type = context.entity_type
    entity_id = context.entity_ids[0]
    entity_class = get_entity_class(entity_type)
    entity = await entity_class.load(context.project_name, entity_id)

    await entity.ensure_update_access(executor.user)
    setattr(entity.attrib, attribute, value)
    await entity.save()

    return await executor.get_simple_response(
        message=f"Set {attribute} to {value!r} on {entity.name}",
    )
