/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientsCreateIngredientIn } from './RecipeIngredientsCreateIngredientIn';

export type RecipeIngredientsCreateIn = {
    title: string;
    ordering: number;
    ingredients: Array<RecipeIngredientsCreateIngredientIn>;
};

