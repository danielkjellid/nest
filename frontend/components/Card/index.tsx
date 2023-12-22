import React, { Children } from 'react'

import { useCommonStyles } from '../../styles/common'

import { useCardStyles } from './Card.styles'
import { CardForm } from './Form'
import { CardKeyValue } from './KeyValue'
import { CardTable, CardTableRow } from './Table'

interface CardProps {
  title?: string
  subtitle?: string
  children: React.ReactNode
}

function Card({ title, subtitle, children }: CardProps) {
  const { classes } = useCardStyles()
  const { classes: commonClasses } = useCommonStyles()

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

    if (childIsElement({ childrenNodes: childrenNodes, element: 'CardTable' })) {
      return <div>{children}</div>
    } else if (childIsElement({ childrenNodes: childrenNodes, element: 'CardKeyValue' })) {
      return <dl className="divide-solid m-0 divide-y">{children}</dl>
    } else if (childIsElement({ childrenNodes: childrenNodes, element: 'CardForm' })) {
      return <div className="divide-solid sm:px-6 px-4 space-y-6 divide-y">{children}</div>
    } else {
      return <div className="sm:px-6 px-4 py-4">{children}</div>
    }
  }

  return (
    <div className={`${classes.card} overflow-hidden rounded-md shadow`}>
      {title && (
        <div className="sm:px-6 px-4 py-6">
          <h3 className={`text-base font-semibold leading-7 ${commonClasses.title}`}>{title}</h3>
          <p className={`max-w-2xl m-0 text-sm leading-6 ${commonClasses.subtitle}`}>{subtitle}</p>
        </div>
      )}
      <div className={`${commonClasses.border} border-t`}>{renderContainer()}</div>
    </div>
  )
}

Card.KeyValue = CardKeyValue
Card.Table = CardTable
Card.TableRow = CardTableRow
Card.Form = CardForm

export { Card }
