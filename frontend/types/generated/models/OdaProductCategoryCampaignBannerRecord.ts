/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductCategoryCampaignBannerPromotionBubbleRecord } from './OdaProductCategoryCampaignBannerPromotionBubbleRecord';

export type OdaProductCategoryCampaignBannerRecord = {
    id: number;
    imageUrl?: string;
    leadText?: string;
    regularText?: string;
    title?: string;
    description?: string;
    buttonText?: string;
    link?: string;
    hasDarkOverlay: boolean;
    promotionBubble?: OdaProductCategoryCampaignBannerPromotionBubbleRecord;
};

