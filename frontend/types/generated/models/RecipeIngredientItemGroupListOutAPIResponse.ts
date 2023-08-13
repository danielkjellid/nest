/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemGroupListOut } from './RecipeIngredientItemGroupListOut';

export type RecipeIngredientItemGroupListOutAPIResponse = {
    status: RecipeIngredientItemGroupListOutAPIResponse.status;
    message?: string;
    data?: Array<RecipeIngredientItemGroupListOut>;
};

export namespace RecipeIngredientItemGroupListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

