/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IngredientItem } from './IngredientItem';
import type { RecipeStepType } from './RecipeStepType';

export type Step = {
    id?: number;
    number: number;
    duration: number;
    instruction: string;
    stepType: RecipeStepType;
    ingredientItems: Array<IngredientItem>;
};

