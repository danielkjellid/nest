/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailIngredientItemOut } from './RecipeDetailIngredientItemOut';

export type RecipeDetailIngredientGroupOut = {
    id: number;
    title: string;
    ingredientItems: Array<RecipeDetailIngredientItemOut>;
};

