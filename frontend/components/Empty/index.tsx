import { Text, Title, createStyles } from '@mantine/core'

import { IconMoodSad } from '@tabler/icons-react'
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

interface EmptyProps {
  title: string
  message: string
}

function Empty({ title, message }: EmptyProps) {
  const { classes } = useStyles()
  return (
    <div
      className={`${classes.main} border-2 border-dashed rounded-md h-full flex items-center justify-center`}
    >
      <div className={`${classes.text} text-center space-y-2`}>
        <IconMoodSad className={`${classes.icon} h-12 w-12`} stroke={1.3} />
        <Title fz="lg" fw="bold">
          {title}
        </Title>
        <Text>{message}</Text>
      </div>
    </div>
  )
}

export default Empty
