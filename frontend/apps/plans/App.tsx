import Empty from '../../components/Empty'
import React from 'react'
import { useCommonContext } from '../../contexts/CommonProvider'

function PlansApp() {
  const { currentHome } = useCommonContext()

  if (currentHome === null) {
    return (
      <Empty
        title="You are currently not assigned any homes"
        message="Please contact an admin."
        className="min-h-screen"
      />
    )
  }

  return <p>Plans</p>
}

export default PlansApp
