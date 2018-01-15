export default function post (url = '', payload = {}, options = {}) {
	var request = new Request(url, {
		headers: new Headers({
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		})
	})

	if (options == null) options = {}
	if (options.credentials == null) options.credentials = 'same-origin'
	
	options.method = 'POST'
	options.body = JSON.stringify(payload)

	return fetch(request, options)
		.then((resp) => {
			let json = resp.json()
			if (resp.ok) {
				return json
			} else {
				return json.then(Promise.reject.bind(Promise))
			}
		})
}
