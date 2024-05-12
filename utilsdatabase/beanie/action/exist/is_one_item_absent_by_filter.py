from typing import Type

from beanie import Document
from utilscommon.utilscommon.exception.project_base_exception import ProjectBaseException


async def is_one_item_absent_by_filter(
        document: Type[Document],
        filter_: dict,
        fetch_links: bool = False,
        raise_on_existence: bool = False,
        exception_input: dict = dict(),  # noqa
) -> bool:
    result = await document.find_one(
        filter_,
        fetch_links=fetch_links,
    ).exists()

    if result:
        if raise_on_existence:
            raise ProjectBaseException(**exception_input)

        return False

    else:
        return True