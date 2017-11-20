import React from 'react'
import ReactDOM from 'react-dom'
import './css/index.css'
import App from './js/App'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import registerServiceWorker from './js/services/registerServiceWorker'
import Store from'./js/Store'


ReactDOM.render((
	<BrowserRouter>
		<Provider store={Store}>	
			<App />
		</Provider>
	</BrowserRouter>
), document.getElementById('root'))

registerServiceWorker()
