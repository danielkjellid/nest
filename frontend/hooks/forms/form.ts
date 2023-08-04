import { buildMultipartForm, determineIsMultipart } from './multipart'
import { useEffect, useState } from 'react'

import { ButtonProps } from '../../components/Button'
import { FormElement } from '../../components/Form/types'
import { performPost as httpPost } from '../fetcher/http'
import { notifications } from '@mantine/notifications'
import schema from '../../../schema.json'

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

  const [data, setData] = useState<Partial<T> | null>(null)

  useEffect(() => {
    if (existingObj) {
      setData(existingObj)
      setFormKey(key)
    }
  }, [existingObj])

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

  const [errors, setErrors] = useState<Partial<Record<keyof T, string>> | null>({})
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

  const buildPayload = (): any => {
    if (!data) return

    if (isMultipart) {
      return { data: buildMultipartForm<T>(data), options: { isMultipart: true } }
    }

    return { data, options: {} }

    // return data
  }

  /*******************
   ** Loading state **
   *******************/

  const [loadingState, setLoadingState] = useState<ButtonProps['loadingState']>('initial')

  /**********
   ** Http **
   **********/

  const performPost = async ({ url }: { url: string }) => {
    try {
      setLoadingState('loading')
      await httpPost({
        url,
        ...buildPayload(),
      })
      notifications.show({
        title: 'Changes were saved successfully',
        message: 'Your changes were saves successfully.',
        color: 'green',
      })
      setLoadingState('success')
    } catch (e) {
      const error = e as any
      setLoadingState('error')
      if (error && error.response && error.response.data) {
        setErrors(error.response.data)
      }
      console.log(e)
    }
  }

  /**********
   ** Misc **
   **********/

  const [formKey, setFormKey] = useState(new Date().toDateString())
  const formFromSchema = (schema as any).components.schemas[key] as FormComponentSchema
  const isMultipart = determineIsMultipart(schema.paths, key)

  return {
    key: formKey,
    data,
    setData,
    onChange,
    errors,
    setErrors,
    resetErrors,
    buildPayload,
    resetForm,
    loadingState,
    setLoadingState,
    performPost,
    elements: formFromSchema.properties,
    required: formFromSchema.required,
    columns: formFromSchema.columns,
    isMultipart,
  }
}
