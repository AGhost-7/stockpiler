import React from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'
//components
import Header from './header'
import Footer from './footer'
//pages
import Home from '../pages/home'
import Register from '../pages/register'

export default class Layout extends React.Component {
	render() {
		return (
			<div id='full-display'>
				<Header />
				<main>
					<Switch>
						<Route path='/' exact component={Home} />
						<Route path='/register' component={Register} />
						<Redirect to='/' />
					</Switch>
				</main>
				<Footer />
			</div>
		)
	}

}

