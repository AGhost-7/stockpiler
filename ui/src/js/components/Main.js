import React, { Component } from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'

// when the user is not logged in
import Home from '../pages/Home'
import Login from '../pages/Login'
import SignUp from '../pages/SignUp'
import ConfirmEmail from '../pages/ConfirmEmail'
// when the user is logged in


class Main extends Component {

	render() {
		return (
			<Switch>
				<Route exact path='/' component={Home} />
				<Route path='/login' component={Login} />
				<Route path='/sign-up' component={SignUp} />
				<Route path='/email-confirmation/:id' component={ConfirmEmail} />
				<Redirect to="/" />
			</Switch>
		)
	}
}

export default Main
