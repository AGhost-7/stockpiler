import React from 'react'
import NavBar from './navbar'
import MenuItem from './menu-item'


export default class Header extends React.Component {
	render() {
		return (
			<header>
				<NavBar>
					<MenuItem href='/'>Home</MenuItem>
					<MenuItem href='/register'>Register</MenuItem>
				</NavBar>
			</header>
		)
	}

}

