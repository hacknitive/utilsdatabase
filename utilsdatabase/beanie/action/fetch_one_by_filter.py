from typing import (
    Type,
    Dict,
    Optional,
    Union,
    List,
    Tuple,
)

from beanie import (
    Document,
    SortDirection,
)
from pydantic import BaseModel


async def fetch_one_by_filter(
        document: Type[Document],
        filter_: Dict,
        project_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        skip: Optional[int] = None,
        sort: Union[None, str, List[Tuple[str, SortDirection]]] = None,
) -> Document | None:
    return await document.find_many(
        filter_,
        projection_model=project_model,
        fetch_links=fetch_links,
        skip=skip,
        limit=1,
        sort=sort,
    ).first_or_none()
