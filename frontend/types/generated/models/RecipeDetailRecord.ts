/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDifficulty } from './RecipeDifficulty';
import type { RecipeDurationRecord } from './RecipeDurationRecord';
import type { RecipeGlycemicData } from './RecipeGlycemicData';
import type { RecipeHealthScore } from './RecipeHealthScore';
import type { RecipeIngredientItemGroupRecord } from './RecipeIngredientItemGroupRecord';
import type { RecipeStatus } from './RecipeStatus';
import type { RecipeStepRecord } from './RecipeStepRecord';

export type RecipeDetailRecord = {
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
    duration: RecipeDurationRecord;
    glycemicData?: (RecipeGlycemicData | null);
    healthScore?: (RecipeHealthScore | null);
    ingredientGroups: Array<RecipeIngredientItemGroupRecord>;
    steps: Array<RecipeStepRecord>;
};

