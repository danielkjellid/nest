/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeListIngredientItemOut } from './RecipeListIngredientItemOut';

export type RecipeListStepsOut = {
    id: number;
    number: number;
    duration: number;
    instruction: string;
    stepType: number;
    ingredientItems: Array<RecipeListIngredientItemOut>;
};

