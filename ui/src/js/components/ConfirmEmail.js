import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { confirmEmail } from '../actions/user-actions'
import { Row } from 'react-materialize'
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

class ConfirmEmail extends Component {

	static propTypes = {
		request: PropTypes.object,
		match: PropTypes.object.isRequired,
		user: PropTypes.object.isRequired,
		message: PropTypes.string
	}

	constructor(props) {
		super(props) 
		this.state = {
			id: null,
			email_confirmed: false,
			message: ''
		}
	}

	componentWillMount() {
		if(this.props.match.params.id) {
			this.setState({ id: this.props.match.params.id })	
		}

		if(this.props.message) {
			this.setState({ message: this.props.user.message })	
		}

		if(this.props.user.email_confirmed) {
			this.setState({ email_confirmed: this.props.user.email_confirmed })	
		}
	}

	componentDidMount() {
		if(this.state.id && !this.state.email_confirmed) {
			confirmEmail({ id: this.state.id })
		}
	}

	componentWillReceiveProps(nextProps) {
		if(nextProps.request.message !== this.state.message) {
			this.setState({ message: nextProps.request.message })
		}
	}

	getConfirmed() {
		return (
			<Row>
				<p>The email {this.props.user.email} is confirmed.</p>
			</Row>
		)	
	}

	getConfirming() {
		let message = this.state.message || 'We are confirming your email...'
		return (
			<Row>
				<h1> Email Confirmation </h1>
				<p>{message}</p>
			</Row> 
		)
	}

	render() {
		let body
		if(!this.props.user.id) {
			body = this.getConfirming()
		} else {
			body = this.getConfirmed()
		}
		return (
			<main className='layout'>
				{body}
			</main>
		)
	}
}

export default connect(mapStateToProps)(ConfirmEmail)
