import React, { Component } from 'react'
import { Row, Input } from 'react-materialize'


class Login extends Component {
	
	render() {
		return (
			<section className="layout-section">
				<Row>
					<Input type="email" label="Email" s={12} />
					<Input type="password" label="password" s={12} />
					<Input type="submit" />
				</Row>
			</section>
		)
	}
}

export default Login
