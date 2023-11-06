/* eslint-disable indent */
import { useCallback, useMemo, useRef, useState } from 'react'
import useSWR from 'swr'
import { v4 as uuid } from 'uuid'

import { RequestError, makeQuery, performGet, performPost } from './http'
import {
  LazyRequestHookOptions,
  LazyRequestOptions,
  RequestHookOptions,
  RequestQuery,
  RequestResult,
  RequestTuple,
  URL,
} from './types'

/**
 * useFetch fetches data on render.
 *
 * Example:
 *
 * interface User {id: number; name: string;}
 * interface UserFilter {isActive: boolean;}
 *
 * const urls = {
 *   default: () => '/api/v1/users',
 * }
 *
 * const useList = (query?: Partial<UserFilter>) =>
 *     useFetcher<User[], UserFilter>(urls.default(), { query }),
 *
 * const {data} = useList({isActive: false})
 */
export const useFetch = <TData = any, TQuery = RequestQuery>(
  url: URL,
  options: RequestHookOptions<TData, TQuery> = {}
): RequestResult<TData> => {
  const { getter = performGet, query } = options
  const { data, error, mutate, isValidating } = useSWR<TData, RequestError>(
    url + makeQuery(query),
    () => getter<TData>({ url: url as string, options: options as any })
  )

  const loading = useMemo<boolean>(
    () => !data && !error && isValidating,
    [data, error, isValidating]
  )

  return { data, error, loading, called: true, reload: () => mutate() }
}

/**
 * useLazyFetch lets you execute an explicit http call.
 *
 * Example:
 *
 * interface User {id: number; name: string;}
 *
 * const urls = {
 *     detail: (id: number) => `/api/v1/users/${id}`,
 * };
 *
 * const [update, result] = useLazyFetcher<Partial<User>>({
 *     setter: performPut,
 * });
 *
 * update(urls.detail(1), { name: 'Updated name' });
 */
export const useLazyFetch = <TData = any, TQuery = RequestQuery, TResponseData = TData>(
  baseOptions: LazyRequestHookOptions = {}
): RequestTuple<TData, TResponseData> => {
  const { setter = performPost } = baseOptions
  const called = useRef<boolean>(false)
  const [loading, setLoading] = useState<boolean>(false)

  // We do not have a reference to the api call we are going to execute here.
  const ref = useRef<string>(uuid())

  const { data, error, mutate } = useSWR<TResponseData | undefined, RequestError>(
    ref.current,
    () => undefined,
    {
      // We want to disable the revalidation here, the hook is lazy and we don't
      // have the correct setter function by default.
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
      shouldRetryOnError: false,
    }
  )

  const call = useCallback<
    (url: string, options?: LazyRequestOptions<TData, TQuery>) => Promise<TResponseData | undefined>
  >(
    async (
      url: string,
      options?: LazyRequestOptions<TData, TQuery>
    ): Promise<TResponseData | undefined> => {
      called.current = true
      try {
        setLoading(true)
        const response = await mutate(
          setter<TResponseData>({ url: url + makeQuery(options?.query), data: options?.data }),
          false
        )

        setLoading(false)
        return response
      } catch (e) {
        setLoading(false)
        throw e
      }
    },
    [called, setter, mutate]
  )

  if (!called.current) {
    return [call, { called: false, loading, data: undefined, error: undefined }]
  }

  return [
    call,
    {
      data,
      error,
      loading,
      called: true,
    },
  ]
}
