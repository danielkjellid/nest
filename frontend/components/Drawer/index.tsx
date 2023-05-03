import {
  Box,
  Drawer as MDrawer,
  DrawerProps as MDrawerProps,
  ModalBase,
  ScrollArea,
  Text,
} from '@mantine/core'

import React from 'react'

interface DrawerProps extends MDrawerProps {
  opened: boolean
  title: string
  children: React.ReactNode
  actions?: React.ReactNode
  onClose: () => void
}

function Drawer({
  opened,
  title,
  children,
  actions,
  onClose,
  withOverlay,
  overlayProps,
  withCloseButton,
  closeButtonProps,
}: DrawerProps) {
  const hasHeader = !!title || withCloseButton

  return (
    <MDrawer.Root opened={opened} onClose={onClose} position="right" size="lg">
      {withOverlay && <ModalBase.Overlay {...overlayProps} />}
      <ModalBase.Content
        radius={0}
        className="relative h-screen"
        style={{ bottom: '67px', top: 0 }}
      >
        {hasHeader && (
          <ModalBase.Header>
            {title && (
              <Text fz="xl" fw={500}>
                {title}
              </Text>
            )}
            {withCloseButton && <ModalBase.CloseButton {...closeButtonProps} />}
          </ModalBase.Header>
        )}

        <ModalBase.Body>
          {children}
          <div className="bg-green-400 h-96 w-full"></div>
          <div className="bg-green-400 h-96 w-full"></div>
          <div className="bg-green-400 h-96 w-full"></div>
          <div className="bg-green-400 h-96 w-full"></div>
          <div className="bg-green-400 h-96 w-full"></div>
        </ModalBase.Body>
      </ModalBase.Content>
      {actions && (
        <div className="absolute bottom-0 right-0" style={{ zIndex: 9999, width: 620 }}>
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
      )}
    </MDrawer.Root>
    // <MDrawer
    //   size="lg"
    //   opened={opened}
    //   onClose={onClose}
    //   title={
    // <Text fz="xl" fw={500}>
    //   {title}
    // </Text>
    //   }
    //   position="right"
    //   className="relative"
    // >
    //   <ScrollArea>{children}</ScrollArea>
    // {actions && (
    //   <div className="absolute bottom-0 right-0 left-0">
    //     <Box
    //       sx={(theme) => ({
    //         backgroundColor:
    //           theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[1],
    //       })}
    //       className="p-4 w-full"
    //     >
    //       {actions}
    //     </Box>
    //   </div>
    // )}
    // </MDrawer>
  )
}

export default Drawer
