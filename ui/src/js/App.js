import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import Header from './components/Header'
import Main from './components/Main'
import SPFooter from './components/SPFooter'

const mapStateToProps = (state) => {
	return {
		...state,
		user: state.user.user,
		isSignedUpIn: state.user.user.id,
		isLoggedIn: state.user.user.id && state.user.user.email_confirmed
	}
}

class App extends Component {

	render() {
		return (
			<div className='app'>
				<Header />
				<Main {...this.props} />
				<SPFooter />
			</div>

		)
	}
}

export default withRouter(connect(mapStateToProps)(App))
