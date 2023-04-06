import React, { useEffect, useRef } from 'react'

import Error from './Error'
import { ErrorProps } from './Error'
import Loading from './Loading'
import { LoadingProps } from './Loading'
import { RequestResult } from '../../hooks/fetcher'

export type HooksResult<THooks extends object> = {
  [k in keyof THooks]: THooks[k] extends RequestResult<unknown>
    ? NonNullable<THooks[k]['data']>
    : never
}

interface ViewProps<THooks extends object, ComponentProps extends object> {
  component: React.ComponentType<{ results: HooksResult<THooks> } & ComponentProps> | null
  componentProps: Omit<ComponentProps, 'results'>
  results: THooks
  loadingProps?: LoadingProps
  initialLoadOnly?: boolean
  errorProps: ErrorProps
}

function View<THooks extends object, ComponentProps extends object>({
  component: Component,
  componentProps,
  results,
  loadingProps,
  errorProps,
  initialLoadOnly = false,
}: ViewProps<THooks, ComponentProps>) {
  /***********
   ** Error **
   ***********/

  const error = Object.values(results).some(
    (result) => result && typeof result.error !== 'undefined'
  )

  /**********
   ** Data **
   **********/

  const data: { [key: string]: any } = {}

  for (const [key, value] of Object.entries(results)) {
    data[key] = value.data
  }

  const dataLoaded = Object.values(data).every((val) => typeof val !== 'undefined')

  /*************
   ** Loading **
   *************/

  const loading = Object.values(results).some((result) => result.loading)

  // Initial load handling - We want to disable the loading
  // indicator in some cases (during polling).
  const initialRunRef = useRef(true)
  const allowLoading = initialLoadOnly ? initialRunRef.current || !dataLoaded : true

  useEffect(() => {
    initialRunRef.current = false
  }, [initialRunRef])

  if (error) {
    return <Error {...errorProps} />
  }

  if (loading && allowLoading) {
    return <Loading {...loadingProps} />
  }

  if (dataLoaded && Component) {
    return (
      <Component results={data as HooksResult<THooks>} {...(componentProps as ComponentProps)} />
    )
  }

  return null
}

export default View
