import { FrontendComponents } from '../../types'

export type FormEnum = { label: string; value: string }

export interface FormElementOptionsObj {
  beforeSlot?: React.ReactNode
  afterSlot?: React.ReactNode
  options?: FormEnum[]
}

export interface FormElementOptions {
  [x: string]: FormElementOptionsObj
}

export interface FormElementObj {
  title: string
  helpText?: string | null
  component: FrontendComponents
  defaultValue?: string | number | boolean | null
  placeholder?: string | null
  hiddenLabel?: boolean
  colSpan?: number | null
  section?: string | null
  type: string
  enum?: FormEnum[]
}

export interface FormElement {
  [x: string]: FormElementObj
}