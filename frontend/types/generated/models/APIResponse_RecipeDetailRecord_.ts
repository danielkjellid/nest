/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailRecord } from './RecipeDetailRecord';

export type APIResponse_RecipeDetailRecord_ = {
    status: APIResponse_RecipeDetailRecord_.status;
    message?: (string | null);
    data: (RecipeDetailRecord | null);
};

export namespace APIResponse_RecipeDetailRecord_ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

