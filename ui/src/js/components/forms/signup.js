import React from 'react'

export default class SignupForm extends React.Component {

	render () {
		return (
			<form class="col s12 m6">
				<div class="row">
					<div class="input-field">
						<input id="signup_username" type="text" class="validate" />
						<label for="signup_username">Username</label>
					</div>
				</div>
				<div class="row">
					<div class="input-field">
						<input id="signup_password" type="password" class="validate" />
						<label for="signup_password">Password</label>
					</div>
				</div>
				<div class="row">
					<div class="input-field">
						<input id="signup_email" type="email" class="validate" />
						<label for="signup_email">Email</label>
					</div>
				</div>
				<div class="row">
					<div class="input-field">
						<input class="btn" id="signup_submit" type="submit" />
					</div>
				</div>
			</form>)
	}
}
