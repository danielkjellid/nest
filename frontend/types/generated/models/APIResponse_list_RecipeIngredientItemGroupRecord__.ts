/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientItemGroupRecord } from './RecipeIngredientItemGroupRecord';

export type APIResponse_list_RecipeIngredientItemGroupRecord__ = {
    status: APIResponse_list_RecipeIngredientItemGroupRecord__.status;
    message?: (string | null);
    data: (Array<RecipeIngredientItemGroupRecord> | null);
};

export namespace APIResponse_list_RecipeIngredientItemGroupRecord__ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

