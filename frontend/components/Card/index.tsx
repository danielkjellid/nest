import { CardTable, CardTableRow } from './Table'
import React, { Children } from 'react'

import { CardKeyValue } from './KeyValue'
import { useCardStyles } from './Card.styles'

interface CardProps {
  title: string
  subtitle?: string
  children: React.ReactNode
}

function Card({ title, subtitle, children }: CardProps) {
  const { classes } = useCardStyles()

  const childIsElement = ({
    childrenNodes,
    element,
  }: {
    childrenNodes: React.ReactNode[]
    element: string
  }) => {
    return childrenNodes.some(
      (child) =>
        React.isValidElement(child) && typeof child.type !== 'string' && child.type.name === element
    )
  }
  const renderContainer = () => {
    const childrenNodes = Children.toArray(children)

    if (childIsElement({ childrenNodes, element: 'CardTable' })) {
      return <div>{children}</div>
    } else if (childIsElement({ childrenNodes, element: 'CardKeyValue' })) {
      return <dl className="divide-solid m-0 divide-y">{children}</dl>
    } else {
      return <div className="sm:px-6 px-4 py-4">{children}</div>
    }
  }

  return (
    <div className={`${classes.card} overflow-hidden rounded shadow`}>
      <div className="sm:px-6 px-4 py-6">
        <h3 className={`text-base font-semibold leading-7 ${classes.title}`}>{title}</h3>
        <p className={`max-w-2xl m-0 text-sm leading-6 ${classes.subtitle}`}>{subtitle}</p>
      </div>
      <div className={`${classes.border} border-t`}>{renderContainer()}</div>
    </div>
  )
}

Card.KeyValue = CardKeyValue
Card.Table = CardTable
Card.TableRow = CardTableRow

export { Card }
