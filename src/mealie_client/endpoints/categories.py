"""
Categories endpoint manager for the Mealie SDK.
"""

from typing import Any, Dict, List, Optional, Union, cast
from ..models.common import OrderByNullPosition, OrderDirection
from ..models.category import (
    Category,
    CategoryCreateRequest,
    CategoryFilter,
    CategorySummary,
    CategoryUpdateRequest,
)
from ..exceptions import NotFoundError
from ..utils import clean_dict


class CategoriesManager:
    """Manages category-related API operations."""

    def __init__(self, client: Any) -> None:
        self.client = client

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 50,
        order_by: Optional[str] = None,
        order_direction: OrderDirection = OrderDirection.ASC,
        order_by_null_position: OrderByNullPosition = OrderByNullPosition.LAST,
        search: Optional[str] = None,
        accept_language: Optional[str] = None,
    ) -> List[CategorySummary]:
        """
        Get all categories.

        Returns:
            List of category summaries
        """
        response = await self.client.get(
            "organizers/categories",
            params=CategoryFilter(
                page=page,
                per_page=per_page,
                order_by=order_by,
                order_direction=order_direction,
                order_by_null_position=order_by_null_position,
                search=search,
                accept_language=accept_language,
            ).to_params(),
        )

        if isinstance(response, list):
            categories_data = response
        elif isinstance(response, dict) and "items" in response:
            categories_data = response["items"]
        else:
            categories_data = []

        return [
            CategorySummary.from_dict(cat_data)
            if isinstance(cat_data, dict)
            else cat_data
            for cat_data in categories_data
        ]

    async def get(self, category_id: str) -> Category:
        """
        Get a specific category by ID.

        Args:
            category_id: Category ID identifier

        Returns:
            Complete category object
        """
        try:
            response = await self.client.get(f"organizers/categories/{category_id}")

            if isinstance(response, bytes):
                response_text = response.decode("utf-8", errors="ignore").lower()
                if "<!doctype html>" in response_text or "<html" in response_text:
                    raise NotFoundError(
                        f"Category '{category_id}' not found",
                        resource_type="category",
                        resource_id=category_id,
                    )

            if not isinstance(response, dict):
                raise ValueError("Response must be a dictionary")

            return Category.from_dict(response)
        except Exception as e:
            if hasattr(e, "status_code") and getattr(e, "status_code") == 404:
                raise NotFoundError(
                    f"Category '{category_id}' not found",
                    resource_type="category",
                    resource_id=category_id,
                )
            raise

    async def get_by_slug(self, slug: str) -> Category:
        """
        Get a specific category by slug.

        Args:
            slug: Category slug

        Returns:
            Complete category object
        """
        response = await self.client.get(f"organizers/categories/slug/{slug}")
        return Category.from_dict(response) if isinstance(response, dict) else response

    async def create(
        self, category: Union[CategoryCreateRequest, Dict[str, Any]]
    ) -> Category:
        """
        Create a new category.

        Args:
            category: Category object or dict to create

        Returns:
            Created category object
        """
        if hasattr(category, "to_dict"):
            category_data = category.to_dict()
        else:
            category_data = cast(Dict[str, Any], category)

        response = await self.client.post(
            "organizers/categories", json_data=clean_dict(category_data)
        )
        return Category.from_dict(response) if isinstance(response, dict) else response

    async def update(
        self, category_id: str, category: Union[CategoryUpdateRequest, Dict[str, Any]]
    ) -> Category:
        """
        Update an existing category.

        Args:
            category_id: Category ID identifier
            category: Category object or dict to update

        Returns:
            Updated category object
        """
        if hasattr(category, "to_dict"):
            category_data = category.to_dict()
        else:
            category_data = cast(Dict[str, Any], category)

        response = await self.client.put(
            f"organizers/categories/{category_id}", json_data=clean_dict(category_data)
        )
        return Category.from_dict(response) if isinstance(response, dict) else response

    async def delete(self, category_id: str) -> bool:
        """
        Delete an existing category.

        Args:
            category_id: Category ID identifier

        Returns:
            True if deletion was successful
        """
        await self.client.delete(f"organizers/categories/{category_id}")
        return True

    async def get_empty(self) -> List[CategorySummary]:
        """
        Get all empty categories.

        Returns:
            List of category summaries
        """
        response = await self.client.get("organizers/categories/empty")
        if isinstance(response, list):
            return [CategorySummary.from_dict(d) for d in response]
        return []
