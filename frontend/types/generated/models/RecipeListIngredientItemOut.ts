/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeListIngredientItemPortionUnitOut } from './RecipeListIngredientItemPortionUnitOut';
import type { RecipeListIngredientOut } from './RecipeListIngredientOut';

export type RecipeListIngredientItemOut = {
    id: number;
    ingredient: RecipeListIngredientOut;
    portionQuantityDisplay: string;
    portionQuantityUnit: RecipeListIngredientItemPortionUnitOut;
};

