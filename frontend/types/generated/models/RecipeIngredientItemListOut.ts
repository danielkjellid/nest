/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemPortionUnitListOut } from './RecipeIngredientItemPortionUnitListOut';
import type { RecipeIngredientListOut } from './RecipeIngredientListOut';

export type RecipeIngredientItemListOut = {
    id: number;
    ingredient: RecipeIngredientListOut;
    portionQuantityDisplay: string;
    portionQuantityUnit: RecipeIngredientItemPortionUnitListOut;
};

