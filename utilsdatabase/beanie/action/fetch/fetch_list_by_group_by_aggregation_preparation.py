from beanie import Document
from ...enum import EnumOrderBy
from ..utility import (
    prepare_filter_for_group_by_aggregation,
    create_group_by_pipeline,
)
from .fetch_list_by_aggregation import fetch_list_by_aggregation



async def fetch_list_by_group_by_aggregation_preparation(
        document: type[Document],
        aggregation: list[dict],
        inputs: dict,
        group_by_on: list[str],
        search_field_name: str = 'search',
        fields_names_for_regex: tuple[str, ...] = tuple(),
        fields_names_for_range: tuple[str, ...] = tuple(),
        fields_names_for_in: tuple[str, ...] = tuple(),
        fields_names_for_search: tuple[str, ...] = tuple(),
        order_by: dict[str, EnumOrderBy] | None = None,
) -> dict:
    first_filter, middle_filter, last_filter = prepare_filter_for_group_by_aggregation(
        inputs=inputs,
        search_field_name=search_field_name,
        fields_names_for_regex=fields_names_for_regex,
        fields_names_for_range=fields_names_for_range,
        fields_names_for_in=fields_names_for_in,
        fields_names_for_search=fields_names_for_search,
    )

    return await fetch_list_by_aggregation(
        document=document,
        aggregation=[
            *aggregation,
            {'$match': middle_filter},
            *create_group_by_pipeline(group_by_on=group_by_on),
        ],
        first_filter=first_filter,
        last_filter=last_filter,
        order_by=order_by,
        current_page=current_page,
        page_size=page_size,
    )
