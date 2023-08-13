/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemListOut } from './RecipeIngredientItemListOut';

export type RecipeIngredientItemGroupListOut = {
    id: number;
    title: string;
    ingredientItems: Array<RecipeIngredientItemListOut>;
};

