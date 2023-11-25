import { type ForwardRefExoticComponent } from 'react'

import { type FrontendComponents } from '../../types'

export type FormEnum = { label: string; value: string }

export interface FormElementOptionsObj {
  beforeSlot?: React.ReactNode
  afterSlot?: React.ReactNode
  options?: FormEnum[]
  helpText?: string
  placeholder?: string
  accessorKey?: string
  searchable?: boolean
  itemComponent?: ForwardRefExoticComponent<any>
}

export interface FormElementOptions {
  [x: string]: FormElementOptionsObj
}

export interface FormElementObj {
  title: string
  helpText?: string | null
  component: string
  defaultValue?: string | number | boolean | null
  placeholder?: string | null
  hiddenLabel?: boolean
  colSpan?: number | null
  section?: string | null
  type: string
  // enum?: FormEnum[]
  order: number
  min?: number | null
  max?: number | null
}

export interface FormElement {
  [x: string]: FormElementObj
}
