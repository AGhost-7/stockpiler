import React from 'react'
import ReactDOM from 'react-dom'
import './css/index.css'
import App from './js/App'
import { BrowserRouter } from 'react-router-dom'
import registerServiceWorker from './js/services/registerServiceWorker'

ReactDOM.render((
	<BrowserRouter>
		<App />
	</BrowserRouter>
), document.getElementById('root'))

registerServiceWorker()
