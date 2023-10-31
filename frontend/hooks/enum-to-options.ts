interface Option {
  label: string
  value: string
}

const useEnumToOptions = (e: object): Option[] =>
  Object.entries(
    Object.fromEntries(Object.entries(e).filter(([key, _val]) => Number.isNaN(Number(key))))
  ).map(([label, value]) => ({
    label,
    value: value.toString(),
  }))

export { useEnumToOptions }
