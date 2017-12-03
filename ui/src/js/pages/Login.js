import React, { Component } from 'react'
import { Row, Input } from 'react-materialize'



class Login extends Component {
	
	render() {
		return (
			<main className='layout'>
				<Row>
					<Input type='email' label='Email' s={12} />
					<Input type='password' label='password' s={12} />
					<Input type='submit' />
				</Row>
			</main>
		)
	}
}

export default Login
