import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import Layout from './components/layout'
import { Provider } from 'react-redux'
import store from './store'

export default class App extends React.Component {
	componentDidMount() {
		store.dispatch((dispatch) => {
			dispatch({type: "GET_USER"})
		})
	}

	render() {
		return (
			<Provider store={store}>
				<BrowserRouter>
					<Layout />
				</BrowserRouter>
			</Provider>
			)
	}
}

