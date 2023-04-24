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
import {
  FormElementEnumRecord,
  FormElementRecord,
  FormRecord,
  FrontendComponents,
} from '../../types'
import React, { useState } from 'react'

import { IconUpload } from '@tabler/icons-react'
import { useForm } from '@mantine/form'

interface FormElementOptionsObj {
  beforeSlot?: React.ReactNode
  afterSlot?: React.ReactNode
  options?: FormElementEnumRecord[]
}

interface FormElementOptions {
  [x: string]: FormElementOptionsObj
}

interface FormProps<T extends object> {
  form?: FormRecord
  existingObj?: Partial<T>
  elementOptions?: FormElementOptions
  errors?: Record<keyof T, any>
  onChange?: (values: T) => void
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
  form,
  elementOptions,
  existingObj,
  errors,
  onChange,
}: FormProps<T>) {
  type K = keyof T

  if (!form) {
    return null
  }

  const getInitialFormValues = (form: FormRecord) => {
    const initialValues = {} as T
    form.elements.map((element) => {
      const elemId = element.id as K

      if (existingObj && existingObj[elemId] !== undefined) {
        initialValues[elemId] = existingObj[elemId] as T[K]
      } else if (element.component === FrontendComponents.CHECKBOX) {
        initialValues[elemId] = (
          element.defaultValue !== null ? element.defaultValue : false
        ) as T[K]
      } else if (element.component === FrontendComponents.FILE_INPUT) {
        initialValues[elemId] = (
          element.defaultValue !== null ? element.defaultValue : null
        ) as T[K]
      } else {
        initialValues[elemId] = (element.defaultValue !== null ? element.defaultValue : '') as T[K]
      }
      return initialValues
    })
    return initialValues
  }

  const [formValues, setFormValues] = useState<T>(getInitialFormValues(form))

  const handleInputChange = (
    key: string,
    eventOrValue: React.ChangeEvent<HTMLInputElement> | string | File | null
  ) => {
    let value

    if (eventOrValue) {
      if (typeof eventOrValue === 'string' || eventOrValue instanceof File) {
        value = eventOrValue
      } else {
        const eventTarget = eventOrValue.currentTarget as HTMLInputElement

        if (eventTarget.checked !== undefined) {
          value = eventTarget.checked
        } else {
          value = eventTarget.value
        }
      }
    } else {
      value = null
    }

    setFormValues({ ...formValues, [key]: value })
  }

  const createCheckboxComponent = (element: FormElementRecord) => {
    const { id, title } = element
    return (
      <Checkbox
        key={id}
        label={title}
        checked={formValues[id as K] as boolean}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => handleInputChange(id, event)}
      />
    )
  }

  const getErrorForElement = (elementId: string) => {
    const errorForElement =
      errors && Object.entries(errors).find(([key, value]) => key === elementId)

    return errorForElement ? errorForElement[1] : undefined
  }

  const createFormComponent = (element: FormElementRecord, options?: FormElementEnumRecord[]) => {
    // The checkbox component uses slightly different properties than the other supported components.
    if (element.component === FrontendComponents.CHECKBOX) {
      return createCheckboxComponent(element)
    }

    return (
      // @ts-ignore
      React.createElement(supportedComponents[element.component], {
        key: element.id,
        placeholder: element.placeholder,
        required: form.required.includes(element.id),
        label: !element.hiddenLabel ? element.title : undefined,
        'aria-label': element.hiddenLabel ? element.title : undefined,
        description: element.helpText,
        data: options || [],
        error: getErrorForElement(element.id),
        className: `w-full col-span-${element.colSpan ? element.colSpan : form.columns}`,
        onChange: (e: any) => handleInputChange(element.id, e),
        value: formValues[element.id as K],
        icon:
          element.component === FrontendComponents.FILE_INPUT ? (
            <IconUpload className="w-4 h-4" />
          ) : undefined,
      })
    )
  }

  return (
    <form
      encType={form.isMultipartForm ? 'multipart/form-data' : undefined}
      onSubmit={() => onChange(formValues)}
    >
      <div className={`grid grid-cols-${form.columns ? form.columns : 1} gap-4 items-end`}>
        {form.elements.map((element) => {
          if (element.component) {
            const optionsForElem =
              elementOptions !== undefined ? elementOptions[element.id] : undefined
            if (optionsForElem !== undefined) {
              const options = element.enum
                ? element.enum
                : optionsForElem.options
                ? optionsForElem.options
                : undefined

              return (
                <div key={element.id} className="flex items-end space-x-3 w-full">
                  {optionsForElem.beforeSlot}
                  {createFormComponent(element, options)}
                  {optionsForElem.afterSlot}
                </div>
              )
            } else {
              return createFormComponent(element, element.enum)
            }
          }
        })}
      </div>
    </form>
  )
}

export default Form
