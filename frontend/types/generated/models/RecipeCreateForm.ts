/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDifficulty } from './RecipeDifficulty';
import type { RecipeStatus } from './RecipeStatus';

export type RecipeCreateForm = {
    title: string;
    searchKeywords?: (string | null);
    defaultNumPortions: number;
    status: (RecipeStatus | string);
    difficulty: (RecipeDifficulty | string);
    externalId?: (string | null);
    externalUrl?: (string | null);
    isVegetarian?: boolean;
    isPescatarian?: boolean;
};

