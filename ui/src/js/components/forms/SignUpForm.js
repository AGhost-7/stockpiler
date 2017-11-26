import React, { Component } from 'react'
import { Row, Input } from 'react-materialize'
import { register } from '../../actions/user-actions'
import PropTypes from 'prop-types'


class SignUpForm extends Component {

	static propTypes = {
		error: PropTypes.bool.isRequired,
		fulfilled: PropTypes.bool.isRequired,
		pending: PropTypes.bool.isRequired,
		message: PropTypes.string
	}


	constructor(props) {
		super(props)
		this.initState = {
			email: '',
			password: '',
			error: false,
			pending: false,
			fulfilled: false,
			message: ''
		}
		this.state = this.initState
		this.handleChange = this.handleChange.bind(this)    
		this.handleSubmit = this.handleSubmit.bind(this)
	}

	componentWillReceiveProps(nextProps) {
		if (nextProps.error !== this.props.error) {
			this.setState({ error: nextProps.error })
		}
		if (nextProps.pending !== this.props.pending) {
			this.setState({ pending: nextProps.pending })
		}
		if (nextProps.fulfilled !== this.props.fulfilled) {
			this.setState({ fulfilled: nextProps.fulfilled })
		}
		if (nextProps.message !== this.state.message) {
			this.setState({ message: nextProps.message })
		}
	}

	handleChange(e) {
		this.setState({
			[e.target.name]:  e.target.value
		})
	}

	handleSubmit(e) {
		e.preventDefault()

		register(this.state)
	}

	getForm() {
		const { email, password } = this.state
		return (
			<form id='register' onSubmit={this.handleSubmit.bind(this)}>
				<Row>
					<fieldset disabled={this.state.error || this.state.pending}>
						<Input type='email' label='email' value={email} name='email' s={12} onChange={this.handleChange.bind(this)} />
						<Input type='password' label='password' value={password} name='password' s={12} onChange={this.handleChange.bind(this)} />
						<Input type='submit' />
					</fieldset>
				</Row>
			</form>
		)
	}

	getThankYou() {
		return (
			<Row>
				<p className='thank-you'>Thank you for registering, check you email for confirm your account.</p>
			</Row>
		)
	}

	getError() {
		return (
			<Row> 
				<p>{ this.state.message }</p>
				<button onClick={this.resetForm.bind(this)}>Try again</button>
			</Row>
		)
	}

	resetForm() {
		document.getElementById('register').reset()
		this.setState(this.initState)
	}


	render() {
		let body
		let errorBlock = this.state.error ? this.getError() : null
		if(!this.state.fulfilled) { 
			body = this.getForm()
		} else {
			body = this.getThankYou()
		}
		return (
			<div>
				{ errorBlock }
				{ body }
			</div>)
	}
}

export default SignUpForm
