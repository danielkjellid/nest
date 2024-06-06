/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IngredientGroupItem } from './IngredientGroupItem';
import type { RecipeCreateForm } from './RecipeCreateForm';
import type { Step } from './Step';

export type RecipeEditIn = {
    baseRecipe: RecipeCreateForm;
    ingredientItemGroups?: Array<IngredientGroupItem>;
    steps?: Array<Step>;
};

