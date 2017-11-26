import React, { Component } from 'react'
import SignUpForm from './forms/SignUpForm'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'

const mapStateToProps = (state) => {
	return {
		...state,
		user: state.user.user,
		request: {
			pending: state.user.pending,
			fulfilled: state.user.fulfilled,
			error: state.user.error,
			message: state.user.message
		}
	}
}

class SignUp extends Component {

	static propTypes = {
		request: PropTypes.object.isRequired,
	}

	render() {
		return (
			<main>
				<h1>Sign up</h1>	
				<SignUpForm {...this.props.request} />
			</main>
		)
	}
}

export default connect(mapStateToProps)(SignUp)
