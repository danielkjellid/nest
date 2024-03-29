import React, { Children, useMemo } from 'react'

import { useCommonStyles } from '../../styles/common'
import Empty from '../Empty'

import { useCardStyles } from './Card.styles'

interface CardTableRowProps {
  headers: Header[]
  item: any
}

function CardTableRow({ headers, item }: CardTableRowProps) {
  const { classes } = useCommonStyles()
  const getNestedValue = (obj: any, path: (string | number)[], fallback?: any): any => {
    const last = path.length - 1
    if (last < 0) return obj === undefined ? fallback : obj

    let fetchedObj: any = {}

    for (let i = 0; i < last; i += 1) {
      if (obj == null) {
        return fallback
      }
      fetchedObj = obj[path[i]]
    }

    if (fetchedObj == null) return fallback
    return fetchedObj[path[last]] === undefined ? fallback : fetchedObj[path[last]]
  }

  const getObjectValueByPath = (obj: any, path: string, fallback?: any): any => {
    // credit: http://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key#comment55278413_6491621
    if (obj == null || !path || typeof path !== 'string') return fallback
    if (obj[path] !== undefined) return obj[path]
    let convertedPath = path.replace(/\[(\w+)\]/g, '.$1') // convert indexes to properties
    convertedPath = convertedPath.replace(/^\./, '') // strip a leading dot
    return getNestedValue(obj, convertedPath.split('.'), fallback)
  }

  const sortedItemValues = useMemo(
    () =>
      headers.map((header) => {
        const value = getObjectValueByPath(item, header.value)
        const align = header.align ? header.align : undefined

        return {
          value: value,
          align: align,
        }
      }),
    [headers]
  )
  return (
    <tr className={classes.border}>
      {sortedItemValues.map((obj, i) => (
        <td
          key={i}
          className={`px-6 py-3 text-sm leading-5 ${classes.title} align-top align-${obj.align}`}
        >
          {obj.value}
        </td>
      ))}
    </tr>
  )
}

interface Header {
  label: string
  value: string
  align?: 'left' | 'center' | 'right'
}

interface CardTableProps {
  headers: Header[]
  items?: any[]
  children?: React.ReactNode
}

function CardTable({ headers, items, children }: CardTableProps) {
  const { classes } = useCardStyles()
  const { classes: commonClasses } = useCommonStyles()

  const renderTableContent = () => {
    if (items && items.length) {
      return items.map((item, i) => <CardTableRow key={i} item={item} headers={headers} />)
    }

    if (children && Children.toArray(children).length) {
      return children
    }

    return (
      <tr>
        <td className="sm:px-6 px-4 py-4" colSpan={headers.length + 1}>
          <Empty
            title="No records found"
            message="The data here is currently empty. Please check back later."
            className="w-full"
          />
        </td>
      </tr>
    )
  }

  return (
    <table className="w-full text-sm">
      <thead>
        <tr>
          {headers.map((header) => (
            <th
              className={`${classes.tableHeader} sm:px-6 px-4 py-4 border-b ${commonClasses.border} text-left ${commonClasses.subtitle}`}
              key={header.value}
            >
              {header.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-solid divide-y">{renderTableContent()}</tbody>
    </table>
  )
}

export { CardTable, CardTableRow }
