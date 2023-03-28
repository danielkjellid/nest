import React, { createContext, useContext } from 'react'

export interface Home {
  id: number
  address: string
  numResidents: number
  numWeeksRecipeRotation: number
  weeklyBudget: number
  isActive: boolean
}

export interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  fullName: string
  isActive: boolean
  isStaff: boolean
  isSuperuser: boolean
  home?: Home
}

export interface Config {
  isProduction: boolean
}

export interface CommonContextType {
  config: Config
  currentUser: User
  currentHome: Home | null
  availableHomes: Home[]
  setCurrentHome(home: Home): void
}

const CommonContext = createContext<CommonContextType | null>(null)

export function useCommonContext() {
  const ctx = useContext(CommonContext)

  if (!ctx) {
    throw new Error(
      'useCommonContext hook was called outside of context, make sure your app is wrapped with CommonProvider component'
    )
  }

  return ctx
}

interface CommonProviderProps extends CommonContextType {
  children: React.ReactNode
}

export function CommonProvider({
  config,
  currentUser,
  currentHome,
  availableHomes,
  setCurrentHome,
  children,
}: CommonProviderProps) {
  return (
    <CommonContext.Provider
      value={{ config, currentUser, currentHome, availableHomes, setCurrentHome }}
    >
      {children}
    </CommonContext.Provider>
  )
}
