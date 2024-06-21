from typing import Type

from beanie import Document


async def insert_one(
        document: Type[Document],
        inputs: dict,
) -> Type[Document] | Document:
    obj = document(**inputs)
    await obj.insert()
    return obj
