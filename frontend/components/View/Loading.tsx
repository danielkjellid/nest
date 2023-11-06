import { Loader, LoadingOverlay, Text } from '@mantine/core'

export interface LoadingProps {
  description?: string
}

function Loading({ description }: LoadingProps) {
  return (
    <LoadingOverlay
      visible
      loader={
        <div className="space-y-3 text-center">
          <Loader size="lg" className="mx-auto" />
          {description && <Text fz="md">{description}</Text>}
        </div>
      }
    />
  )
}

export default Loading
