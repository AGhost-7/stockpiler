import React from 'react'
import ReactDOM from 'react-dom'
import App from '../js/App'
import registerServiceWorker from '../js/services/registerServiceWorker'

describe('Testing', () => {

	it('renders without crashing', () => {
		const div = document.createElement('div')
		ReactDOM.render(<App />, div)
		registerServiceWorker()
	})

})
