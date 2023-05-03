import humps from 'humps'

// Recursively iterates the schema and looks for the object key 'multipart/form-data' in
// any of the paths, then it checks if the reference to that object value corresponds with
// the current form key.
export const determineIsMultipart = (obj: Record<string, any>, formKey: string): any => {
  let foundMultipartKey = false
  for (const pathValue of Object.values(obj)) {
    for (const operationValue of Object.values(pathValue)) {
      if ((operationValue as any).requestBody && (operationValue as any).requestBody.content) {
        if ((operationValue as any).requestBody.content['multipart/form-data']) {
          foundMultipartKey = (operationValue as any).requestBody.content[
            'multipart/form-data'
          ].schema.$ref
            .split('/')
            .includes(formKey)
        }
      }
    }
  }

  return foundMultipartKey
}

// Takes current form object and converts it to a valid form data.
export function buildMultipartForm<T extends object>(data: Partial<T>): FormData {
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
