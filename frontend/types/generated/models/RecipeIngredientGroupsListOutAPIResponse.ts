/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientGroupsListOut } from './RecipeIngredientGroupsListOut';

export type RecipeIngredientGroupsListOutAPIResponse = {
    status: RecipeIngredientGroupsListOutAPIResponse.status;
    message?: string;
    data?: Array<RecipeIngredientGroupsListOut>;
};

export namespace RecipeIngredientGroupsListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

