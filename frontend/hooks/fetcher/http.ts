import { Getter, RequestOptions, Setter } from './types'

/* eslint-disable @typescript-eslint/ban-ts-comment */
/* eslint-disable indent */
import { APIResponse } from '../../types'
import { decamelize } from 'humps'
import { notifications } from '@mantine/notifications'

const csrfToken = window.csrfToken

export class RequestError extends Error {
  public response?: Response & {
    data?: APIResponse | any
  }

  constructor(message: string, response?: Response, data?: any) {
    super(message)
    this.response = response
    if (this.response) this.response.data = data
  }
}

async function getter<T>({
  url,
  options = {},
}: {
  url: string
  options?: RequestOptions
}): Promise<T> {
  if (!url) {
    throw new Error(`No url provided, got ${url}`)
  }

  if (options.noContentTypeHeader && options.headers) {
    // @ts-ignore
    delete options.headers['Content-Type']
  }

  const response = await fetch(url, {
    credentials: 'same-origin',
    ...options,
    headers: { ...options.headers },
  })

  const data = await response.text()

  if (!response.ok) {
    const error = new RequestError(
      `Got a '${response.status} ${response.statusText}' response.`,
      response,
      JSON.parse(data)
    )

    if (error && error.response?.data?.message) {
      const { message } = error.response.data
      notifications.show({ message, color: 'red' })
    }
    throw error
  }

  const jsonData = data ? JSON.parse(data) : null

  return jsonData as T
}

const setter =
  (method: string): Setter =>
  <T>({ url, data, options = {} }: { url: string; data: any; options?: RequestOptions }) => {
    return getter<T>({
      url: url,
      options: {
        body: options.isMultipart ? data : JSON.stringify(data),
        method,
        ...options,
        headers: {
          'X-CSRFToken': csrfToken,
          ...options.headers,
        },
      },
    })
  }

const encodeQuery = (key: string, value: string | boolean | string[]): string | null => {
  if (value === null || value === undefined) {
    return null
  }

  if (typeof value === 'boolean') {
    return `${encodeURIComponent(decamelize(key))}=${value ? 'true' : 'false'}`
  }

  if (typeof value === 'object') {
    return `${encodeURIComponent(decamelize(key))}=${value
      .filter((v) => v)
      .map(encodeURIComponent)
      .join(',')}`
  }

  return `${encodeURIComponent(decamelize(key))}=${encodeURIComponent(value)}`
}

const queryFactory = (obj: Record<string, any> | undefined) => {
  if (!obj) {
    return ''
  }

  const query = Object.keys(obj)
    .reduce<(string | null)[]>((queryParts, key) => [...queryParts, encodeQuery(key, obj[key])], [])
    .filter((v) => v)
    .join('&')

  return query ? `?${query}` : ''
}

export const performGet: Getter = getter
export const performPost: Setter = setter('post')
export const performPut: Setter = setter('put')
export const performDelete: Setter = setter('delete')
export const makeQuery: typeof queryFactory = queryFactory
