/**
 * Our store, see readme's in either reducers or middelware
 * for more information
 */
import { createStore } from 'redux'
import reducer from './reducers'
import middleware from './middleware'

export default createStore(reducer, middleware)
