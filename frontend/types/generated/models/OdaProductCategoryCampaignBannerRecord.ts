/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductCategoryCampaignBannerPromotionBubbleRecord } from './OdaProductCategoryCampaignBannerPromotionBubbleRecord';

export type OdaProductCategoryCampaignBannerRecord = {
    id: number;
    imageUrl?: (string | null);
    leadText?: (string | null);
    regularText?: (string | null);
    title?: (string | null);
    description?: (string | null);
    buttonText?: (string | null);
    link?: (string | null);
    hasDarkOverlay: boolean;
    promotionBubble?: (OdaProductCategoryCampaignBannerPromotionBubbleRecord | null);
};

