/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDifficulty } from './RecipeDifficulty';
import type { RecipeStatus } from './RecipeStatus';

export type RecipeCreateIn = {
    title: string;
    searchKeywords?: string;
    defaultNumPortions: string;
    externalId?: string;
    externalUrl?: string;
    status: (RecipeStatus | string);
    difficulty: (RecipeDifficulty | string);
    isPartialRecipe?: boolean;
    isVegetarian?: boolean;
    isPescatarian?: boolean;
};
