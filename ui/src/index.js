import React from 'react'
import ReactDOM from 'react-dom'
import './css/index.css'
import App from './js/App'
import registerServiceWorker from './js/services/registerServiceWorker'
import { Provider } from 'react-redux'
import { BrowserRouter as Router } from 'react-router-dom'
import Store from './js/Store'

ReactDOM.render((
	<Provider store={Store}>
		<Router>
			<App />
		</Router>
	</Provider>
), document.getElementById('root'))
registerServiceWorker()
