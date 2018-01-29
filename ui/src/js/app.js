import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import Layout from './components/layout'
import { Provider } from 'react-redux'
import Store from './store'

export default class App extends React.Component {
	componentDidMount() {
		Store.dispatch({type: "GET_USER"})
	}

	render() {
		return (
			<Provider store={Store}>
				<BrowserRouter>
					<Layout />
				</BrowserRouter>
			</Provider>
			)
	}
}

