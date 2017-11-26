import React, { Component } from 'react'
import { Route, Switch, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import Header from './components/Header'
import SPFooter from './components/SPFooter'
import Home from './components/Home'
import Login from './components/Login'
import SignUp from './components/SignUp'
import ConfirmEmail from './components/ConfirmEmail'

const mapStateToProps = (state) => {
	return {
		...state,
		user: state.user.user,
	}
}

class App extends Component {

	render() {
		return (
			<div className='app'>
				<Header />
				<Switch>
					<Route exact path='/' component={Home} />
					<Route path='/login' component={Login} />
					<Route path='/sign-up' component={SignUp} />
					<Route path='/email-confirmation/:id' component={ConfirmEmail} />
				</Switch>
				<SPFooter />
			</div>

		)
	}
}

export default withRouter(connect(mapStateToProps)(App))
