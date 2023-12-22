/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductLocalInfoBadgeRecord } from './OdaProductLocalInfoBadgeRecord';
import type { OdaProductLocalInfoKeywordEmphasisRecord } from './OdaProductLocalInfoKeywordEmphasisRecord';

export type OdaProductLocalInfoTableRow = {
    key: string;
    value: string;
    badge?: (OdaProductLocalInfoBadgeRecord | null);
    indent?: (number | null);
    tooltip?: (string | null);
    link?: (string | null);
    emphasis?: (OdaProductLocalInfoKeywordEmphasisRecord | null);
    keyId?: (string | null);
};

