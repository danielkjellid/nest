import { IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-react'

import React from 'react'
import { useCardStyles } from './Card.styles'

interface CardKeyValueProps {
  k: string
  value: string | React.ReactNode | boolean
}

function CardKeyValue({ k, value }: CardKeyValueProps) {
  const { classes } = useCardStyles()
  return (
    <div className={`${classes.border} sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 px-4 py-4`}>
      <dt className={`text-sm font-medium ${classes.title}`}>{k}</dt>
      {typeof value === 'boolean' ? (
        <dd className="sm:col-span-2 sm:mt-0 mt-1 text-sm">
          {value ? (
            <IconCircleCheckFilled className={classes.iconSuccess} />
          ) : (
            <IconCircleXFilled className={classes.iconDanger} />
          )}
        </dd>
      ) : (
        <dd className={`sm:col-span-2 sm:mt-0 mt-1 text-sm leading-6 ${classes.subtitle}`}>
          {value}
        </dd>
      )}
    </div>
  )
}

export { CardKeyValue }
