import React from 'react'

import { useCommonStyles } from '../../../styles/common'
import { type ProductDetailOut } from '../../../types'

interface ProductDetailHeaderProps
  extends Pick<ProductDetailOut, 'thumbnailUrl' | 'fullName' | 'supplier'> {
  actions?: React.ReactNode
}

function ProductDetailHeader({
  thumbnailUrl,
  fullName,
  supplier,
  actions,
}: ProductDetailHeaderProps) {
  const { classes } = useCommonStyles()

  return (
    <header className="lg:grid-cols-2 grid content-center grid-cols-1 gap-8">
      <div className="lg:order-1 text-ellipsis flex items-center self-center order-2 space-x-6">
        <img
          className={`object-contain w-16 h-16 p-1 border-2 ${classes.border} border-solid rounded-lg bg-white`}
          src={thumbnailUrl}
          alt=""
        />
        <div className="overflow-hidden">
          <div className=" max-w-full text-lg font-semibold leading-6 truncate">{fullName}</div>
          <div className="mt-1 text-sm">{supplier}</div>
        </div>
      </div>
      {actions && (
        <div className="lg:order-2 justify-self-start lg:justify-self-end self-center order-1 space-x-1">
          {actions}
        </div>
      )}
    </header>
  )
}

export { ProductDetailHeader }
