import Form from '../../components/Form'
import { useForm } from '../../hooks/forms/form'

function SettingsApp() {
  const form = useForm({ key: 'RecipeCreateForm' })
  return (
    <div>
      <p>{JSON.stringify(form)}</p>
      <Form {...form} />
      <button onClick={() => form.validate()}>Validate</button>
    </div>
  )
}

export default SettingsApp
