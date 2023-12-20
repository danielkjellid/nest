/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemGroupRecord } from './RecipeIngredientItemGroupRecord';

export type RecipeIngredientItemGroupRecordAPIResponse = {
    status: RecipeIngredientItemGroupRecordAPIResponse.status;
    message?: string;
    data?: Array<RecipeIngredientItemGroupRecord>;
};

export namespace RecipeIngredientItemGroupRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

