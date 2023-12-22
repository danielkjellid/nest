/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UnitRecord } from './UnitRecord';

export type APIResponse_list_UnitRecord__ = {
    status: APIResponse_list_UnitRecord__.status;
    message?: (string | null);
    data: (Array<UnitRecord> | null);
};

export namespace APIResponse_list_UnitRecord__ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

