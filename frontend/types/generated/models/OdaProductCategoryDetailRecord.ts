/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductCategoryCampaignBannerRecord } from './OdaProductCategoryCampaignBannerRecord';
import type { OdaProductCategoryRecord } from './OdaProductCategoryRecord';

export type OdaProductCategoryDetailRecord = {
    id: number;
    name: string;
    parent?: number;
    ordering: number;
    description: string;
    isNew: boolean;
    children: Array<OdaProductCategoryDetailRecord>;
    parents: Array<OdaProductCategoryRecord>;
    siblings: Array<OdaProductCategoryRecord>;
    campaignBanners: Array<OdaProductCategoryCampaignBannerRecord>;
};

