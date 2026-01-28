/* eslint-disable @typescript-eslint/no-unused-vars */
export default defineEventHandler((event) => {
  console.log('Hello World')
  return {
    hello: 'world'
  }
})
