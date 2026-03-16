# Mealie SDK Endpoint Status Report

This report identifies the current status of Mealie API endpoints implementation in the SDK compared to the latest `openapi.json` definition.

## Status Summary

| Manager | Status | Implementation Level |
| :--- | :--- | :--- |
| **Recipes** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Users** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Groups** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Meal Plans** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Shopping Lists** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Foods** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Units** | ✅ Up to Date | High |
| **Households** | 🏗️ Needs Completion | Partial (Core CRUD done) |
| **Labels** | ✅ Up to Date | High |

---

## Detailed Analysis

### 1. Recipes (`RecipesManager`)
**Status:** 🏗️ Needs Completion
- **Implemented:**
    - `GET /api/recipes`
    - `GET /api/recipes/{recipe_id_or_slug}`
    - `POST /api/recipes`
    - `PATCH /api/recipes/{recipe_id_or_slug}`
    - `DELETE /api/recipes/{recipe_id_or_slug}`
    - `POST /api/recipes/create/url`
    - `GET /api/recipes/suggestions`
- **Missing Endpoints:**
    - `POST /api/recipes/bulk-actions/categorize`
    - `POST /api/recipes/bulk-actions/delete`
    - `POST /api/recipes/bulk-actions/export`
    - `GET /api/recipes/bulk-actions/export/{export_id}/download`
    - `POST /api/recipes/create/image`
    - `POST /api/recipes/create/zip`
    - `GET /api/recipes/shared/{token_id}`
    - `GET /api/recipes/timeline/events`
    - `POST /api/recipes/{slug}/image` (Upload image)
    - `GET /api/recipes/{slug}/comments`
    - `POST /api/recipes/{slug}/duplicate`

### 2. Users (`UsersManager`)
**Status:** 🏗️ Needs Completion
- **Implemented:**
    - `GET /api/admin/users`
    - `GET /api/admin/users/{user_id}`
    - `POST /api/admin/users`
    - `PUT /api/admin/users/{user_id}`
    - `DELETE /api/admin/users/{user_id}`
    - `GET /api/users/self`
- **Missing Endpoints:**
    - `POST /api/users/register`
    - `POST /api/users/forgot-password`
    - `POST /api/users/reset-password`
    - `GET /api/users/api-tokens`
    - `POST /api/users/api-tokens`
    - `DELETE /api/users/api-tokens/{token_id}`
    - `GET /api/users/self/favorites`
    - `GET /api/users/self/ratings`
    - `POST /api/users/{id}/image`

### 3. Groups (`GroupsManager`)
**Status:** 🏗️ Needs Completion
- **Implemented:**
    - `GET /api/groups/self`
    - `GET /api/groups/preferences`
    - `PUT /api/groups/preferences`
    - `GET /api/admin/groups`
    - `GET /api/admin/groups/{group_id}`
    - `POST /api/admin/groups`
    - `PUT /api/admin/groups/{group_id}`
    - `DELETE /api/admin/groups/{group_id}`
- **Missing Endpoints:**
    - `GET /api/groups/reports`
    - `GET /api/groups/migrations`
    - `POST /api/groups/seeders`
- **Correction Required:** Module docstring incorrectly states groups are read-only.

### 4. Meal Plans (`MealPlansManager`)
**Status:** 🏗️ Needs Completion
- **Implemented:**
    - `GET /api/households/mealplans`
    - `GET /api/households/mealplans/{plan_id}`
    - `GET /api/households/mealplans/today`
    - `POST /api/households/mealplans`
    - `PUT /api/households/mealplans/{plan_id}`
    - `DELETE /api/households/mealplans/{plan_id}`
- **Missing Endpoints:**
    - `GET /api/households/mealplan-rules`
    - `POST /api/households/mealplan-rules`

### 5. Shopping Lists (`ShoppingListsManager`)
**Status:** 🏗️ Needs Completion
- **Implemented:**
    - `GET /api/households/shopping/lists`
    - `GET /api/households/shopping/lists/{list_id}`
    - `POST /api/households/shopping/lists`
    - `PUT /api/households/shopping/lists/{list_id}`
    - `DELETE /api/households/shopping/lists/{list_id}`
    - `POST /api/households/shopping/lists/{list_id}/items`
    - `PUT /api/households/shopping/lists/{list_id}/items/{item_id}`
    - `DELETE /api/households/shopping/lists/{list_id}/items/{item_id}`
- **Missing Endpoints:**
    - `POST /api/households/shopping/lists/{list_id}/clear`
    - `POST /api/households/shopping/lists/{list_id}/copy`

### 6. Households (`HouseholdsManager`)
**Status:** 🏗️ Needs Completion
- **Implemented:**
    - `GET /api/admin/households`
    - `GET /api/admin/households/{household_id}`
    - `POST /api/admin/households`
    - `PUT /api/admin/households/{household_id}`
    - `DELETE /api/admin/households/{household_id}`
    - `GET /api/households/self`
- **Missing Endpoints:**
    - `GET /api/households/invitations`
    - `POST /api/households/webhooks`
- **Correction Required:** Module docstring incorrectly states households are read-only.

### 7. Missing Managers (Not Implemented)
The following entire API sections are currently missing from the SDK:

- **Categories**: `Explore: Categories`, `Organizer: Categories`
- **Tags**: `Explore: Tags`, `Organizer: Tags`
- **Tools**: `Explore: Tools`, `Organizer: Tools`
- **Admin Utilities**: `Admin: Backups`, `Admin: Debug`, `Admin: Email`, `Admin: Maintenance`
- **App Info**: `App: About`, `App: Startup Info`, `App: Theme`
- **Cookbooks**: `Explore: Cookbooks`, `Households: Cookbooks`
- **Webhooks**: `Households: Webhooks`
- **Invitations**: `Households: Invitations`
