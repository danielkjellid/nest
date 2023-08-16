/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeListIngredientItemGroupOut } from './RecipeListIngredientItemGroupOut';
import type { RecipeListStepsOut } from './RecipeListStepsOut';

export type RecipeListOut = {
    id: number;
    title: string;
    defaultNumPortions: number;
    steps: Array<RecipeListStepsOut>;
    ingredientItemGroups: Array<RecipeListIngredientItemGroupOut>;
};

