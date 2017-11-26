import { combineReducers } from 'redux'
// list reducers here
import userReducer from './user-reducer'


export default combineReducers({
	user: userReducer
})
