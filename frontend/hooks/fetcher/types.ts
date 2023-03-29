import { RequestError } from './http'

export type Getter = <T>(url: string, options?: RequestOptions) => Promise<T>
export type Setter = <T>(url: string, data: any, options?: RequestOptions) => Promise<T>

export interface RequestOptions extends RequestInit {
  noContentTypeHeader?: boolean
}

// OperationQuery
export type RequestQuery = Record<string, number | boolean | string>

type URLType = string | null
type URLFunction = () => URLType
// URLInterface
export type URL = URLFunction | URLType

// QueryHookOptions
export interface RequestHookOptions<TData, TQuery> {
  getter?: Getter
  query?: Partial<TQuery>
  data?: TData
}

export interface LazyRequestHookOptions<TData, TQuery> {
  setter?: Setter
}

// QueryResult
export interface RequestResult<TData, TQuery> {
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

export type LazyRequestResult<TData, TQuery> =
  | PendingLazyRequestResult
  | Omit<RequestResult<TData, TQuery>, 'reload'>

export interface LazyRequestOptions<TData, TQuery> {
  query?: Partial<TQuery>
  data?: TData
}

export type RequestTuple<TData, TQuery, TResponseData> = [
  (url: string, options?: LazyRequestResult<TData, TQuery>) => Promise<TResponseData | undefined>,
  LazyRequestResult<TResponseData, TQuery>
]
