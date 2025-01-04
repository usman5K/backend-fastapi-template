import re

from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # format TitleCase names into lower_snake_case
        name = cls.__name__

        snake_case_name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        return snake_case_name
