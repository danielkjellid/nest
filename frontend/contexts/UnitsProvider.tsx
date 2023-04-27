import React, { createContext, useContext, useMemo } from 'react'

import { UnitListOut } from '../types'

export interface UnitsContextType {
  units: UnitListOut[] | undefined
}

const UnitsContext = createContext<UnitListOut[] | undefined>(undefined)

export function useUnits() {
  const ctx = useContext(UnitsContext)

  if (!ctx) {
    throw new Error(
      'useUnits hook was called outside of context, make sure your app is wrapped with UnitsProvider component'
    )
  }

  return ctx
}

interface UnitsProviderProps extends UnitsContextType {
  children: React.ReactNode
}

export function UnitsProvider({ units, children }: UnitsProviderProps) {
  const value = useMemo(() => units, [units])
  return <UnitsContext.Provider value={value}>{children}</UnitsContext.Provider>
}
