import { RequestError } from './http'

export type Getter = <T>(url: string, options?: RequestOptions) => Promise<T>
export type Setter = <T>(url: string, data: any, options?: RequestOptions) => Promise<T>

export interface RequestOptions extends RequestInit {
  noContentTypeHeader?: boolean
}

export type RequestQuery = Record<string, number | boolean | string>

type URLType = string | null
type URLFunction = () => URLType
export type URL = URLFunction | URLType

export interface RequestHookOptions<TData, TQuery> {
  getter?: Getter
  query?: Partial<TQuery>
  data?: TData
}

export interface LazyRequestHookOptions {
  setter?: Setter
}

export interface RequestResult<TData> {
  data: TData | undefined
  error?: RequestError
  loading: boolean
  called: true
  reload: () => void
}

export interface PendingLazyRequestResult {
  data: undefined
  error: undefined
  loading: boolean
  called: false
}

export type LazyRequestResult<TData> =
  | PendingLazyRequestResult
  | Omit<RequestResult<TData>, 'reload'>

export interface LazyRequestOptions<TData, TQuery> {
  query?: Partial<TQuery>
  data?: TData
}

export type RequestTuple<TData, TResponseData> = [
  (url: string, options?: LazyRequestResult<TData>) => Promise<TResponseData | undefined>,
  LazyRequestResult<TResponseData>
]
