import {
  Autocomplete,
  Checkbox,
  Chip,
  ColorInput,
  FileInput,
  MultiSelect,
  NumberInput,
  PasswordInput,
  PinInput,
  Radio,
  Rating,
  Select,
  Slider,
  Switch,
  TextInput,
  Textarea,
} from '@mantine/core'
import React, { useEffect, useState } from 'react'

import { FrontendComponents } from '../../types/'
import { IconUpload } from '@tabler/icons-react'

type FormEnum = { label: string; value: string }

interface FormElementOptionsObj {
  beforeSlot?: React.ReactNode
  afterSlot?: React.ReactNode
  options?: FormEnum[]
}

interface FormElementOptions {
  [x: string]: FormElementOptionsObj
}

interface FormElementObj {
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

interface FormProps<T extends object> {
  elements: FormElement
  elementsOptions?: FormElementOptions
  required: string[]
  columns: number
  isMultipart: boolean
  data?: Partial<T> | null
  errors?: Partial<Record<keyof T, string>> | null
  onChange: (values: T) => void
}

const supportedComponents = {
  Autocomplete,
  Checkbox,
  Chip,
  ColorInput,
  FileInput,
  MultiSelect,
  PasswordInput,
  PinInput,
  Radio,
  Rating,
  Select,
  Slider,
  Switch,
  Textarea,
  TextInput,
  NumberInput,
}

for (const property in supportedComponents) {
  const supportedValues = Object.values(FrontendComponents)
  if (!supportedValues.includes(property as FrontendComponents)) {
    throw new Error('Component defined in supportedComponents is not a member of FrontendElements.')
  }
}

function Form<T extends object>({
  elements,
  elementsOptions,
  required,
  columns,
  isMultipart,
  data,
  errors,
  onChange,
}: FormProps<T>) {
  type K = keyof T

  if (!elements) {
    return null
  }

  const getInitialFormValues = () => {
    const initialValues = {} as T

    Object.entries(elements).map(([elementKey, element]) => {
      const elemId = elementKey as K

      if (data && data[elemId] !== undefined) {
        initialValues[elemId] = data[elemId] as T[K]
      } else if ((element as FormElementObj).component === FrontendComponents.CHECKBOX) {
        initialValues[elemId] = (element.defaultValue ? element.defaultValue : false) as T[K]
      } else if (element.component === FrontendComponents.FILE_INPUT) {
        initialValues[elemId] = (element.defaultValue ? element.defaultValue : null) as T[K]
      } else {
        initialValues[elemId] = (element.defaultValue ? element.defaultValue : '') as T[K]
      }
      return initialValues
    })
    return initialValues
  }

  const [formValues, setFormValues] = useState<T>(getInitialFormValues())

  const handleInputChange = (
    key: K,
    eventOrValue: React.ChangeEvent<HTMLInputElement> | string | File | null
  ) => {
    let value

    if (eventOrValue) {
      if (typeof eventOrValue === 'string' || eventOrValue instanceof File) {
        value = eventOrValue
      } else {
        const eventTarget = eventOrValue.currentTarget as HTMLInputElement

        if (eventTarget.type === 'checkbox') {
          value = eventTarget.checked
        } else {
          value = eventTarget.value
        }
      }
    } else {
      value = null
    }

    setFormValues({ ...formValues, [key]: value })
    onChange({ ...formValues, [key]: value })
  }

  const createCheckboxComponent = (elementKey: K, element: FormElementObj) => {
    if (!elementKey) {
      return null
    }

    const { title } = element
    return (
      <Checkbox
        key={elementKey.toString()}
        label={title}
        checked={formValues[elementKey as K] as boolean}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          handleInputChange(elementKey, event)
        }
      />
    )
  }

  const getErrorForElement = (elementId: K) => {
    const errorForElement = errors && errors[elementId]

    return errorForElement
  }

  const createFormComponent = (elementKey: K, element: FormElementObj, options?: FormEnum[]) => {
    // The checkbox component uses slightly different properties than the other supported components.
    if (element.component === FrontendComponents.CHECKBOX) {
      return createCheckboxComponent(elementKey, element)
    }

    return (
      // @ts-ignore
      React.createElement(supportedComponents[element.component], {
        key: elementKey,
        placeholder: element.placeholder,
        required: required.includes(elementKey as string),
        label: !element.hiddenLabel ? element.title : undefined,
        'aria-label': element.hiddenLabel ? element.title : undefined,
        description: element.helpText,
        data: options || [],
        error: getErrorForElement(elementKey),
        className: `w-full col-span-${element.colSpan ? element.colSpan : columns}`,
        onChange: (e: any) => handleInputChange(elementKey, e),
        value: formValues[elementKey as K],
        icon:
          element.component === FrontendComponents.FILE_INPUT ? (
            <IconUpload className="w-4 h-4" />
          ) : undefined,
      })
    )
  }

  const resetForm = () => {
    const values = {} as T
    Object.entries(elements).map(([elementKey, element]) => {
      const elemId = elementKey as K

      if ((element as FormElementObj).component === FrontendComponents.CHECKBOX) {
        values[elemId] = (element.defaultValue ? element.defaultValue : false) as T[K]
      } else if ((element as FormElementObj).component === FrontendComponents.FILE_INPUT) {
        values[elemId] = (element.defaultValue ? element.defaultValue : null) as T[K]
      } else {
        console.log(elemId, element)
        values[elemId] = (element.defaultValue ? element.defaultValue : '') as T[K]
      }
    })

    setFormValues({ ...values })
  }

  // Back populate the set values to the parent.
  useEffect(() => {
    onChange(formValues)
  }, [formValues])

  useEffect(() => {
    if (data === null) {
      console.log('is called')
      resetForm()
    }
  }, [data])

  return (
    <form encType={isMultipart ? 'multipart/form-data' : undefined}>
      <div className={`grid grid-cols-${columns ? columns : 1} gap-4 items-end`}>
        {Object.entries(elements as T).map(([key, element]) => {
          if (element.component) {
            const optionsForElem = elementsOptions !== undefined ? elementsOptions[key] : undefined
            if (optionsForElem !== undefined) {
              const options = element.enum
                ? element.enum
                : optionsForElem.options
                ? optionsForElem.options
                : undefined

              return (
                <div key={key.toString()} className="flex items-end space-x-3 w-full">
                  {optionsForElem.beforeSlot}
                  {createFormComponent(key as K, element, options)}
                  {optionsForElem.afterSlot}
                </div>
              )
            } else {
              return createFormComponent(key as K, element, element.enum)
            }
          }
        })}
      </div>
    </form>
  )
}

export default Form
