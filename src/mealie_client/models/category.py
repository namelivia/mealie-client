"""
Category models for the Mealie SDK.

This module contains data models for categories and category management.
"""

from typing import Any, Dict, List, Optional
from .common import BaseModel, OrderByNullPosition, OrderDirection, QueryFilter


class Category(BaseModel):
    """
    Category model representing a recipe category.
    """

    def __init__(
        self,
        id: Optional[str] = None,
        group_id: Optional[str] = None,
        name: str = "",
        slug: str = "",
        **kwargs: Any,
    ) -> None:
        self.id = id
        self.group_id = group_id
        self.name = name
        self.slug = slug
        super().__init__(**kwargs)


class CategorySummary(BaseModel):
    """
    Simplified category model for lists and summaries.
    """

    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        slug: str = "",
        **kwargs: Any,
    ) -> None:
        self.id = id
        self.name = name
        self.slug = slug
        super().__init__(**kwargs)


class CategoryCreateRequest(BaseModel):
    """
    Request model for creating a new category.
    """

    def __init__(
        self,
        name: str,
        **kwargs: Any,
    ) -> None:
        self.name = name
        super().__init__(**kwargs)


class CategoryUpdateRequest(BaseModel):
    """
    Request model for updating an existing category.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.name = name
        super().__init__(**kwargs)


class CategoryFilter(QueryFilter):
    """
    Filter options for category queries.
    """

    def __init__(
        self,
        page: int = 1,
        per_page: int = 50,
        order_by: Optional[str] = None,
        order_direction: OrderDirection = OrderDirection.ASC,
        order_by_null_position: OrderByNullPosition = OrderByNullPosition.LAST,
        search: Optional[str] = None,
        accept_language: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
            order_by_null_position=order_by_null_position,
            search=search,
            accept_language=accept_language,
            **kwargs,
        )
