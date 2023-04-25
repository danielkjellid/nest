import schema from '../../../schema.json'
import { useState } from 'react'

interface FormMeta {}

const findFormByTitle = (obj: Record<string, any>, key: string): any => {
  if (obj && typeof obj === 'object') {
    for (const val of Object.values(obj)) {
      if (val && val['title'] && val['title'] === key) {
        return val
      } else {
        const found = findFormByTitle(val, key)
        if (found) return found
      }
    }
  }
}

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

const useForm = (key: string) => {
  const [isMultipart, setIsMultipart] = useState(determineIsMultipart(schema))
  const [formMeta, setFormMeta] = useState({})

  const formData = findFormByTitle(schema, key)
  const form = formData.properties

  return form
}

export { useForm }
