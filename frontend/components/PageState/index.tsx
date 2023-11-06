import { Text, Title, createStyles } from '@mantine/core'

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
  className?: string
}

function PageState({ title, message, icon, className }: PageStateProps) {
  const { classes } = useStyles()
  return (
    <div
      className={`${classes.main} ${className} border-2 border-dashed rounded-md flex items-center justify-center p-8`}
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
