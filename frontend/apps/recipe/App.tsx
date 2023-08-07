import React, { useState } from 'react'
import BaseApp from '../../components/BaseApp/BaseApp'
import Header from '../../components/Header'
import { Recipe } from './components/Recipe'

import { CommonProvider, CommonContextType } from '../../contexts/CommonProvider'

function RecipeAppInner() {
  return <Recipe />
}

function RecipeApp(props: CommonContextType) {
  const { currentUser, availableHomes, config } = props
  let home: CommonContextType['currentHome']

  if (currentUser) {
    if (currentUser.home) {
      home = currentUser.home
    } else if (!currentUser.home && availableHomes.length) {
      home = availableHomes.sort((a, b) => a.id - b.id)[0]
    } else {
      home = null
    }
  } else {
    home = null
  }

  const [currentHome, setCurrentHome] = useState<CommonContextType['currentHome']>(home)

  return (
    <CommonProvider
      config={config}
      currentUser={currentUser}
      currentHome={currentHome}
      availableHomes={availableHomes}
      setCurrentHome={setCurrentHome}
    >
      <BaseApp header={<Header />}>
        <RecipeAppInner />
      </BaseApp>
    </CommonProvider>
  )
}

export { RecipeApp }
