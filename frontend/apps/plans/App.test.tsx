import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'

import { CommonProvider } from '../../contexts/CommonProvider'
import PlansApp from './App'
import React from 'react'

const homeTestUtil = (
  id = 1,
  address = 'Example road 1',
  numResidents = 2,
  numWeeksRecipeRotation = 2,
  weeklyBudget = 2000,
  isActive = true
) => ({
  id: id,
  address: address,
  numResidents: numResidents,
  numWeeksRecipeRotation: numWeeksRecipeRotation,
  weeklyBudget: weeklyBudget,
  isActive: isActive,
})

const userTestUtil = (
  id = 1,
  email = 'user@example.com',
  firstName = 'Example',
  lastName = 'User',
  isActive = true,
  isStaff = false,
  isSuperuser = false,
  home = undefined
) => ({
  id: id,
  email: email,
  firstName: firstName,
  lastName: lastName,
  fullName: `${firstName} ${lastName}`,
  isActive: isActive,
  isStaff: isStaff,
  isSuperuser: isSuperuser,
  home: home,
})

const configTestUtil = (isProduction = true) => ({
  isProduction: isProduction,
})

const createTestData = () => ({
  currentHome: homeTestUtil(),
  currentUser: userTestUtil(),
  availableHomes: [homeTestUtil(2, 'Example road 2')],
  config: configTestUtil(),
})

describe('Test PageApp app', () => {
  it('empty state provided when currentHome is null and availableHomes is empty', () => {
    const { config, currentUser } = createTestData()
    render(
      <CommonProvider
        currentHome={null}
        availableHomes={[]}
        config={config}
        currentUser={currentUser}
        setCurrentHome={() => console.log('Set home')}
      >
        <PlansApp />
      </CommonProvider>
    )

    expect(screen.getByText(/You are currently not assigned any homes/i)).toBeInTheDocument()
  })

  it('empty state matches snapshot', () => {
    const { config, currentUser } = createTestData()

    const { asFragment } = render(
      <CommonProvider
        currentHome={null}
        availableHomes={[]}
        config={config}
        currentUser={currentUser}
        setCurrentHome={() => console.log('Set home')}
      >
        <PlansApp />
      </CommonProvider>
    )

    expect(asFragment()).toMatchSnapshot()
  })

  it('normal state provided when currentHome is not null and availableHomes is empty', () => {
    const { config, currentHome, currentUser } = createTestData()
    render(
      <CommonProvider
        currentHome={currentHome}
        availableHomes={[]}
        config={config}
        currentUser={currentUser}
        setCurrentHome={() => console.log('Set home')}
      >
        <PlansApp />
      </CommonProvider>
    )

    expect(screen.getByText(/Plans/i)).toBeInTheDocument()
  })

  it('normal state provided when currenHome is null and availableHomes is not empty', () => {
    const { config, availableHomes, currentUser } = createTestData()
    render(
      <CommonProvider
        currentHome={null}
        availableHomes={availableHomes}
        config={config}
        currentUser={currentUser}
        setCurrentHome={() => console.log('Set home')}
      >
        <PlansApp />
      </CommonProvider>
    )

    expect(screen.getByText(/Plans/i)).toBeInTheDocument()
  })
})
