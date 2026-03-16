import asyncio
import os
import sys
import traceback
from datetime import date, timedelta
from typing import Any, List, Dict, Optional, Union

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from mealie_client import MealieClient
from mealie_client.models.recipe import RecipeCreateRequest, RecipeUpdateRequest
from mealie_client.models.meal_plan import MealPlanCreateRequest, MealPlanUpdateRequest
from mealie_client.models.shopping_list import (
    ShoppingListCreateRequest,
    ShoppingListUpdateRequest,
)
from mealie_client.models.food import FoodCreateRequest, FoodUpdateRequest
from mealie_client.models.unit import UnitCreateRequest, UnitUpdateRequest


class SDKTester:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.api_token = api_token
        self.results = []

    def log(self, manager: str, operation: str, status: str, details: str = ""):
        self.results.append(
            {
                "manager": manager,
                "operation": operation,
                "status": status,
                "details": details,
            }
        )
        print(f"[{manager}] {operation}: {status} {details}")

    async def run_tests(self):
        async with MealieClient(
            base_url=self.base_url, api_token=self.api_token
        ) as client:
            # 1. App Info / Health
            try:
                info = await client.get_app_info()
                self.log(
                    "App",
                    "get_app_info",
                    "✅ SUCCESS",
                    f"Version: {info.get('version')}",
                )
            except Exception as e:
                self.log("App", "get_app_info", "❌ FAILED", str(e))

            # Testing sequence: Create -> Update -> Delete
            await self.test_recipes_crud(client)
            await self.test_shopping_lists_crud(client)
            await self.test_foods_crud(client)
            await self.test_units_crud(client)

            # Read-only or safe tests
            await self.test_users(client)
            await self.test_meal_plans(client)
            await self.test_households(client)
            await self.test_labels(client)
            await self.test_groups(client)

        self.write_report()

    async def test_recipes_crud(self, client):
        manager = "Recipes"
        recipe_id = None
        try:
            # Create
            new_recipe = await client.recipes.create(
                RecipeCreateRequest(
                    name="SDK CRUD Test Recipe", description="Initial description"
                )
            )
            recipe_id = new_recipe.id
            self.log(manager, "create", "✅ SUCCESS", f"ID: {recipe_id}")

            # Update
            updated = await client.recipes.update(
                recipe_id, RecipeUpdateRequest(description="Updated description")
            )
            self.log(
                manager,
                "update",
                "✅ SUCCESS",
                f"New description: {updated.description}",
            )

            # Get
            recipe = await client.recipes.get(recipe_id)
            self.log(manager, "get", "✅ SUCCESS", f"Name: {recipe.name}")

        except Exception as e:
            self.log(manager, "CRUD Operations", "❌ FAILED", str(e))
        finally:
            if recipe_id:
                try:
                    await client.recipes.delete(recipe_id)
                    self.log(manager, "delete (Cleanup)", "✅ SUCCESS")
                except Exception as cleanup_err:
                    self.log(manager, "delete (Cleanup)", "❌ FAILED", str(cleanup_err))

    async def test_shopping_lists_crud(self, client):
        manager = "ShoppingLists"
        list_id = None
        try:
            # Create
            new_list = await client.shopping_lists.create(
                ShoppingListCreateRequest(name="SDK CRUD Test List")
            )
            list_id = new_list.id
            self.log(manager, "create", "✅ SUCCESS", f"ID: {list_id}")

            # Update
            updated = await client.shopping_lists.update(
                list_id, ShoppingListUpdateRequest(name="SDK CRUD Updated List")
            )
            self.log(manager, "update", "✅ SUCCESS", f"New name: {updated.name}")

        except Exception as e:
            self.log(manager, "CRUD Operations", "❌ FAILED", str(e))
        finally:
            if list_id:
                try:
                    await client.shopping_lists.delete(list_id)
                    self.log(manager, "delete (Cleanup)", "✅ SUCCESS")
                except Exception as cleanup_err:
                    self.log(manager, "delete (Cleanup)", "❌ FAILED", str(cleanup_err))

    async def test_foods_crud(self, client):
        manager = "Foods"
        food_id = None
        try:
            # Create
            new_food = await client.foods.create(
                FoodCreateRequest(name="SDK CRUD Test Food")
            )
            food_id = new_food.id
            self.log(manager, "create", "✅ SUCCESS", f"ID: {food_id}")

            # Update
            updated = await client.foods.update(
                food_id, FoodUpdateRequest(description="SDK Update")
            )
            self.log(manager, "update", "✅ SUCCESS")

        except Exception as e:
            self.log(manager, "CRUD Operations", "❌ FAILED", str(e))
        finally:
            if food_id:
                try:
                    await client.foods.delete(food_id)
                    self.log(manager, "delete (Cleanup)", "✅ SUCCESS")
                except Exception as cleanup_err:
                    self.log(manager, "delete (Cleanup)", "❌ FAILED", str(cleanup_err))

    async def test_units_crud(self, client):
        manager = "Units"
        unit_id = None
        try:
            # Create
            new_unit = await client.units.create(
                UnitCreateRequest(name="SDK CRUD Test Unit", abbreviation="sct")
            )
            unit_id = new_unit.id
            self.log(manager, "create", "✅ SUCCESS", f"ID: {unit_id}")

            # Update
            await client.units.update(
                unit_id, UnitUpdateRequest(name="SDK CRUD Updated Unit")
            )
            self.log(manager, "update", "✅ SUCCESS")

        except Exception as e:
            self.log(manager, "CRUD Operations", "❌ FAILED", str(e))
        finally:
            if unit_id:
                try:
                    await client.units.delete(unit_id)
                    self.log(manager, "delete (Cleanup)", "✅ SUCCESS")
                except Exception as cleanup_err:
                    self.log(manager, "delete (Cleanup)", "❌ FAILED", str(cleanup_err))

    async def test_users(self, client):
        manager = "Users"
        try:
            me = await client.users.get_self()
            self.log(manager, "get_self", "✅ SUCCESS", f"User: {me.username}")

            # We don't perform CRUD on users to avoid lockouts
            users = await client.users.get_all(per_page=5)
            self.log(
                manager, "get_all (Admin)", "✅ SUCCESS", f"Found {len(users)} users"
            )
        except Exception as e:
            self.log(manager, "Operations", "❌ FAILED", str(e))

    async def test_meal_plans(self, client):
        manager = "MealPlans"
        try:
            # We only read to avoid messing with planned meals
            today = date.today()
            plans = await client.meal_plans.get_all(
                start_date=today, end_date=today + timedelta(days=1)
            )
            self.log(manager, "get_all", "✅ SUCCESS", f"Found {len(plans)} plans")

            today_plan = await client.meal_plans.get_today()
            self.log(
                manager,
                "get_today",
                "✅ SUCCESS",
                f"Found: {'Yes' if today_plan else 'No'}",
            )
        except Exception as e:
            self.log(manager, "Operations", "❌ FAILED", str(e))

    async def test_households(self, client):
        manager = "Households"
        try:
            me = await client.households.get_self()
            self.log(manager, "get_self", "✅ SUCCESS", f"Name: {me.name}")
        except Exception as e:
            self.log(manager, "Operations", "❌ FAILED", str(e))

    async def test_labels(self, client):
        manager = "Labels"
        try:
            labels = await client.labels.get_all(per_page=5)
            self.log(manager, "get_all", "✅ SUCCESS", f"Found {len(labels)} labels")
        except Exception as e:
            self.log(manager, "Operations", "❌ FAILED", str(e))

    async def test_groups(self, client):
        manager = "Groups"
        try:
            me = await client.groups.get_self()
            self.log(manager, "get_self", "✅ SUCCESS", f"Name: {me.name}")
        except Exception as e:
            self.log(manager, "Operations", "❌ FAILED", str(e))

    def write_report(self):
        with open("sdk_test_results.md", "w") as f:
            f.write("# SDK Integration Test Results\n\n")
            f.write("| Manager | Operation | Status | Details |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for r in self.results:
                f.write(
                    f"| {r['manager']} | {r['operation']} | {r['status']} | {r['details']} |\n"
                )
        print("\nReport written to sdk_test_results.md")


if __name__ == "__main__":
    url = os.environ.get("MEALIE_BASE_URL")
    token = os.environ.get("MEALIE_API_TOKEN")

    if not url or not token:
        print("Please set MEALIE_BASE_URL and MEALIE_API_TOKEN environment variables")
        sys.exit(1)

    tester = SDKTester(url, token)
    asyncio.run(tester.run_tests())
