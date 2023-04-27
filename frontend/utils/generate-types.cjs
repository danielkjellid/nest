/* eslint-disable */
const OpenAPI = require('openapi-typescript-codegen')
const fs = require('fs')
const path = require('path')

const outputPath = './frontend/types/generated/dist'

const generateTypesFromSchema = () => {
  fs.readFile(path.join(__dirname, '../../schema.json'), (err, file) => {
    OpenAPI.generate({
      input: JSON.parse(file.toString()),
      output: outputPath,
      exportCore: true,
      exportModels: true,
      exportServices: false,
      exportSchemas: false,
      useOptions: true,
    })
  })
}

if (require.main === module) {
  generateTypesFromSchema()
}

module.exports = {
  generateTypesFromSchema,
}
