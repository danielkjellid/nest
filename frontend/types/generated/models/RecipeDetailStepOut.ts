/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailIngredientItemOut } from './RecipeDetailIngredientItemOut';

export type RecipeDetailStepOut = {
    id: number;
    number: number;
    instruction: string;
    stepTypeDisplay: string;
    ingredientItems: Array<RecipeDetailIngredientItemOut>;
};

