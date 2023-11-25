import { type FormElementObj, type FormElement } from '../../components/Form/types'

import { type SchemaFormElementObj, type SchemaFormElement } from './types'

type K = keyof FormElementObj
type KS = keyof SchemaFormElementObj
type Mapping = Record<KS, K>

const MAPPING: Mapping = {
  title: 'title',
  type: 'type',
  enum: 'enum',
  'x-helpText': 'helpText',
  'x-component': 'component',
  'x-defaultValue': 'defaultValue',
  'x-placeholder': 'placeholder',
  'x-hiddenLabel': 'hiddenLabel',
  'x-colSpan': 'colSpan',
  'x-section': 'section',
  'x-order': 'order',
  'x-min': 'min',
  'x-max': 'max',
}

const convertProperty = (property: SchemaFormElementObj): FormElementObj => {
  const mapping = (key: KS): K => MAPPING[key] as K
  const convertedProperty: Partial<FormElementObj> = {}

  Object.entries(property).map(([k, v]) => {
    const mappedKey = mapping(k as KS)
    convertedProperty[mappedKey] = v
  })

  return convertedProperty as FormElementObj
}

const convertSchemaElemToFormElem = (schemaProperties: SchemaFormElement): FormElement => {
  const convertedProperties: Partial<FormElement> = {}

  Object.entries(schemaProperties).map(([key, property]) => {
    convertedProperties[key] = convertProperty(property)
  })

  return convertedProperties as FormElement
}

export { convertSchemaElemToFormElem }
