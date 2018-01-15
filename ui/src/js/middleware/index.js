import { applyMiddleware } from 'redux'
import { createLogger } from 'redux-logger'
import promise from 'redux-promise-middleware'
import thunk from 'redux-thunk'


export default applyMiddleware(promise(), thunk, createLogger())
