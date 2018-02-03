export default function isPromise(value) {
	if (value !== null && typeof value === 'object'
		return typeof value.then === 'function'

	return false;
}
