import { notifications } from '@mantine/notifications'
import Ajv from 'ajv'
import { useEffect, useState } from 'react'

import { type ButtonProps } from '../../components/Button'
import { type FormElement } from '../../components/Form/types'
import { performPost as httpPost } from '../fetcher/http'

import formsSchema from './forms.json'
import { buildMultipartForm } from './multipart'

interface FormComponentSchema {
  properties: FormElement
  required: string[]
  columns: number
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

export function useForm<T extends object>({
  key,
  initialData = null,
  isMultipart = false,
}: {
  key: keyof (typeof formsSchema)['definitions']
  initialData?: Partial<T> | null
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
    if (initialData) {
      setFormData(initialData)
      setFormKey(key)
    }
  }, [initialData])

  const onChange = (val: Partial<T>) => {
    // If we have fields with errors that are part of the onChange payload, we want to "resolve"
    // errors for those fields, but keep errors for fields that have not change since the erroneous
    // state.
    if (formData && errors) {
      const updatedErrors = { ...errors }
      Object.keys(val).map((valueKey) => {
        const keyFromValue = valueKey as keyof T
        if (
          val[keyFromValue] &&
          val[keyFromValue] !== formData[keyFromValue] &&
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
    if (validator.errors) {
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
    if (formData) setFormData(null)
    if (errors) setErrors(null)
    setLoadingState('initial')
  }

  /*************
   ** Payload **
   *************/

  const buildPayload = (): any => {
    if (!formData) return

    if (isMultipart) {
      return { data: buildMultipartForm<T>(formData), options: { isMultipart: true } }
    }

    // Convert empty string values to null.
    Object.entries(formData).map(([key, val]) => {
      if (val === '') formData[key as keyof T] = null as T[keyof T]
    })

    return { formData, options: {} }
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
