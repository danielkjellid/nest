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
import { IconUpload } from '@tabler/icons-react'
import React, { ForwardRefExoticComponent, useEffect, useState } from 'react'

import { FrontendComponents } from '../../types/'
import { ButtonProps } from '../Button'
import { Counter } from '../Counter'

import { FormElement, FormElementObj, FormElementOptions, FormEnum } from './types'



const supportedComponents = {
  Autocomplete,
  Checkbox,
  Chip,
  ColorInput,
  Counter,
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

  const getOptionsForElement = ({ elementKey }: { elementKey: string }) =>
    elementsOptions && elementsOptions[elementKey]

  const getDefaultForElement = ({ element }: { element: FormElementObj }) => {
    if ((element as FormElementObj).component === FrontendComponents.Checkbox) {
      return (element.defaultValue ? element.defaultValue : false) as T[K]
    } else if ((element as FormElementObj).component === FrontendComponents.FileInput) {
      return (element.defaultValue ? element.defaultValue : null) as T[K]
    } else {
      return (element.defaultValue ? element.defaultValue : '') as T[K]
    }
  }

  // We want to use controlled elements only, and therefore, we have to be a bit careful with
  // what state we're setting the elements to. For checkboxes, we want to set a boolean, for
  // the file input we want to set null, and for everything else we want to set an empty string.
  const setDefaultFormValues = () => {
    const values = {} as T
    Object.entries(elements).map(([elementKey, element]) => {
      const elemId = elementKey as K
      values[elemId] = getDefaultForElement({ element })
    })

    return values
  }

  const getAccessorKeyValue = ({ accessorKey, obj }: { accessorKey: string; obj: any }) => {
    const accessorValue = accessorKey.split('.').reduce((o, i) => (o ? o[i] : ''), obj)
    return accessorValue
  }

  const getInitialFormValues = ({
    initialData,
  }: {
    initialData: Partial<T> | null | undefined
  }) => {
    let initialValues = {} as T

    Object.entries(elements).map(([elementKey, element]) => {
      if (initialData) {
        const elemOptions = getOptionsForElement({ elementKey })
        if (elemOptions && elemOptions.accessorKey) {
          const accessorValue = getAccessorKeyValue({
            accessorKey: elemOptions.accessorKey,
            obj: initialData,
          })

          initialValues[elementKey as K] = accessorValue
            ? (accessorValue.toString() as T[K])
            : getDefaultForElement({ element })
        } else if (initialData[elementKey as K] !== null) {
          initialValues[elementKey as K] = initialData[elementKey as K] as T[K]
        } else {
          initialValues[elementKey as K] = getDefaultForElement({ element })
        }
      } else {
        initialValues = setDefaultFormValues()
      }
    })

    return initialValues
  }

  // The formValues variable controls all state passed back and forth.
  const [formValues, setFormValues] = useState<T>(getInitialFormValues({ initialData: data }))

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
      if (
        typeof eventOrValue === 'string' ||
        typeof eventOrValue === 'number' ||
        eventOrValue instanceof File
      ) {
        value = eventOrValue
      } else {
        const eventTarget = eventOrValue.currentTarget as HTMLInputElement

        if (eventTarget) {
          if (eventTarget.type === 'checkbox') {
            value = eventTarget.checked
          } else {
            value = eventTarget.value
          }
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

  const createCheckboxComponent = ({
    elementKey,
    element,
    helpText,
    disabled,
  }: {
    elementKey: K
    element: FormElementObj
    helpText?: string
    disabled?: boolean
  }) => {
    if (!elementKey) {
      return null
    }

    const { title } = element
    return (
      <Checkbox
        key={elementKey.toString()}
        label={title}
        description={helpText ? helpText : element.helpText}
        disabled={disabled ? disabled : loadingState === 'loading'}
        checked={formValues[elementKey as K] as boolean}
        className={`w-full col-span-${element.colSpan ? element.colSpan : columns}`}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          handleInputChange(elementKey, event)
        }
      />
    )
  }

  const createFormComponent = ({
    elementKey,
    element,
    options,
    placeholder,
    helpText,
    disabled,
    searchable,
    itemComponent,
  }: {
    elementKey: K
    element: FormElementObj
    options?: FormEnum[]
    placeholder?: string
    helpText?: string
    disabled?: boolean
    searchable?: boolean
    itemComponent?: ForwardRefExoticComponent<any>
  }) => {
    // The checkbox component uses slightly different properties than the other supported components.
    if (element.component === FrontendComponents.Checkbox) {
      return createCheckboxComponent({ elementKey, element })
    }

    // Sanitize options, all values need to be string.
    if (options) {
      options = options.map((option) => ({
        ...option,
        label: option.label,
        value: option.value.toString(),
      }))
    }

    return (
      // @ts-ignore
      React.createElement(supportedComponents[element.component], {
        key: elementKey,
        placeholder: placeholder ? placeholder : element.placeholder,
        required: required && required.includes(elementKey as string),
        label: !element.hiddenLabel ? element.title : undefined,
        'aria-label': element.hiddenLabel ? element.title : undefined,
        description: helpText ? helpText : element.helpText,
        data: options || [],
        error: getErrorForElement(elementKey),
        className: `w-full col-span-${element.colSpan ? element.colSpan : columns}`,
        disabled: disabled ? disabled : loadingState === 'loading',
        searchable: searchable ? searchable : undefined,
        itemComponent: itemComponent ? itemComponent : undefined,
        onChange: (e: any) => handleInputChange(elementKey, e),
        min: element.min ? element.min : undefined,
        max: element.max ? element.max : undefined,
        value: formValues[elementKey as K],
        icon:
          element.component === FrontendComponents.FileInput ? (
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
        {Object.entries(elements as T)
          .sort(([, a], [, b]) => a.order - b.order)
          .map(([key, element]) => {
            if (element.component) {
              const optionsForElem = getOptionsForElement({ elementKey: key })
              if (optionsForElem !== undefined) {
                const options = element.enum
                  ? element.enum
                  : optionsForElem.options
                  ? optionsForElem.options
                  : undefined

                return (
                  <div
                    key={key.toString()}
                    className={`flex items-end space-x-3 w-full col-span-${
                      element.colSpan ? element.colSpan : columns
                    }`}
                  >
                    {optionsForElem.beforeSlot}
                    {createFormComponent({
                      elementKey: key as K,
                      element,
                      options: options,
                      placeholder: optionsForElem.placeholder,
                      helpText: optionsForElem.helpText,
                      searchable: optionsForElem.searchable,
                      itemComponent: optionsForElem.itemComponent,
                    })}
                    {optionsForElem.afterSlot}
                  </div>
                )
              } else {
                return createFormComponent({ elementKey: key as K, element, options: element.enum })
              }
            }
          })}
      </div>
    </form>
  )
}

export default Form
