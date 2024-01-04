/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeCreateForm } from './RecipeCreateForm';
import type { RecipeCreateIngredientItemGroup } from './RecipeCreateIngredientItemGroup';
import type { RecipeCreateSteps } from './RecipeCreateSteps';

export type RecipeCreateIn = {
    baseRecipe: RecipeCreateForm;
    ingredientItemGroups: Array<RecipeCreateIngredientItemGroup>;
    steps: Array<RecipeCreateSteps>;
};

