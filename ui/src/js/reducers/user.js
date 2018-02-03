const userReducer = (state = {
	id: '',
	email: '',
	username: '',
}, actions) => {
	switch(actions.type) {
		case "GET_USER":
			state = {...state}
			break
		default:
			break
	}
	return state
}

export default userReducer
