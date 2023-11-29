/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeListOut } from './RecipeListOut';

export type RecipeListOutListAPIResponse = {
    status: RecipeListOutListAPIResponse.status;
    message?: string;
    data?: Array<RecipeListOut>;
};

export namespace RecipeListOutListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

