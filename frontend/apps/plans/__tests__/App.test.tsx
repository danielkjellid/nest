import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { createCommonContextTestData } from '../../../contexts/__tests__/utils'
import { CommonProvider } from '../../../contexts/CommonProvider'
import PlansApp from '../App'

describe('Test PageApp app', () => {
  it('empty state provided when currentHome is null and availableHomes is empty', () => {
    const { config, currentUser } = createCommonContextTestData()
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
    const { config, currentUser } = createCommonContextTestData()

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
    const { config, currentHome, currentUser } = createCommonContextTestData()
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
})
