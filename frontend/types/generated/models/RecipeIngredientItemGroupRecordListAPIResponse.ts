/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemGroupRecord } from './RecipeIngredientItemGroupRecord';

export type RecipeIngredientItemGroupRecordListAPIResponse = {
    status: RecipeIngredientItemGroupRecordListAPIResponse.status;
    message?: string;
    data?: Array<RecipeIngredientItemGroupRecord>;
};

export namespace RecipeIngredientItemGroupRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

