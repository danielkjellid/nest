/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientRecord } from './RecipeIngredientRecord';
import type { UnitRecord } from './UnitRecord';

export type RecipeIngredientItemRecord = {
    id: number;
    groupTitle: string;
    ingredient: RecipeIngredientRecord;
    additionalInfo?: string;
    portionQuantity: number;
    portionQuantityUnit: UnitRecord;
    portionQuantityDisplay: string;
};

