import { FormElement } from '../../components/Form'
import schema from '../../../schema.json'

const determineIsMultipart = (obj: Record<string, any>): any => {
  if (obj && typeof obj === 'object') {
    for (const [key, value] of Object.entries(obj)) {
      if (key && key === 'multipart/form-data') {
        return true
      } else {
        const found = determineIsMultipart(value)
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

function useForm(key: string) {
  const isMultipart = determineIsMultipart(schema)

  // console.log(Object.entries(schema.components.schemas).find(([k, v]) => k === key))
  const formData = (schema as any).components.schemas[key] as FormComponent

  const f = {
    elements: formData.properties,
    required: formData.required,
    columns: formData.columns,
    isMultipart,
  }

  return f
}

export { useForm }
