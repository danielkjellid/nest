import { CommonContextType, CommonProvider } from '../state/CommonProvider'
import React, { useState } from 'react'

import BaseApp from './BaseApp'
import Header from '../components/Header'
import Navbar from '../components/Navbar'

declare global {
  interface Window {
    initialProps: CommonContextType
  }
}

function MainAppInner(props: CommonContextType) {
  console.log(props)
  return <div className="h-screen border-2 border-dashed border-gray-200 rounded-md"></div>
}

function MainApp(props: CommonContextType) {
  const { currentUser, availableHomes } = props
  /**********
   ** Home **
   **********/

  let home: CommonContextType['currentHome']

  // if (currentUser.home) {
  //   home = currentUser.home
  // } else if (!currentUser.home && availableHomes.length) {
  //   home = availableHomes.sort((a, b) => a.id - b.id)[0]
  // } else {
  //   home = null
  //   // TODO: redirect/show empty state - no homes assigned
  // }

  if (currentUser.home) {
    home = currentUser.home
  } else {
    home = availableHomes.sort((a, b) => a.id - b.id)[0]
  }

  const [currentHome, setCurrentHome] = useState<CommonContextType['currentHome']>(home)

  return (
    <CommonProvider
      config={props.config}
      currentUser={props.currentUser}
      currentHome={currentHome}
      availableHomes={availableHomes}
      setCurrentHome={setCurrentHome}
    >
      <BaseApp navbar={<Navbar />} header={<Header />}>
        <MainAppInner {...props} />
      </BaseApp>
    </CommonProvider>
  )
}

export default MainApp
