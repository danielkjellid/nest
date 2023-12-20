/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemRecord } from './RecipeIngredientItemRecord';
import type { RecipeStepType } from './RecipeStepType';

export type RecipeStepRecord = {
    id: number;
    number: number;
    duration: number;
    instruction: string;
    stepType: RecipeStepType;
    stepTypeDisplay: string;
    ingredientItems: Array<RecipeIngredientItemRecord>;
};

