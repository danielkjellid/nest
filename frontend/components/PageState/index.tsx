import { Text, Title, createStyles } from '@mantine/core'

import React from 'react'

const useStyles = createStyles((theme) => ({
  main: {
    borderColor: theme.colorScheme === 'dark' ? theme.colors.gray[7] : theme.colors.gray[4],
  },

  text: {
    color: theme.colorScheme === 'dark' ? theme.colors.gray[5] : theme.colors.gray[7],
  },

  icon: {
    color: theme.colors.gray[6],
  },
}))

interface PageStateProps {
  title: string
  message: string
  icon: React.ReactNode
}

function PageState({ title, message, icon }: PageStateProps) {
  const { classes } = useStyles()
  return (
    <div
      className={`${classes.main} border-2 border-dashed rounded-md h-full flex items-center justify-center`}
    >
      <div className={`${classes.text} text-center space-y-2`}>
        {icon}
        <Title fz="lg" fw="bold">
          {title}
        </Title>
        <Text>{message}</Text>
      </div>
    </div>
  )
}

export default PageState
