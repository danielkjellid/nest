/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeRecord } from './RecipeRecord';

export type APIResponse_list_RecipeRecord__ = {
    status: APIResponse_list_RecipeRecord__.status;
    message?: (string | null);
    data: (Array<RecipeRecord> | null);
};

export namespace APIResponse_list_RecipeRecord__ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

