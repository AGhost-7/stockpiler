/**
 * Add middleware here, store custom middleware in
 * `./custom/`
 */
import { createStore } from 'redux'
import reducer from './reducers'
import middleware from './middleware'

export default createStore(reducer, middleware)
