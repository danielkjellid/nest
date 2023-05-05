import {
  Box,
  Drawer as MDrawer,
  DrawerProps as MDrawerProps,
  ModalBase,
  Text,
  Transition,
} from '@mantine/core'

import React from 'react'

interface DrawerProps extends MDrawerProps {
  opened: boolean
  title: string
  children: React.ReactNode
  actions: React.ReactNode
  onClose: () => void
}

function Drawer({
  opened,
  title,
  children,
  actions,
  onClose,
  overlayProps,
  withCloseButton,
  closeButtonProps,
}: DrawerProps) {
  const hasHeader = !!title || withCloseButton

  return (
    <MDrawer.Root opened={opened} onClose={onClose} position="right" size="lg">
      <ModalBase.Overlay {...overlayProps} />
      <ModalBase.Content radius={0} className="rounded-t-md" style={{ marginBottom: '80px' }}>
        {hasHeader && (
          <ModalBase.Header>
            {title && (
              <Text fz="xl" fw={500}>
                {title}
              </Text>
            )}
            <ModalBase.CloseButton {...closeButtonProps} />
          </ModalBase.Header>
        )}

        <ModalBase.Body>{children}</ModalBase.Body>
      </ModalBase.Content>
      <Transition mounted={opened} transition="slide-left" duration={200}>
        {(styles) => (
          <div
            className="absolute bottom-0 rounded-md"
            style={{ zIndex: 9999, width: 620, right: '8px', bottom: '8px' }}
          >
            <Box
              sx={(theme) => ({
                backgroundColor:
                  theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[1],
              })}
              className="rounded-b-md w-full p-4"
              style={{ height: '68px', ...styles }}
            >
              {actions}
            </Box>
          </div>
        )}
      </Transition>
    </MDrawer.Root>
  )
}

export default Drawer
