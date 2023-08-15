/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeListIngredientItemGroupOut } from './RecipeListIngredientItemGroupOut';

export type RecipeListOut = {
    id: number;
    title: string;
    defaultNumPortions: number;
    ingredientItemGroups: Array<RecipeListIngredientItemGroupOut>;
};

