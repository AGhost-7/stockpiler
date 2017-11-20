export default function reducer(state = {
	user: {
		id: null,
		name: null
	}
}, action) {
	switch (action.type) {
	case 'CHANGE_NAME':
		return {
			...state,
			name: action.payload
		}

	case 'LOGIN': 
		break

	default: 
		break
	}
	return state
}
