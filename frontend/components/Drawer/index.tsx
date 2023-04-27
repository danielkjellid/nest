import { Box, Drawer as MDrawer, Text } from '@mantine/core'

import React from 'react'

interface DrawerProps {
  opened: boolean
  title: string
  children: React.ReactNode
  actions?: React.ReactNode
  onClose: () => void
}

function Drawer({ opened, title, children, actions, onClose }: DrawerProps) {
  return (
    <MDrawer
      size="lg"
      opened={opened}
      onClose={onClose}
      title={
        <Text fz="xl" fw={500}>
          {title}
        </Text>
      }
      position="right"
    >
      {children}
      <div className="absolute bottom-0 right-0 left-0">
        <Box
          sx={(theme) => ({
            backgroundColor:
              theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[1],
          })}
          className="p-4 w-full"
        >
          {actions}
        </Box>
      </div>
    </MDrawer>
  )
}

export default Drawer
