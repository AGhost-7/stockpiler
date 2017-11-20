export function setUserName(name) {
	return {
		type: 'SET_USER_NAME',
		payload: name
	}
}

export function fetchUser() {
	return {
		type: 'FETCH_USER_FULFILLED',
		payload: {
			id: 1,
			name: 'billy bob',
		}
	}
}
