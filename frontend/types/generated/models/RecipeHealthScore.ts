/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeHealthScoreImpactRecord } from './RecipeHealthScoreImpactRecord';

export type RecipeHealthScore = {
    rating: number;
    positiveImpact: Array<RecipeHealthScoreImpactRecord>;
    negativeImpact: Array<RecipeHealthScoreImpactRecord>;
};

