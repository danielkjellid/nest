/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailDurationOut } from './RecipeDetailDurationOut';
import type { RecipeDetailIngredientGroupOut } from './RecipeDetailIngredientGroupOut';
import type { RecipeDetailStepOut } from './RecipeDetailStepOut';

export type RecipeDetailOut = {
    id: number;
    title: string;
    slug: string;
    defaultNumPortions: number;
    searchKeywords?: string;
    externalId?: string;
    externalUrl?: string;
    statusDisplay: string;
    difficultyDisplay: string;
    isVegetarian: boolean;
    isPescatarian: boolean;
    duration: RecipeDetailDurationOut;
    steps: Array<RecipeDetailStepOut>;
    ingredientGroups: Array<RecipeDetailIngredientGroupOut>;
};

