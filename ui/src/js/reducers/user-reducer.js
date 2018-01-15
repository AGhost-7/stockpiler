const userReducer = (state = {
	user: {
		id: null,
		name: null,
		email: null,
		email_confirmed: false
	},
	pending: false,
	fulfilled: false,
	error: false
}, action) => {
	
	switch (action.type) {

	case 'USERS_REGISTER_PENDING':
	case 'USERS_CONFIRM_EMAIL_PENDING':
		state = {
			...state,
			error: false,
			pending: true,
			fulfilled: false
		}
		break
	
	case 'USERS_REGISTER_FULFILLED':
	case 'USERS_CONFIRM_EMAIL_FULFILLED':
		state = {
			...state,
			user: action.payload,
			error: false,
			pending: false,
			fulfilled: true
		}
		break

	case 'USERS_REGISTER_REJECTED':
	case 'USERS_CONFIRM_EMAIL_REJECTED':
		state = {
			...state,
			message: action.payload.message,
			error: true,
			pending: false,
			fulfilled: false
		}
		break

	default:
		break
	}
	return state
}

export default userReducer
