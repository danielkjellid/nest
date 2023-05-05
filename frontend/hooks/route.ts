import { useMemo } from 'react'

export function useStrippedRoute(prefix: string): (url: string) => string {
  return useMemo(() => (url: string) => url.replace(prefix, ''), [prefix])
}
