import { post, get, dispatch } from '../api'

export function register(payload) {
	return dispatch({
		type: 'USERS_REGISTER', 
		payload: post('//localhost:5000/v1/users/register', payload)
	})

}

export function confirmEmail(payload) {

	return dispatch({
		type: 'USERS_CONFIRM_EMAIL', 
		payload: get(`//localhost:5000/v1/users/confirm-email/${payload.id}`)
	})

}
