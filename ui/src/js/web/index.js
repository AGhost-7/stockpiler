import post from './post'
import get from './get'
import Store from '../Store'

const subscribe = Store.subscribe
const _dispatch = Store.dispatch

/**
 * handle _REJECTED promises
 *
 * @param object 
 */
const dispatch = object => {
	// if we're dispatching a promise then catch here
	if(object.payload instanceof Promise) {
		return _dispatch(object)
			.catch(() => {
				return
			})
	}

	return _dispatch
}


export { 
	post,
	get,
	dispatch,
	subscribe
}
