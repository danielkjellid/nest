import Form from '../../components/Form'
import { useForm2 } from '../../hooks/forms/form'

function SettingsApp() {
  const form = useForm2({ key: 'TestForm' })
  return (
    <div>
      <p>{JSON.stringify(form)}</p>
      <Form {...form} />
      <button onClick={() => form.validate()}>Validate</button>
    </div>
  )
}

export default SettingsApp
