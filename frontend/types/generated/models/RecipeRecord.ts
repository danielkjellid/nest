/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDifficulty } from './RecipeDifficulty';
import type { RecipeStatus } from './RecipeStatus';

export type RecipeRecord = {
    id: number;
    title: string;
    slug: string;
    defaultNumPortions: number;
    searchKeywords?: (string | null);
    externalId?: (string | null);
    externalUrl?: (string | null);
    status: RecipeStatus;
    statusDisplay: string;
    difficulty: RecipeDifficulty;
    difficultyDisplay: string;
    isVegetarian: boolean;
    isPescatarian: boolean;
};

