import { buildMultipartForm, determineIsMultipart } from './multipart'

import { ButtonProps } from '../../components/Button'
import { FormElement } from '../../components/Form/types'
import schema from '../../../schema.json'
import { useState } from 'react'

interface FormComponentSchema {
  properties: FormElement
  required: string[]
  columns: number
}

export function useForm<T extends object>({
  key,
  existingObj,
}: {
  key: string
  existingObj?: Partial<T>
}) {
  /**********
   ** Data **
   **********/

  const [data, setData] = useState<Partial<T> | null>(existingObj || ({} as T))

  const onChange = (val: Partial<T>) => {
    // If we have fields with errors that are part of the onChange payload, we want to "resolve"
    // errors for those fields, but keep errors for fields that have not change since the erroneous
    // state.
    if (data && errors) {
      const updatedErrors = { ...errors }
      Object.keys(val).map((valueKey) => {
        const keyFromValue = valueKey as keyof T
        if (
          val[keyFromValue] &&
          val[keyFromValue] !== data[keyFromValue] &&
          errors[keyFromValue] !== undefined
        ) {
          delete updatedErrors[keyFromValue]
        }
      })

      setErrors({ ...updatedErrors })
    }

    // Update the data as well.
    setLoadingState('initial')
    setData(val)
  }

  /************
   ** Errors **
   ************/

  const [errors, setErrors] = useState<Partial<Record<keyof T, string>> | null>(null)
  const resetErrors = () => setErrors(null)

  /***********
   ** Reset **
   ***********/

  const resetForm = () => {
    if (data) setData(null)
    if (errors) setErrors(null)
    setLoadingState('initial')
  }

  /*************
   ** Payload **
   *************/

  const buildPayload = (): FormData | Partial<T> | undefined => {
    if (!data) return

    if (isMultipart) {
      console.log('fires')
      return buildMultipartForm<T>(data)
    }

    return data
  }

  /****************
   ** Submission **
   ****************/

  const [loadingState, setLoadingState] = useState<ButtonProps['loadingState']>('initial')

  /**********
   ** Misc **
   **********/

  const formFromSchema = (schema as any).components.schemas[key] as FormComponentSchema
  const isMultipart = determineIsMultipart(schema, key)

  return {
    data,
    onChange,
    errors,
    setErrors,
    resetErrors,
    buildPayload,
    resetForm,
    loadingState,
    setLoadingState,
    elements: formFromSchema.properties,
    required: formFromSchema.required,
    columns: formFromSchema.columns,
    isMultipart,
  }
}
