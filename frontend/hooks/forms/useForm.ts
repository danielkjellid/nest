import { FormElement } from '../../components/Form'
import humps from 'humps'
import schema from '../../../schema.json'
import { useState } from 'react'

const determineIsMultipart = (obj: Record<string, any>, formKey: string): any => {
  if (obj && typeof obj === 'object') {
    for (const [key, value] of Object.entries(obj)) {
      if (key && key === 'multipart/form-data') {
        return value.schema.$ref.split('/').includes(formKey)
      } else {
        const found = determineIsMultipart(value, formKey)
        if (found !== undefined) return found as boolean
      }
    }
  }
}

interface FormComponent {
  properties: FormElement
  required: string[]
  columns: number
  isMultipart: boolean
}

function buildMultipartForm<T extends object>(data: Partial<T>): FormData {
  const fd = new FormData()

  // When appending to form data, it converts available types to string,
  // even undefined or null. Therefore we need to explicitly check if
  // the field has any value before appending it to make error flow good.
  Object.entries(data).forEach(([key, value]) => {
    // Multipart form data does not run through the parser in the backend,
    // so we need to decamelize values here.
    const decamelizedKey = humps.decamelize(key)

    if (value !== undefined && value !== null && value !== '') {
      if (Array.isArray(value)) {
        value.forEach((val) => {
          if (val instanceof File) {
            fd.append(`${decamelizedKey}[]`, val)
          } else {
            fd.append(decamelizedKey, JSON.stringify(val))
          }
        })
      } else if (value instanceof File) {
        fd.append(decamelizedKey, value)
      } else if (typeof value === 'boolean') {
        fd.append(decamelizedKey, JSON.stringify(value))
      } else {
        fd.append(decamelizedKey, value.toString())
      }
    }
  })

  return fd
}

function useForm<T extends object>({
  key,
  existingObj,
}: {
  key: string
  existingObj?: Partial<T>
}) {
  const formFromSchema = (schema as any).components.schemas[key] as FormComponent
  const isMultipart = determineIsMultipart(schema, key)

  const [data, setData] = useState<Partial<T> | null>(existingObj || ({} as T))

  const buildPayload = (): FormData | Partial<T> | undefined => {
    if (!data) return

    if (isMultipart) {
      return buildMultipartForm<T>(data)
    }

    return data
  }

  const onChange = (val: any) => setData(val)

  const [errors, setErrors] = useState<Partial<Record<keyof T, string>> | null>(null)

  const resetErrors = () => {
    setErrors(null)
  }

  const resetForm = () => {
    if (data) {
      setData(null)
    }
    setErrors(null)
  }

  return {
    data,
    elements: formFromSchema.properties,
    required: formFromSchema.required,
    columns: formFromSchema.columns,
    isMultipart,
    errors,
    setErrors,
    resetErrors,
    onChange,
    buildPayload,
    resetForm,
  }
}

export { useForm }
