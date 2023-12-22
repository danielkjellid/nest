/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientRecord } from './RecipeIngredientRecord';

export type APIResponse_list_RecipeIngredientRecord__ = {
    status: APIResponse_list_RecipeIngredientRecord__.status;
    message?: (string | null);
    data: (Array<RecipeIngredientRecord> | null);
};

export namespace APIResponse_list_RecipeIngredientRecord__ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

