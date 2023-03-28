import Empty from '../../components/Empty'
import React from 'react'
import { useCommonContext } from '../../contexts/CommonProvider'

function PlansApp() {
  const { currentHome, availableHomes } = useCommonContext()

  if (currentHome === null && !availableHomes.length) {
    return (
      <Empty title="You are currently not assigned any homes" message="Please contact an admin." />
    )
  }

  return <p>Plans</p>
}

export default PlansApp
