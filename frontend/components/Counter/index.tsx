import {
  ActionIcon,
  Input,
  NumberInput,
  NumberInputHandlers,
  useMantineTheme,
  InputProps,
  NumberInputProps,
} from '@mantine/core'
import { IconMinus, IconPlus } from '@tabler/icons-react'
import React, { useRef } from 'react'

interface CounterProps extends NumberInputProps {
  label?: string
  required?: boolean
  description?: string
  error?: string
  value: number
  className?: string
  onChange: (value: number | '') => void
}

function Counter({
  label,
  required,
  description,
  error,
  value,
  className,
  onChange,
  ...props
}: CounterProps) {
  const theme = useMantineTheme()
  const handlers = useRef<NumberInputHandlers>()

  return (
    <Input.Wrapper
      label={label}
      required={required}
      description={description}
      error={error}
      className={`w-full ${className}`}
    >
      <div className="flex items-center w-full space-x-2">
        <ActionIcon
          color={theme.primaryColor}
          variant="outline"
          size="lg"
          onClick={() => handlers.current?.decrement()}
          disabled={!!props.min && value <= props.min}
        >
          <IconMinus />
        </ActionIcon>
        <NumberInput
          hideControls
          className="w-full"
          value={value}
          onChange={(val) => onChange(val)}
          handlersRef={handlers}
          styles={{ input: { textAlign: 'center' } }}
          {...props}
        />
        <ActionIcon
          color={theme.primaryColor}
          variant="outline"
          size="lg"
          onClick={() => handlers.current?.increment()}
          disabled={!!props.max && value >= props.max}
        >
          <IconPlus />
        </ActionIcon>
      </div>
    </Input.Wrapper>
  )
}

export { Counter }
