import { IconHeartBroken } from '@tabler/icons-react'

import PageState from '../PageState'

export interface ErrorProps {
  description: string
}

function Error({ description }: ErrorProps) {
  return (
    <PageState
      title="Something went wrong"
      className="min-h-screen"
      message={description}
      icon={<IconHeartBroken className="w-12 h-12 mx-auto" stroke={1.3} />}
    />
  )
}

export default Error
