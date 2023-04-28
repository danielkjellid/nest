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
import { FormElement, FormElementObj, FormElementOptions, FormEnum } from './types'
import React, { useEffect, useState } from 'react'

import { ButtonProps } from '../Button'
import { FrontendComponents } from '../../types/'
import { IconUpload } from '@tabler/icons-react'

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

// Sanity check that the list of supportedComponents matches the components defined in the backend.
for (const property in supportedComponents) {
  const supportedValues = Object.values(FrontendComponents)
  if (!supportedValues.includes(property as FrontendComponents)) {
    throw new Error('Component defined in supportedComponents is not a member of FrontendElements.')
  }
}

interface FormProps<T extends object> {
  elements: FormElement
  elementsOptions?: FormElementOptions
  required: string[]
  columns: number
  isMultipart: boolean
  data?: Partial<T> | null
  errors?: Partial<Record<keyof T, string>> | null
  loadingState?: ButtonProps['loadingState']
  onChange: (values: T) => void
}

function Form<T extends object>({
  elements,
  elementsOptions,
  required,
  columns,
  isMultipart,
  data,
  errors,
  loadingState,
  onChange,
}: FormProps<T>) {
  type K = keyof T

  if (!elements) {
    return null
  }

  /*******************************************
   ** Values: defaults, initial and current **
   *******************************************/

  // We want to use controlled elements only, and therefore, we have to be a bit careful with
  // what state we're setting the elements to. For checkboxes, we want to set a boolean, for
  // the file input we want to set null, and for everything else we want to set an empty string.
  const setDefaultFormValues = () => {
    const values = {} as T
    Object.entries(elements).map(([elementKey, element]) => {
      const elemId = elementKey as K

      if ((element as FormElementObj).component === FrontendComponents.CHECKBOX) {
        values[elemId] = (element.defaultValue ? element.defaultValue : false) as T[K]
      } else if ((element as FormElementObj).component === FrontendComponents.FILE_INPUT) {
        values[elemId] = (element.defaultValue ? element.defaultValue : null) as T[K]
      } else {
        values[elemId] = (element.defaultValue ? element.defaultValue : '') as T[K]
      }
    })

    return values
  }

  const getInitialFormValues = () => {
    let initialValues = {} as T

    Object.keys(elements).map((elementKey) => {
      // If we have data passed, we want to set the initial values equal to that of the
      // existing object. If not, just set the defaults for each element.
      if (data && data[elementKey as K] !== undefined) {
        initialValues[elementKey as K] = data[elementKey as K] as T[K]
      } else {
        initialValues = setDefaultFormValues()
      }
    })

    return initialValues
  }

  // The formValues variable controls all state passed back and forth.
  const [formValues, setFormValues] = useState<T>(getInitialFormValues())

  /*************************
   ** Handle form changes **
   *************************/

  // Set the appropriate value based on type of element, with respect to supported
  // values for special elements such as checkboxes and file inputs.
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

  /**********************
   ** Element creation **
   **********************/

  const createCheckboxComponent = (elementKey: K, element: FormElementObj) => {
    if (!elementKey) {
      return null
    }

    const { title } = element
    return (
      <Checkbox
        key={elementKey.toString()}
        label={title}
        disabled={loadingState === 'loading'}
        checked={formValues[elementKey as K] as boolean}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          handleInputChange(elementKey, event)
        }
      />
    )
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
        disabled: loadingState === 'loading',
        onChange: (e: any) => handleInputChange(elementKey, e),
        value: formValues[elementKey as K],
        icon:
          element.component === FrontendComponents.FILE_INPUT ? (
            <IconUpload className="w-4 h-4" />
          ) : undefined,
      })
    )
  }

  /************
   ** Errors **
   ************/

  const getErrorForElement = (elementId: K) => errors && errors[elementId]

  /************
   ** Resets **
   ************/

  // Reset form. This will communicate the change back to the parent as well because of the
  // useEffect bellow firing.
  const resetForm = () => {
    const values = setDefaultFormValues()
    setFormValues({ ...values })
  }

  /***********
   ** Hooks **
   ***********/

  // Back populate the set values to the parent.
  useEffect(() => {
    // We don't want to back populate if the errors object is present, because
    // it would effectively remove the errors.
    if (!errors) {
      onChange(formValues)
    }
  }, [formValues])

  useEffect(() => {
    if (data === null) {
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
