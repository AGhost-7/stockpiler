import React from 'react'

export default class LoginForm extends React.Component {

	constructor(props) {
		super(props)
		this.onSubmit = this.onSubmit.bind(this)
	}

	onSubmit() {
		console.log('test');
		return false;
	}

	render () {
		return (
			<form class="col s12 m6"i onSubmit={this.onSubmit}>
				<div class="row">
					<div class="input-field">
						<input id="login_username" type="text" class="validate" />
						<label for="login_username">Username</label>
					</div>
				</div>
				<div class="row">
					<div class="input-field">
						<input id="login_password" type="password" class="validate" />
						<label for="login_password">Password</label>
					</div>
				</div>
				<div class="row">
					<div class="input-field">
						<input class="btn" id="login_submit" type="submit" />
					</div>
				</div>
			</form>)
	}
}
