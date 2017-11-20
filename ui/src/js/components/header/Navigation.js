import React, { Component } from 'react'
import { Navbar } from 'react-materialize'
import { Link } from 'react-router-dom'



class Navigation extends Component {
	static propTypes = {
		title: () => {
			
		}
	}


	render() {
		return (
			<Navbar brand={this.props.title} right>
				<Link to='/'>Home</Link>
				<Link to='/get-started'>Get started</Link>
				<Link to='/login'>Login</Link>
				<Link to='/sign-up'>Sign-up</Link>
			</Navbar>
		)
	}
}

export default Navigation
