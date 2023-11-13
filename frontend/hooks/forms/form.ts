import { notifications } from '@mantine/notifications'
import Ajv from 'ajv'
import { useEffect, useState } from 'react'

import formsSchema from '../../../forms.json'
import schema from '../../../schema.json'
import { type ButtonProps } from '../../components/Button'
import { type FormElement } from '../../components/Form/types'
import { performPost as httpPost } from '../fetcher/http'

import { buildMultipartForm, determineIsMultipart } from './multipart'

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

    // Convert empty string values to null.
    Object.entries(data).map(([key, val]) => {
      if (val === '') data[key as keyof T] = null as T[keyof T]
    })

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

  async function performPost<T>({ url }: { url: string }) {
    try {
      setLoadingState('loading')
      const response = await httpPost<T>({
        url,
        ...buildPayload(),
      })
      notifications.show({
        title: 'Changes were saved successfully',
        message: 'Your changes were saves successfully.',
        color: 'green',
      })
      setLoadingState('success')
      return response
    } catch (e) {
      const error = e as any
      setLoadingState('error')
      if (error && error.response && error.response.data) {
        setErrors(error.response.data.data)
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

const useValidator = () => {
  const ajv = new Ajv({ allErrors: true })

  // We use Ajv in strict mode, so we need to whitelist the extra
  // attributes we're using.
  ajv.addKeyword('helpText')
  ajv.addKeyword('component')
  ajv.addKeyword('defaultValue')
  ajv.addKeyword('placeholder')
  ajv.addKeyword('hiddenLabel')
  ajv.addKeyword('colSpan')
  ajv.addKeyword('section')
  ajv.addKeyword('order')
  ajv.addKeyword('min')
  ajv.addKeyword('max')
  ajv.addKeyword('columns')
  ajv.addKeyword('xEnumVarnames')

  return ajv
}

export function useForm2<T extends object>({
  key,
  data = null,
  isMultipart = false,
}: {
  key: keyof (typeof formsSchema)['definitions']
  data?: Partial<T> | null
  isMultipart?: boolean
}) {
  /**********
   ** Data **
   **********/

  const [formData, setFormData] = useState<Partial<T> | null>(null)
  const schema = formsSchema['definitions'][key] as FormComponentSchema

  const validator = useValidator()
  validator.compile(schema)

  useEffect(() => {
    if (data) {
      setFormData(data)
      setFormKey(key)
    }
  }, [data])

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
    setFormData(val)
  }

  const validate = () => {
    const errors = {}
    validator.validate(schema, formData || {})

    if (!formData) {
      Object.keys(schema.properties).map((key) => {
        if (schema.required.includes(key)) {
          // @ts-ignore
          errors[key] = 'Field must not be empty'
        }
      })
    }
    console.log(validator.errors)
    if (!errors && validator.errors) {
      validator.errors.map((error) => {
        const pathParts = error.instancePath.split('/')
        const inputKey = pathParts[pathParts.length - 1]
        const errorMsg = error.message

        if (!inputKey || !errorMsg) return undefined

        // @ts-ignore
        errors[inputKey] = errorMsg.charAt(0).toUpperCase() + errorMsg.slice(1).toLocaleLowerCase()
      })
    }

    setErrors(errors)
    return Object.keys(errors).length
  }

  /*******************
   ** Loading state **
   *******************/

  const [loadingState, setLoadingState] = useState<ButtonProps['loadingState']>('initial')

  /************
   ** Errors **
   ************/

  const [errors, setErrors] = useState<Partial<Record<keyof T, string>> | null>({})
  const resetErrors = () => setErrors(null)

  /***********
   ** Reset **
   ***********/

  const resetForm = () => {
    if (data) setFormData(null)
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

    // Convert empty string values to null.
    Object.entries(data).map(([key, val]) => {
      if (val === '') data[key as keyof T] = null as T[keyof T]
    })

    return { data, options: {} }
  }

  /**********
   ** Http **
   **********/

  async function performPost<T>({ url }: { url: string }) {
    const isValid = validate()

    if (!isValid) return

    try {
      setLoadingState('loading')
      const response = await httpPost<T>({
        url,
        ...buildPayload(),
      })
      notifications.show({
        title: 'Changes were saved successfully',
        message: 'Your changes were saves successfully.',
        color: 'green',
      })
      setLoadingState('success')
      return response
    } catch (e) {
      const error = e as any
      setLoadingState('error')
      if (error && error.response && error.response.data) {
        setErrors(error.response.data.data)
      }
      console.log(e)
    }
  }

  /**********
   ** Misc **
   **********/

  const [formKey, setFormKey] = useState(new Date().toDateString())

  return {
    key: formKey,
    data: formData,
    setData: setFormData,
    onChange,
    errors,
    setErrors,
    resetErrors,
    buildPayload,
    resetForm,
    validate,
    loadingState,
    setLoadingState,
    performPost,
    elements: schema.properties,
    required: schema.required,
    columns: schema.columns,
    isMultipart,
  }
}
