import { notifications } from '@mantine/notifications'
import Ajv from 'ajv'
import addFormats from 'ajv-formats'
import { useEffect, useState } from 'react'

import openAPISchema from '../../../schema.json'
import { type ButtonProps } from '../../components/Button'
import { performPost as httpPost } from '../fetcher/http'

import { buildMultipartForm } from './multipart'
import { type SchemaFormElement } from './types'
import { convertSchemaElemToFormElem } from './utils'

interface FormComponentSchema {
  title: string
  type: string
  properties: SchemaFormElement
  required: string[]
  'x-columns': number
  'x-form': boolean
}

const useValidator = () => {
  const ajv = new Ajv({ allErrors: true })

  // We use Ajv in strict mode, so we need to whitelist the extra
  // attributes we're using.
  ajv.addKeyword('x-helpText')
  ajv.addKeyword('x-component')
  ajv.addKeyword('x-defaultValue')
  ajv.addKeyword('x-placeholder')
  ajv.addKeyword('x-hiddenLabel')
  ajv.addKeyword('x-colSpan')
  ajv.addKeyword('x-section')
  ajv.addKeyword('x-order')
  ajv.addKeyword('x-min')
  ajv.addKeyword('x-max')
  ajv.addKeyword('x-columns')
  ajv.addKeyword('x-form')
  ajv.addKeyword('x-enum')

  addFormats(ajv)

  return ajv
}

export function useForm<T extends object>({
  key,
  initialData = null,
  isMultipart = false,
}: {
  key: keyof (typeof openAPISchema)['components']['schemas']
  initialData?: Partial<T> | null
  isMultipart?: boolean
}) {
  /**********
   ** Data **
   **********/
  const [formData, setFormData] = useState<Partial<T> | null>(null)
  const rawSchema = openAPISchema['components']['schemas'][key]
  const schema = rawSchema as FormComponentSchema

  // Some keys are ignored as ajv cannot resolve the proper referenced
  // type.
  const ignoredKeys = ['anyOf', 'allOf', 'oneOf']
  Object.values(schema.properties).forEach((property) => {
    ignoredKeys.forEach((key) => {
      if (Object.keys(property).includes(key)) {
        // @ts-ignore
        delete property[key]
      }
    })
  })

  const validator = useValidator()
  validator.compile(schema)

  useEffect(() => {
    if (initialData) {
      setFormData(structuredClone(initialData))
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

    if (validator.errors) {
      validator.errors.map((error) => {
        const pathParts = error.instancePath.split('/')
        const inputKey = pathParts[pathParts.length - 1]
        const errorMsg = error.message

        if (!inputKey || !errorMsg || !schema.required.includes(inputKey)) return
        console.error(error)
        // @ts-ignore
        errors[inputKey] = errorMsg.charAt(0).toUpperCase() + errorMsg.slice(1).toLocaleLowerCase()
      })
    }

    setErrors(errors)
    return !Object.keys(errors).length
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
    const isValid = validate()

    if (!isValid) return

    if (isMultipart) {
      return { data: buildMultipartForm<T>(formData), options: { isMultipart: true } }
    }

    // Convert empty string values to null.
    Object.entries(formData).map(([key, val]) => {
      if (val === '') formData[key as keyof T] = null as T[keyof T]
    })

    return { data: formData, options: {} }
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
        url: url,
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
    onChange: onChange,
    errors: errors,
    setErrors: setErrors,
    resetErrors: resetErrors,
    buildPayload: buildPayload,
    resetForm: resetForm,
    validate: validate,
    loadingState: loadingState,
    setLoadingState: setLoadingState,
    performPost: performPost,
    elements: convertSchemaElemToFormElem(schema.properties),
    required: schema.required,
    columns: schema['x-columns'],
    isMultipart: isMultipart,
  }
}
