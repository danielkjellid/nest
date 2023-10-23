/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailIngredientItemUnitOut } from './RecipeDetailIngredientItemUnitOut';
import type { RecipeDetailIngredientOut } from './RecipeDetailIngredientOut';

export type RecipeDetailIngredientItemOut = {
    id: number;
    ingredient: RecipeDetailIngredientOut;
    portionQuantity: number;
    portionQuantityDisplay: string;
    portionQuantityUnit: RecipeDetailIngredientItemUnitOut;
};

