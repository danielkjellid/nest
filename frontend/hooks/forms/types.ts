import { type FormEnum } from '../../components/Form/types'

export interface SchemaFormElementObj {
  title: string
  type: string
  enum?: FormEnum[]
  'x-helpText'?: string | null
  'x-component': string
  'x-defaultValue'?: string | number | boolean | null
  'x-placeholder'?: string | null
  'x-hiddenLabel'?: boolean
  'x-colSpan'?: number | null
  'x-section'?: string | null
  'x-order': number
  'x-min'?: number | null
  'x-max'?: number | null
}

export interface SchemaFormElement {
  [x: string]: SchemaFormElementObj
}
