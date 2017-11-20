import React, { Component } from 'react'
import { Navbar } from 'react-materialize'
import { Link } from 'react-router-dom'



class Navigation extends Component {
	static propTypes = {
		title: () => {}
	}


	render() {
		return (
			<Navbar brand={this.props.title} right>
				<li><Link to='/'>Home</Link></li>
				<li><Link to='/get-started'>Get started</Link></li>
				<li><Link to='/login'>Login</Link></li>
				<li><Link to='/sign-up'>Sign-up</Link></li>
			</Navbar>
		)
	}
}

export default Navigation
