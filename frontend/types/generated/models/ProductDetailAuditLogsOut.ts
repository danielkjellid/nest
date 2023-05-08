/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductDetailAuditLogsOut = {
    userOrSource?: string;
    remoteAddr?: string;
    changes: Record<string, Array<any>>;
    createdAt: string;
};

